"""
Niching Particle Swarm Optimization (Niching PSO) Algorithm Implementation

This module provides an implementation of PSO with niching capabilities
to maintain multiple optima through dynamic neighborhoods.
"""

import numpy as np


class NichingPSOConfig:
    """Configuration parameters for Niching PSO algorithm"""
    def __init__(
        self,
        n_particles=10,
        w=0.7,
        c1=1.5,
        c2=1.5,
        max_iterations=50,
        bounds=(-5, 5),
        v_max=1.0,
        n_neighbors=3,
        radius=1.0
    ):
        self.n_particles = n_particles
        self.w = w  # Inertia weight
        self.c1 = c1  # Cognitive parameter
        self.c2 = c2  # Social parameter
        self.max_iterations = max_iterations
        self.bounds = bounds
        self.v_max = v_max
        self.n_neighbors = n_neighbors  # Max number of neighbors
        self.radius = radius  # Connection radius


def rastrigin_function(x):
    """
    Calculate Rastrigin function for positions
    
    Args:
        x: numpy array of shape (n_particles, 2)
        
    Returns:
        numpy array of fitness values
    """
    n = x.shape[1]  # number of dimensions (should be 2)
    return 10 * n + np.sum(x**2 - 10 * np.cos(2 * np.pi * x), axis=1)


def find_connected_particles(particle_idx, positions, n_neighbors, radius):
    """
    Find connected particles for a given particle.
    Returns indices of n closest particles within radius r.
    
    Args:
        particle_idx: Index of the particle
        positions: Array of all particle positions
        n_neighbors: Maximum number of neighbors to connect
        radius: Connection radius
        
    Returns:
        Array of indices of connected particles
    """
    particle_pos = positions[particle_idx]
    
    # Calculate distances to all other particles
    distances = np.linalg.norm(positions - particle_pos, axis=1)
    
    # Exclude the particle itself
    distances[particle_idx] = np.inf
    
    # Find particles within radius
    within_radius = distances <= radius
    
    if not np.any(within_radius):
        # No particles within radius, return empty array
        return np.array([], dtype=int)
    
    # Get indices of particles within radius, sorted by distance
    candidate_indices = np.where(within_radius)[0]
    candidate_distances = distances[candidate_indices]
    sorted_indices = candidate_indices[np.argsort(candidate_distances)]
    
    # Return at most n_neighbors closest particles
    return sorted_indices[:n_neighbors]


def initialize_niching_pso(config, fitness_function=rastrigin_function):
    """
    Initialize Niching PSO with random positions and velocities
    
    Args:
        config: NichingPSOConfig object with algorithm parameters
        fitness_function: Function to evaluate particle fitness
        
    Returns:
        Dictionary containing initial Niching PSO state
    """
    positions = np.random.uniform(
        config.bounds[0],
        config.bounds[1],
        (config.n_particles, 2)
    )
    velocities = np.random.uniform(
        -config.v_max,
        config.v_max,
        (config.n_particles, 2)
    )
    
    fitnesses = fitness_function(positions)
    pbest_positions = positions.copy()
    pbest_fitnesses = fitnesses.copy()
    
    # Initialize social bests (initially same as personal bests)
    sbest_positions = positions.copy()
    sbest_fitnesses = fitnesses.copy()
    
    # Initialize connections (will be updated at each iteration)
    connections = [find_connected_particles(i, positions, config.n_neighbors, config.radius) 
                   for i in range(config.n_particles)]
    
    return {
        'positions': positions,
        'velocities': velocities,
        'pbest_positions': pbest_positions,
        'pbest_fitnesses': pbest_fitnesses,
        'sbest_positions': sbest_positions,
        'sbest_fitnesses': sbest_fitnesses,
        'connections': connections,
        'iteration': 0
    }


def niching_pso_step(state, config, fitness_function=rastrigin_function):
    """
    Execute one Niching PSO iteration
    
    Args:
        state: Current Niching PSO state dictionary
        config: NichingPSOConfig object with algorithm parameters
        fitness_function: Function to evaluate particle fitness
        
    Returns:
        Dictionary containing updated Niching PSO state
    """
    # Create copies to avoid modifying original state
    positions = state['positions'].copy()
    velocities = state['velocities'].copy()
    pbest_positions = state['pbest_positions'].copy()
    pbest_fitnesses = state['pbest_fitnesses'].copy()
    sbest_positions = state['sbest_positions'].copy()
    sbest_fitnesses = state['sbest_fitnesses'].copy()
    
    # Update connections for each particle
    connections = [find_connected_particles(i, positions, config.n_neighbors, config.radius) 
                   for i in range(config.n_particles)]
    
    # Update social bests based on connected particles
    for i in range(config.n_particles):
        connected = connections[i]
        if len(connected) > 0:
            # Social best is the best personal best among connected particles
            connected_pbests = pbest_fitnesses[connected]
            best_connected_idx = connected[np.argmin(connected_pbests)]
            
            # Update social best if a connected particle has better personal best
            if pbest_fitnesses[best_connected_idx] < sbest_fitnesses[i]:
                sbest_positions[i] = pbest_positions[best_connected_idx].copy()
                sbest_fitnesses[i] = pbest_fitnesses[best_connected_idx]
    
    # Update velocities and positions for each particle
    for i in range(config.n_particles):
        r1 = np.random.random(2)
        r2 = np.random.random(2)
        
        # Calculate velocity components
        inertia_component = config.w * velocities[i]
        cognitive_component = config.c1 * r1 * (pbest_positions[i] - positions[i])
        social_component = config.c2 * r2 * (sbest_positions[i] - positions[i])
        
        # Update velocity
        velocities[i] = inertia_component + cognitive_component + social_component
        
        # Limit velocity
        velocities[i] = np.clip(velocities[i], -config.v_max, config.v_max)
        
        # Update position
        positions[i] = positions[i] + velocities[i]
        
        # Apply boundary constraints
        positions[i] = np.clip(positions[i], config.bounds[0], config.bounds[1])
    
    # Evaluate fitnesses
    fitnesses = fitness_function(positions)
    
    # Update personal bests
    improved = fitnesses < pbest_fitnesses
    pbest_positions[improved] = positions[improved]
    pbest_fitnesses[improved] = fitnesses[improved]
    
    # Update social bests if personal best improved
    for i in range(config.n_particles):
        if improved[i] and pbest_fitnesses[i] < sbest_fitnesses[i]:
            sbest_positions[i] = pbest_positions[i].copy()
            sbest_fitnesses[i] = pbest_fitnesses[i]
    
    return {
        'positions': positions,
        'velocities': velocities,
        'pbest_positions': pbest_positions,
        'pbest_fitnesses': pbest_fitnesses,
        'sbest_positions': sbest_positions,
        'sbest_fitnesses': sbest_fitnesses,
        'connections': connections,
        'iteration': state['iteration'] + 1
    }


def run_complete_niching_pso(config, fitness_function=rastrigin_function):
    """
    Run Niching PSO for max_iterations and store all states
    
    Args:
        config: NichingPSOConfig object with algorithm parameters
        fitness_function: Function to evaluate particle fitness
        
    Returns:
        List of state dictionaries for each iteration
    """
    states = []
    state = initialize_niching_pso(config, fitness_function)
    states.append(state.copy())
    
    for _ in range(config.max_iterations):
        state = niching_pso_step(state, config, fitness_function)
        
        # Deep copy arrays to preserve state
        new_state = {
            'positions': state['positions'].copy(),
            'velocities': state['velocities'].copy(),
            'pbest_positions': state['pbest_positions'].copy(),
            'pbest_fitnesses': state['pbest_fitnesses'].copy(),
            'sbest_positions': state['sbest_positions'].copy(),
            'sbest_fitnesses': state['sbest_fitnesses'].copy(),
            'connections': [conn.copy() for conn in state['connections']],
            'iteration': state['iteration']
        }
        
        states.append(new_state)
    
    return states


def initialize_niching_pso_history(config, fitness_function=rastrigin_function):
    """
    Pre-compute complete Niching PSO run and store all states
    
    Args:
        config: NichingPSOConfig object with algorithm parameters
        fitness_function: Function to evaluate particle fitness
        
    Returns:
        Dictionary with all states and current index
    """
    all_states = run_complete_niching_pso(config, fitness_function)
    return {
        'all_states': all_states,
        'current_index': 0
    }

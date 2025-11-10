"""
Particle Swarm Optimization (PSO) Algorithm Implementation

This module provides a complete implementation of the PSO algorithm
for optimization tasks.
"""

import numpy as np


class PSOConfig:
    """Configuration parameters for PSO algorithm"""
    def __init__(
        self,
        n_particles=3,
        w=0.7,
        c1=1.5,
        c2=1.5,
        max_iterations=50,
        bounds=(-5, 5),
        v_max=1.0
    ):
        self.n_particles = n_particles
        self.w = w  # Inertia weight
        self.c1 = c1  # Cognitive parameter
        self.c2 = c2  # Social parameter
        self.max_iterations = max_iterations
        self.bounds = bounds
        self.v_max = v_max


def sphere_function(x):
    """
    Calculate sphere function for positions
    
    Args:
        x: numpy array of shape (n_particles, 2)
        
    Returns:
        numpy array of fitness values
    """
    return np.sum(x**2, axis=1)


def rastrigin_function(x):
    """
    Calculate Rastrigin function for positions
    
    The Rastrigin function is a highly multi-modal function with many local optima.
    Global minimum: f(0,0) = 0
    
    Formula (2D): f(x,y) = 20 + x² - 10*cos(2πx) + y² - 10*cos(2πy)
    
    Args:
        x: numpy array of shape (n_particles, 2)
        
    Returns:
        numpy array of fitness values
    """
    n = x.shape[1]  # number of dimensions (should be 2)
    return 10 * n + np.sum(x**2 - 10 * np.cos(2 * np.pi * x), axis=1)


def initialize_pso(config, fitness_function=sphere_function):
    """
    Initialize PSO with random positions and velocities
    
    Args:
        config: PSOConfig object with algorithm parameters
        fitness_function: Function to evaluate particle fitness
        
    Returns:
        Dictionary containing initial PSO state
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
    
    gbest_idx = np.argmin(fitnesses)
    gbest_position = positions[gbest_idx].copy()
    gbest_fitness = fitnesses[gbest_idx]
    
    return {
        'positions': positions,
        'velocities': velocities,
        'pbest_positions': pbest_positions,
        'pbest_fitnesses': pbest_fitnesses,
        'gbest_position': gbest_position,
        'gbest_fitness': gbest_fitness,
        'iteration': 0
    }


def pso_step(state, config, fitness_function=sphere_function):
    """
    Execute one PSO iteration
    
    Args:
        state: Current PSO state dictionary
        config: PSOConfig object with algorithm parameters
        fitness_function: Function to evaluate particle fitness
        
    Returns:
        Dictionary containing updated PSO state
    """
    # Create copies to avoid modifying original state
    positions = state['positions'].copy()
    velocities = state['velocities'].copy()
    pbest_positions = state['pbest_positions'].copy()
    pbest_fitnesses = state['pbest_fitnesses'].copy()
    gbest_position = state['gbest_position'].copy()
    gbest_fitness = state['gbest_fitness']
    
    # Calculate velocity components
    r1 = np.random.random((config.n_particles, 2))
    r2 = np.random.random((config.n_particles, 2))
    
    inertia_component = config.w * velocities
    cognitive_component = config.c1 * r1 * (pbest_positions - positions)
    social_component = config.c2 * r2 * (gbest_position - positions)
    
    # Update velocities
    velocities = inertia_component + cognitive_component + social_component
    
    # Limit velocities
    velocities = np.clip(velocities, -config.v_max, config.v_max)
    
    # Update positions
    positions = positions + velocities
    
    # Apply boundary constraints
    positions = np.clip(positions, config.bounds[0], config.bounds[1])
    
    # Evaluate fitnesses
    fitnesses = fitness_function(positions)
    
    # Update personal bests
    improved = fitnesses < pbest_fitnesses
    pbest_positions[improved] = positions[improved]
    pbest_fitnesses[improved] = fitnesses[improved]
    
    # Update global best
    min_idx = np.argmin(pbest_fitnesses)
    if pbest_fitnesses[min_idx] < gbest_fitness:
        gbest_position = pbest_positions[min_idx].copy()
        gbest_fitness = pbest_fitnesses[min_idx]
    
    return {
        'positions': positions,
        'velocities': velocities,
        'pbest_positions': pbest_positions,
        'pbest_fitnesses': pbest_fitnesses,
        'gbest_position': gbest_position,
        'gbest_fitness': gbest_fitness,
        'iteration': state['iteration'] + 1
    }


def calculate_velocity_components(state, config):
    """
    Calculate the three velocity components for next iteration
    
    Args:
        state: Current PSO state dictionary
        config: PSOConfig object with algorithm parameters
        
    Returns:
        Tuple of (inertia_component, cognitive_component, social_component)
    """
    positions = state['positions']
    velocities = state['velocities']
    pbest_positions = state['pbest_positions']
    gbest_position = state['gbest_position']
    
    # Generate random values
    r1 = np.random.random((config.n_particles, 2))
    r2 = np.random.random((config.n_particles, 2))
    
    # Calculate components
    inertia_component = config.w * velocities
    cognitive_component = config.c1 * r1 * (pbest_positions - positions)
    social_component = config.c2 * r2 * (gbest_position - positions)
    
    return inertia_component, cognitive_component, social_component


def run_complete_pso(config, fitness_function=sphere_function):
    """
    Run PSO for MAX_ITERATIONS and store all states
    
    Args:
        config: PSOConfig object with algorithm parameters
        fitness_function: Function to evaluate particle fitness
        
    Returns:
        List of state dictionaries for each iteration
    """
    states = []
    state = initialize_pso(config, fitness_function)
    
    # Calculate velocity components for first state (showing move from iteration 0 to 1)
    inertia, cognitive, social = calculate_velocity_components(state, config)
    state['inertia_component'] = inertia
    state['cognitive_component'] = cognitive
    state['social_component'] = social
    states.append(state.copy())
    
    for _ in range(config.max_iterations):
        state = pso_step(state, config, fitness_function)
        
        # Calculate velocity components for THIS state (showing move to NEXT iteration)
        # This ensures vectors always point to the next move, not the previous one
        inertia, cognitive, social = calculate_velocity_components(state, config)
        
        # Deep copy arrays to preserve state
        new_state = {
            'positions': state['positions'].copy(),
            'velocities': state['velocities'].copy(),
            'pbest_positions': state['pbest_positions'].copy(),
            'pbest_fitnesses': state['pbest_fitnesses'].copy(),
            'gbest_position': state['gbest_position'].copy(),
            'gbest_fitness': state['gbest_fitness'],
            'iteration': state['iteration'],
            'inertia_component': inertia.copy(),
            'cognitive_component': cognitive.copy(),
            'social_component': social.copy()
        }
        
        states.append(new_state)
    
    return states


def initialize_pso_history(config, fitness_function=sphere_function):
    """
    Pre-compute complete PSO run and store all states
    
    Args:
        config: PSOConfig object with algorithm parameters
        fitness_function: Function to evaluate particle fitness
        
    Returns:
        Dictionary with all states and current index
    """
    all_states = run_complete_pso(config, fitness_function)
    return {
        'all_states': all_states,
        'current_index': 0
    }

from dash import html, dcc, Input, Output, State, callback
import plotly.graph_objects as go
import numpy as np
import dash_latex as dl
from pso_algorithm import (
    PSOConfig,
    rastrigin_function,
    initialize_pso_history
)

# PSO Configuration
pso_config = PSOConfig(
    n_particles=50,
    w=0.7,
    c1=1.5,
    c2=1.5,
    max_iterations=100,
    bounds=(-5, 5),
    v_max=1.0
)

# Content in multiple languages
CONTENT = {
    'en': {
        'title': 'Particle Swarm Optimization',
        'what_heading': 'What is PSO?',
        'bullet1_part1': '',
        'bullet1_strong': 'Swarm-based optimization algorithm',
        'bullet1_part2': ' inspired by the social behavior of birds flocking.',
        'bullet2_part1': '',
        'bullet2_strong': 'Particles',
        'bullet2_part2': ' move through the search space, influenced by their ',
        'bullet2_strong2': 'own experience',
        'bullet2_part3': ' and the swarm\'s ',
        'bullet2_strong3': 'collective knowledge.',
        'bullet3_part1': 'Intended to solve ',
        'bullet3_strong': 'global optimization',
        'bullet3_part2': ' problems.',
        'how_heading': 'How does it work?',
        'velocity_heading': 'Velocity Update:',
        'position_heading': 'Position Update:',
        'parameters_heading': 'Parameters:',
        'param_w': ' = inertia weight (controls exploration vs exploitation)',
        'param_c1': ' = cognitive parameter (personal best influence)',
        'param_c2': ' = social parameter (global best influence)',
        'param_r': ' = random values ∈ [0,1]',
        'population_label': 'Population Size:',
        'selector_label': 'Select Particle to visualize detailed information:',
        'selector_placeholder': 'None (show all)',
        'info_cognitive': 'Cognitive Component: ',
        'info_cognitive_text': 'Area of all possible cognitive components in the next velocity vector.',
        'info_social': 'Social Component: ',
        'info_social_text': 'Area of all possible social components in the next velocity vector.',
        'info_inertia': 'Inertia Component: ',
        'info_inertia_text': 'Inertia component in the next velocity vector.'
    },
    'pt-br': {
        'title': 'Particle Swarm Optimization',
        'what_heading': 'O que é PSO?',
        'bullet1_part1': '',
        'bullet1_strong': 'Algoritmo de otimização baseado em enxame',
        'bullet1_part2': ' inspirado no comportamento social de bandos de pássaros.',
        'bullet2_part1': '',
        'bullet2_strong': 'Partículas',
        'bullet2_part2': ' se movem pelo espaço de busca, influenciadas por sua ',
        'bullet2_strong2': 'própria experiência',
        'bullet2_part3': ' e pelo ',
        'bullet2_strong3': 'conhecimento coletivo',
        'bullet3_part1': 'Desenvolvido para resolver problemas de ',
        'bullet3_strong': 'otimização global',
        'bullet3_part2': '.',
        'how_heading': 'Como funciona?',
        'velocity_heading': 'Atualização da Velocidade:',
        'position_heading': 'Atualização da Posição:',
        'parameters_heading': 'Parâmetros:',
        'param_w': ' = peso de inércia (controla exploração vs explotação)',
        'param_c1': ' = parâmetro cognitivo (influência do melhor pessoal)',
        'param_c2': ' = parâmetro social (influência do melhor global)',
        'param_r': ' = valores aleatórios ∈ [0,1]',
        'population_label': 'Tamanho da População:',
        'selector_label': 'Selecionar Partícula para visualizar informações detalhadas:',
        'selector_placeholder': 'Nenhuma (mostrar todas)',
        'info_cognitive': 'Componente Cognitivo: ',
        'info_cognitive_text': 'Área de todos os componentes cognitivos possíveis no próximo vetor de velocidade.',
        'info_social': 'Componente Social: ',
        'info_social_text': 'Área de todos os componentes sociais possíveis no próximo vetor de velocidade.',
        'info_inertia': 'Componente de Inércia: ',
        'info_inertia_text': 'Componente de inércia no próximo vetor de velocidade.'
    }
}


# Create visualization
def create_pso_plot(state, selected_particle=None):
    """Create 2D heatmap with particles"""
    # Generate heatmap data (Rastrigin function)
    x = np.linspace(pso_config.bounds[0], pso_config.bounds[1], 200)
    y = np.linspace(pso_config.bounds[0], pso_config.bounds[1], 200)
    X, Y = np.meshgrid(x, y)
    # Rastrigin function: f(x,y) = 20 + x² - 10*cos(2πx) + y² - 10*cos(2πy)
    Z = 20 + X**2 - 10*np.cos(2*np.pi*X) + Y**2 - 10*np.cos(2*np.pi*Y)
    
    # Extract state information
    positions = state['positions']
    pbest_positions = state['pbest_positions']
    pbest_fitnesses = state['pbest_fitnesses']
    gbest = state['gbest_position']
    gbest_fitness = state['gbest_fitness']
    
    # Calculate current fitnesses
    current_fitnesses = rastrigin_function(positions)
    
    # Create figure
    fig = go.Figure()
    
    # Add heatmap
    fig.add_trace(go.Heatmap(
        x=x,
        y=y,
        z=Z,
        colorscale=[[0, 'blue'], [1, 'black']],
        showscale=True,
        colorbar=dict(title='f(x,y)', len=0.7, y=0.4)
    ))
    
    # Add green dashed lines from particles to their personal bests
    for i in range(pso_config.n_particles):
        fig.add_trace(go.Scatter(
            x=[positions[i, 0], pbest_positions[i, 0]],
            y=[positions[i, 1], pbest_positions[i, 1]],
            mode='lines',
            line=dict(color='green', dash='dash', width=3),
            opacity=0.6,
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Add yellow dashed lines from particles to global best
    for i in range(pso_config.n_particles):
        fig.add_trace(go.Scatter(
            x=[positions[i, 0], gbest[0]],
            y=[positions[i, 1], gbest[1]],
            mode='lines',
            line=dict(color='gold', dash='dash', width=3),
            opacity=0.6,
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Add personal bests (light green)
    fig.add_trace(go.Scatter(
        x=pbest_positions[:, 0],
        y=pbest_positions[:, 1],
        mode='markers',
        marker=dict(
            size=10,
            color='lightgreen',
            symbol='circle',
            line=dict(width=2, color='green')
        ),
        name='Personal Bests'
    ))
    
    # Add particles (current positions in red)
    fig.add_trace(go.Scatter(
        x=positions[:, 0],
        y=positions[:, 1],
        mode='markers',
        marker=dict(
            size=12,
            color='red',
            symbol='circle',
            line=dict(width=2, color='darkred')
        ),
        name='Particles'
    ))
    
    # Add global best
    fig.add_trace(go.Scatter(
        x=[gbest[0]],
        y=[gbest[1]],
        mode='markers',
        marker=dict(
            size=16,
            color='gold',
            symbol='star',
            line=dict(width=2, color='orange')
        ),
        name='Global Best'
    ))
    
    # Add particle number annotations
    annotations = []
    for i in range(pso_config.n_particles):
        # Particle number (to the left)
        annotations.append(
            dict(
                x=positions[i, 0],
                y=positions[i, 1],
                text=f'{i+1}',
                showarrow=False,
                xshift=-20,
                yshift=0,
                font=dict(size=11, color='black'),
                bgcolor='rgba(255, 255, 255, 0.8)',
                borderpad=2
            )
        )
    
    # Add rectangles if a particle is selected
    shapes = []
    if selected_particle is not None and 0 <= selected_particle < pso_config.n_particles:
        particle_pos = positions[selected_particle]
        pbest_pos = pbest_positions[selected_particle]
        
        # Green rectangle (cognitive component): particle to personal best
        x0_cog, x1_cog = min(particle_pos[0], pbest_pos[0]), max(particle_pos[0], pbest_pos[0])
        y0_cog, y1_cog = min(particle_pos[1], pbest_pos[1]), max(particle_pos[1], pbest_pos[1])
        
        shapes.append(
            dict(
                type='rect',
                x0=x0_cog, y0=y0_cog, x1=x1_cog, y1=y1_cog,
                fillcolor='green',
                opacity=0.5,
                line=dict(width=0),
                layer='above'
            )
        )
        
        # Yellow rectangle (social component): particle to global best
        x0_soc, x1_soc = min(particle_pos[0], gbest[0]), max(particle_pos[0], gbest[0])
        y0_soc, y1_soc = min(particle_pos[1], gbest[1]), max(particle_pos[1], gbest[1])
        
        shapes.append(
            dict(
                type='rect',
                x0=x0_soc, y0=y0_soc, x1=x1_soc, y1=y1_soc,
                fillcolor='yellow',
                opacity=0.5,
                line=dict(width=0),
                layer='above'
            )
        )
        
        # Add invisible traces for legend entries (rectangles)
        # Green rectangle legend
        fig.add_trace(go.Scatter(
            x=[None],
            y=[None],
            mode='markers',
            marker=dict(size=15, color='green', symbol='square', opacity=0.5),
            name='Cognitive Component',
            showlegend=True
        ))
        
        # Yellow rectangle legend
        fig.add_trace(go.Scatter(
            x=[None],
            y=[None],
            mode='markers',
            marker=dict(size=15, color='yellow', symbol='square', opacity=0.5),
            name='Social Component',
            showlegend=True
        ))
        
        # Add inertia component vector (pink arrow)
        velocity = state['velocities'][selected_particle]
        inertia_velocity = pso_config.w * velocity
        
        # Draw inertia vector as an arrow from particle position (now with legend)
        fig.add_trace(go.Scatter(
            x=[particle_pos[0], particle_pos[0] + inertia_velocity[0]],
            y=[particle_pos[1], particle_pos[1] + inertia_velocity[1]],
            mode='lines+markers',
            line=dict(color='hotpink', width=4),
            marker=dict(size=[0, 12], symbol=['circle', 'arrow-bar-up'], angleref='previous', color='hotpink'),
            name='Inertia component',
            showlegend=True,
            hoverinfo='skip'
        ))
        
        # Add fitness annotations for selected particle only
        # Current particle fitness (to the right)
        annotations.append(
            dict(
                x=particle_pos[0],
                y=particle_pos[1],
                text=f'f={current_fitnesses[selected_particle]:.2f}',
                showarrow=False,
                xshift=20,
                yshift=0,
                font=dict(size=9, color='darkred'),
                bgcolor='rgba(255, 255, 255, 0.8)',
                borderpad=2
            )
        )
        
        # Personal best fitness (above marker)
        annotations.append(
            dict(
                x=pbest_pos[0],
                y=pbest_pos[1],
                text=f'pb={pbest_fitnesses[selected_particle]:.2f}',
                showarrow=False,
                xshift=0,
                yshift=15,
                font=dict(size=9, color='darkgreen'),
                bgcolor='rgba(255, 255, 255, 0.8)',
                borderpad=2
            )
        )
    
    fig.update_layout(
        title=f"PSO Iteration {state['iteration']} | Best Fitness: {state['gbest_fitness']:.4f}",
        xaxis_title='x',
        yaxis_title='y',
        height=600,
        showlegend=True,
        annotations=annotations,
        shapes=shapes,
        xaxis=dict(range=[pso_config.bounds[0], pso_config.bounds[1]]),
        yaxis=dict(range=[pso_config.bounds[0], pso_config.bounds[1]], scaleanchor="x", scaleratio=1)
    )
    
    return fig


# Slide 2 layout
def layout(language='en'):
    # Get content for selected language
    content = CONTENT.get(language, CONTENT['en'])
    
    return html.Div([
        # Stores for PSO state
        dcc.Store(id='pso-state', data=initialize_pso_history(pso_config, rastrigin_function)),
        dcc.Store(id='selected-particle-idx', data=None),
        dcc.Interval(id='pso-interval', interval=500, disabled=True, n_intervals=0),
        
        # Slide title
        html.H2(
            content['title'],
            style={
                'textAlign': 'center',
                'color': '#34495e',
                'marginBottom': '30px'
            }
        ),
        
        # Two-column layout
        html.Div([
            # Left column: Content
            html.Div([
                html.H4(content['what_heading'], style={'color': '#2c3e50'}),

                html.Ul([
                    html.Li([content['bullet1_part1'],
                             html.Strong(content['bullet1_strong']),
                             content['bullet1_part2']]),
                    html.Li([content['bullet2_part1'],
                             html.Strong(content['bullet2_strong']),
                             content['bullet2_part2'], 
                             html.Strong(content['bullet2_strong2']), 
                             content['bullet2_part3'],
                             html.Strong(content['bullet2_strong3'])]),
                    html.Li([content['bullet3_part1'], 
                             html.Strong(content['bullet3_strong']), 
                             content['bullet3_part2']])
                ], style={'fontSize': '18px', 'lineHeight': '1.6'}),
                
                html.H4(content['how_heading'], style={'color': '#2c3e50'}),
                
                html.H5(content['velocity_heading'], style={'color': '#34495e', 'marginTop': '20px'}),
                
                html.Div([
                    dl.DashLatex(
                        r"$$\mathbf{v}_i(t+1) = w\mathbf{v}_i(t) + c_1 r_1 (\mathbf{p}_{best,i} - \mathbf{x}_i(t)) + c_2 r_2 (\mathbf{g}_{best} - \mathbf{x}_i(t))$$",
                        displayMode=True
                    ),
                ], style={'margin': '15px 0', "font_size": "18px"}),
                
                html.H5(content['position_heading'], style={'color': '#34495e', 'marginTop': '20px'}),
                
                html.Div([
                    dl.DashLatex(
                        r"$$\mathbf{x}_i(t+1) = \mathbf{x}_i(t) + \mathbf{v}_i(t+1)$$",
                        displayMode=True
                    ),
                ], style={'margin': '15px 0', "font_size": "18px"}),
                
                html.H5(content['parameters_heading'], style={'color': '#34495e', 'marginTop': '20px'}),
                
                html.Ul([
                    html.Li([dl.DashLatex(r"$w$"), content['param_w']]),
                    html.Li([dl.DashLatex(r"$c_1$"), content['param_c1']]),
                    html.Li([dl.DashLatex(r"$c_2$"), content['param_c2']]),
                    html.Li([dl.DashLatex(r"$r_1, r_2$"), content['param_r']]),
                ], style={'fontSize': '18px', 'lineHeight': '1.6'})
                
            ], style={
                'width': '48%',
                'display': 'inline-block',
                'verticalAlign': 'top',
                'padding': '20px',
                'boxSizing': 'border-box'
            }),
            
            # Right column: Visualization and controls
            html.Div([
                
                # Particle selector dropdown
                html.Div([
                    html.Label(content['selector_label'], 
                               style={'fontSize': '14px', 'marginRight': '10px'}),
                    dcc.Dropdown(
                        id='particle-selector',
                        options=[{'label': f'Particle {i+1}', 'value': i} for i in range(pso_config.n_particles)],
                        placeholder=content['selector_placeholder'],
                        clearable=True,
                        style={'width': '200px', 'display': 'inline-block'}
                    )
                ], style={'textAlign': 'center', 'marginBottom': '10px'}),
                
                dcc.Graph(
                    id='pso-plot',
                    figure=go.Figure(),  # Empty figure initially
                    style={'height': '600px'}
                ),
                
                # Information box (shown when particle is selected)
                html.Div(
                    id='component-info',
                    style={'marginTop': '10px', 'padding': '15px', 'backgroundColor': '#f8f9fa', 'borderRadius': '5px', 'display': 'none'}
                ),
                
                # Control buttons
                html.Div([
                    html.Button(
                        '← Step Back',
                        id='pso-step-back-button',
                        n_clicks=0,
                        style={
                            'padding': '10px 20px',
                            'fontSize': '14px',
                            'marginRight': '10px',
                            'backgroundColor': '#95a5a6',
                            'color': 'white',
                            'border': 'none',
                            'borderRadius': '5px',
                            'cursor': 'pointer'
                        }
                    ),
                    html.Button(
                        'Step Forward →',
                        id='pso-step-forward-button',
                        n_clicks=0,
                        style={
                            'padding': '10px 20px',
                            'fontSize': '14px',
                            'marginRight': '10px',
                            'backgroundColor': '#3498db',
                            'color': 'white',
                            'border': 'none',
                            'borderRadius': '5px',
                            'cursor': 'pointer'
                        }
                    ),
                    html.Button(
                        'Run All',
                        id='pso-run-button',
                        n_clicks=0,
                        style={
                            'padding': '10px 20px',
                            'fontSize': '14px',
                            'marginRight': '10px',
                            'backgroundColor': '#2ecc71',
                            'color': 'white',
                            'border': 'none',
                            'borderRadius': '5px',
                            'cursor': 'pointer'
                        }
                    ),
                    html.Button(
                        'Reset',
                        id='pso-reset-button',
                        n_clicks=0,
                        style={
                            'padding': '10px 20px',
                            'fontSize': '14px',
                            'backgroundColor': '#e74c3c',
                            'color': 'white',
                            'border': 'none',
                            'borderRadius': '5px',
                            'cursor': 'pointer'
                        }
                    )
                ], style={'textAlign': 'center', 'marginTop': '15px'}),
                
            ], style={
                'width': '48%',
                'display': 'inline-block',
                'verticalAlign': 'top',
                'padding': '20px',
                'boxSizing': 'border-box'
            })
        ], style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'width': '100%'
        })
    ])


# Callback for particle selection
@callback(
    Output('selected-particle-idx', 'data'),
    Input('particle-selector', 'value')
)
def update_selected_particle(value):
    return value


# Callback to update component info box
@callback(
    Output('component-info', 'children'),
    Output('component-info', 'style'),
    Input('selected-particle-idx', 'data')
)
def update_component_info(selected_particle):
    # Note: This uses English content - would need app-level language state to translate
    # For now keeping English as these are technical descriptions
    if selected_particle is None:
        # Hide the info box when no particle is selected
        return None, {'display': 'none'}
    
    # Show the info box with component descriptions
    info_content = html.Div([
        html.Div([
            html.Span("• ", style={'color': 'green', 'fontWeight': 'bold', 'fontSize': '18px'}),
            html.Strong("Cognitive Component: ", style={'color': '#2c3e50'}),
            html.Span("Area of all possible cognitive components in the next velocity vector.", 
                     style={'color': '#555'})
        ], style={'marginBottom': '8px'}),
        
        html.Div([
            html.Span("• ", style={'color': 'gold', 'fontWeight': 'bold', 'fontSize': '18px'}),
            html.Strong("Social Component: ", style={'color': '#2c3e50'}),
            html.Span("Area of all possible social components in the next velocity vector.", 
                     style={'color': '#555'})
        ], style={'marginBottom': '8px'}),
        
        html.Div([
            html.Span("• ", style={'color': 'hotpink', 'fontWeight': 'bold', 'fontSize': '18px'}),
            html.Strong("Inertia Component: ", style={'color': '#2c3e50'}),
            html.Span("Inertia component in the next velocity vector.", 
                     style={'color': '#555'})
        ])
    ])
    
    style = {
        'marginTop': '10px',
        'padding': '15px',
        'backgroundColor': '#f8f9fa',
        'borderRadius': '5px',
        'border': '1px solid #dee2e6',
        'fontSize': '14px',
        'lineHeight': '1.6',
        'display': 'block'
    }
    
    return info_content, style


# Callbacks for PSO controls
@callback(
    [Output('pso-state', 'data'),
     Output('pso-plot', 'figure', allow_duplicate=True),
     Output('pso-interval', 'disabled'),
     Output('pso-step-back-button', 'disabled'),
     Output('pso-step-forward-button', 'disabled')],
    [Input('pso-step-back-button', 'n_clicks'),
     Input('pso-step-forward-button', 'n_clicks'),
     Input('pso-run-button', 'n_clicks'),
     Input('pso-reset-button', 'n_clicks'),
     Input('pso-interval', 'n_intervals'),
     Input('selected-particle-idx', 'data')],
    [State('pso-state', 'data'),
     State('pso-interval', 'disabled')],
    prevent_initial_call=True
)
def update_pso(back_clicks, forward_clicks, run_clicks, reset_clicks, n_intervals, selected_particle, history_state, interval_disabled):
    from dash import callback_context
    
    # Convert history state back to proper format
    if history_state is not None and 'all_states' in history_state:
        all_states = history_state['all_states']
        current_index = history_state['current_index']
        
        # Convert numpy arrays in current state
        for i, state in enumerate(all_states):
            converted_state = {
                'positions': np.array(state['positions']),
                'velocities': np.array(state['velocities']),
                'pbest_positions': np.array(state['pbest_positions']),
                'pbest_fitnesses': np.array(state['pbest_fitnesses']),
                'gbest_position': np.array(state['gbest_position']),
                'gbest_fitness': state['gbest_fitness'],
                'iteration': state['iteration']
            }
            # Add velocity components if available
            if 'inertia_component' in state:
                converted_state['inertia_component'] = np.array(state['inertia_component'])
                converted_state['cognitive_component'] = np.array(state['cognitive_component'])
                converted_state['social_component'] = np.array(state['social_component'])
            all_states[i] = converted_state
    else:
        # Initialize if needed
        history_state = initialize_pso_history(pso_config, rastrigin_function)
        all_states = history_state['all_states']
        current_index = history_state['current_index']
    
    ctx = callback_context
    if not ctx.triggered:
        current_state = all_states[current_index]
        back_disabled = current_index == 0
        forward_disabled = current_index >= len(all_states) - 1
        return history_state, create_pso_plot(current_state, selected_particle), True, back_disabled, forward_disabled
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Particle selection changed - just update the plot
    if button_id == 'selected-particle-idx':
        current_state = all_states[current_index]
        back_disabled = current_index == 0
        forward_disabled = current_index >= len(all_states) - 1
        return history_state, create_pso_plot(current_state, selected_particle), True, back_disabled, forward_disabled
    
    # Reset button - generate new PSO run
    if button_id == 'pso-reset-button':
        new_history = initialize_pso_history(pso_config, rastrigin_function)
        current_state = new_history['all_states'][0]
        return new_history, create_pso_plot(current_state, selected_particle), True, True, False
    
    # Step back button
    elif button_id == 'pso-step-back-button':
        if current_index > 0:
            current_index -= 1
        history_state['current_index'] = current_index
        current_state = all_states[current_index]
        back_disabled = current_index == 0
        forward_disabled = current_index >= len(all_states) - 1
        return history_state, create_pso_plot(current_state, selected_particle), True, back_disabled, forward_disabled
    
    # Step forward button
    elif button_id == 'pso-step-forward-button':
        if current_index < len(all_states) - 1:
            current_index += 1
        history_state['current_index'] = current_index
        current_state = all_states[current_index]
        back_disabled = current_index == 0
        forward_disabled = current_index >= len(all_states) - 1
        return history_state, create_pso_plot(current_state, selected_particle), True, back_disabled, forward_disabled
    
    # Run button - enable interval
    elif button_id == 'pso-run-button':
        if current_index >= len(all_states) - 1:
            # Already at end
            return history_state, create_pso_plot(all_states[current_index], selected_particle), True, False, True
        # Enable interval to auto-play
        current_state = all_states[current_index]
        back_disabled = current_index == 0
        forward_disabled = current_index >= len(all_states) - 1
        return history_state, create_pso_plot(current_state, selected_particle), False, back_disabled, forward_disabled
    
    # Interval tick - auto-play mode
    elif button_id == 'pso-interval':
        if current_index < len(all_states) - 1:
            current_index += 1
            history_state['current_index'] = current_index
        
        current_state = all_states[current_index]
        
        # Stop interval if we reached the end
        stop_interval = current_index >= len(all_states) - 1
        back_disabled = current_index == 0
        forward_disabled = current_index >= len(all_states) - 1
        
        return history_state, create_pso_plot(current_state, selected_particle), stop_interval, back_disabled, forward_disabled
    
    # Default return
    current_state = all_states[current_index]
    back_disabled = current_index == 0
    forward_disabled = current_index >= len(all_states) - 1
    return history_state, create_pso_plot(current_state, selected_particle), True, back_disabled, forward_disabled

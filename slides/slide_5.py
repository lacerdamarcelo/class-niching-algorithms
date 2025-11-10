from dash import html, dcc, Input, Output, State, callback
import plotly.graph_objects as go
import numpy as np
import dash_latex as dl
from niching_pso_algorithm import (
    NichingPSOConfig,
    rastrigin_function,
    initialize_niching_pso_history
)

# Niching PSO Configuration
niching_pso_config = NichingPSOConfig(
    n_particles=50,
    w=0.7,
    c1=1.5,
    c2=1.5,
    max_iterations=100,
    bounds=(-3, 3),
    v_max=1.0,
    n_neighbors=3,
    radius=1.5
)

# Content in multiple languages
CONTENT = {
    'en': {
        'title': "Let's modify PSO!",
        'what_heading': 'What should we change in PSO for niching optimization?',
        'bullet1_part1': 'Neighborhood must be ',
        'bullet1_strong': 'dynamic',
        'bullet1_part2': ' to maintain multiple optima.',
        'bullet2_part1': 'Instead of a ',
        'bullet2_strong1': 'global best',
        'bullet2_part2': ', each particle must have a ',
        'bullet2_strong2': 'social best',
        'bullet2_part3': ' from its connected neighbors.',
        'bullet3_part1': 'Connections updated every iteration: up to ',
        'bullet3_strong1': f'n={niching_pso_config.n_neighbors} closest',
        'bullet3_part2': ' particles within ',
        'bullet3_strong2': f'radius r={niching_pso_config.radius}',
        'bullet3_part3': '.',
        'how_heading': 'How would it work?',
        'velocity_heading': 'Velocity Update (same as PSO):',
        'key_diff_heading': 'Key Difference:',
        'key_diff_text': ' = social best (best among connected particles) replaces ',
        'key_diff_text2': ' (global best) from vanilla PSO',
        'result_heading': 'Result:',
        'result1_part1': 'Particles form ',
        'result1_strong': 'niches',
        'result1_part2': ' around different local optima',
        'result2_part1': 'Maintains ',
        'result2_strong': 'diversity',
        'result2_part2': ' in the population',
        'result3_part1': 'Explores ',
        'result3_strong': 'multiple solutions',
        'result3_part2': ' simultaneously',
        'selector_label': 'Select Particle to visualize detailed information:',
        'selector_placeholder': 'None (show all)',
        'info_cognitive': 'Cognitive Component: ',
        'info_cognitive_text': 'Area of all possible cognitive components in the next velocity vector.',
        'info_social': 'Social Component: ',
        'info_social_text': 'Area of all possible social components (toward social best, not global best).',
        'info_inertia': 'Inertia Component: ',
        'info_inertia_text': 'Inertia component in the next velocity vector.',
        'info_connections': 'Connections: ',
        'info_connections_text': 'Dotted lines show which particles are connected (within radius).'
    },
    'pt-br': {
        'title': 'Vamos modificar o PSO!',
        'what_heading': 'O que devemos mudar no PSO para Otimização por Nichos?',
        'bullet1_part1': 'Vizinhança deve ser ',
        'bullet1_strong': 'dinâmica',
        'bullet1_part2': ' para manter múltiplos ótimos.',
        'bullet2_part1': 'Em vez de um ',
        'bullet2_strong1': 'melhor global',
        'bullet2_part2': ', cada partícula deve ter um ',
        'bullet2_strong2': 'melhor social',
        'bullet2_part3': ' de seus vizinhos conectados.',
        'bullet3_part1': 'Conexões atualizadas a cada iteração: até ',
        'bullet3_strong1': f'n={niching_pso_config.n_neighbors} mais próximas',
        'bullet3_part2': ' partículas dentro de ',
        'bullet3_strong2': f'raio r={niching_pso_config.radius}',
        'bullet3_part3': '.',
        'how_heading': 'Como funcionaria?',
        'velocity_heading': 'Atualização de Velocidade (igual ao PSO):',
        'key_diff_heading': 'Diferença Principal:',
        'key_diff_text': ' = melhor social (melhor entre partículas conectadas) substitui ',
        'key_diff_text2': ' (melhor global) do PSO tradicional',
        'result_heading': 'Resultado:',
        'result1_part1': 'Partículas formam ',
        'result1_strong': 'nichos',
        'result1_part2': ' ao redor de diferentes ótimos locais',
        'result2_part1': 'Mantém ',
        'result2_strong': 'diversidade',
        'result2_part2': ' na população',
        'result3_part1': 'Explora ',
        'result3_strong': 'múltiplas soluções',
        'result3_part2': ' simultaneamente',
        'selector_label': 'Selecionar Partícula para visualizar informações detalhadas:',
        'selector_placeholder': 'Nenhuma (mostrar todas)',
        'info_cognitive': 'Componente Cognitivo: ',
        'info_cognitive_text': 'Área de todos os componentes cognitivos possíveis no próximo vetor de velocidade.',
        'info_social': 'Componente Social: ',
        'info_social_text': 'Área de todos os componentes sociais possíveis (em direção ao melhor social, não global).',
        'info_inertia': 'Componente de Inércia: ',
        'info_inertia_text': 'Componente de inércia no próximo vetor de velocidade.',
        'info_connections': 'Conexões: ',
        'info_connections_text': 'Linhas pontilhadas mostram quais partículas estão conectadas (dentro do raio).'
    }
}


# Create visualization
def create_niching_pso_plot(state, selected_particle=None):
    """Create 2D heatmap with particles for Niching PSO"""
    # Generate heatmap data (Rastrigin function)
    x = np.linspace(niching_pso_config.bounds[0], niching_pso_config.bounds[1], 200)
    y = np.linspace(niching_pso_config.bounds[0], niching_pso_config.bounds[1], 200)
    X, Y = np.meshgrid(x, y)
    # Rastrigin function: f(x,y) = 20 + x² - 10*cos(2πx) + y² - 10*cos(2πy)
    Z = 20 + X**2 - 10*np.cos(2*np.pi*X) + Y**2 - 10*np.cos(2*np.pi*Y)
    
    # Extract state information
    positions = state['positions']
    pbest_positions = state['pbest_positions']
    pbest_fitnesses = state['pbest_fitnesses']
    sbest_positions = state['sbest_positions']
    sbest_fitnesses = state['sbest_fitnesses']
    connections = state['connections']
    
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
    for i in range(niching_pso_config.n_particles):
        fig.add_trace(go.Scatter(
            x=[positions[i, 0], pbest_positions[i, 0]],
            y=[positions[i, 1], pbest_positions[i, 1]],
            mode='lines',
            line=dict(color='green', dash='dash', width=3),
            opacity=0.6,
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Add cyan dashed lines from particles to their social bests
    for i in range(niching_pso_config.n_particles):
        fig.add_trace(go.Scatter(
            x=[positions[i, 0], sbest_positions[i, 0]],
            y=[positions[i, 1], sbest_positions[i, 1]],
            mode='lines',
            line=dict(color='cyan', dash='dash', width=3),
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
    
    # Add social bests (purple/magenta)
    fig.add_trace(go.Scatter(
        x=sbest_positions[:, 0],
        y=sbest_positions[:, 1],
        mode='markers',
        marker=dict(
            size=12,
            color='magenta',
            symbol='star',
            line=dict(width=2, color='purple')
        ),
        name='Social Bests'
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
    
    # Add particle number annotations
    annotations = []
    for i in range(niching_pso_config.n_particles):
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
    
    # Add rectangles and connections if a particle is selected
    shapes = []
    if selected_particle is not None and 0 <= selected_particle < niching_pso_config.n_particles:
        particle_pos = positions[selected_particle]
        pbest_pos = pbest_positions[selected_particle]
        sbest_pos = sbest_positions[selected_particle]
        
        # Show connections to connected particles (dotted lines)
        connected_indices = connections[selected_particle]
        for conn_idx in connected_indices:
            fig.add_trace(go.Scatter(
                x=[particle_pos[0], positions[conn_idx, 0]],
                y=[particle_pos[1], positions[conn_idx, 1]],
                mode='lines',
                line=dict(color='lightblue', dash='dot', width=2),
                opacity=0.7,
                showlegend=False,
                hoverinfo='skip'
            ))
        
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
        
        # Cyan rectangle (social component): particle to social best
        x0_soc, x1_soc = min(particle_pos[0], sbest_pos[0]), max(particle_pos[0], sbest_pos[0])
        y0_soc, y1_soc = min(particle_pos[1], sbest_pos[1]), max(particle_pos[1], sbest_pos[1])
        
        shapes.append(
            dict(
                type='rect',
                x0=x0_soc, y0=y0_soc, x1=x1_soc, y1=y1_soc,
                fillcolor='cyan',
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
        
        # Cyan rectangle legend
        fig.add_trace(go.Scatter(
            x=[None],
            y=[None],
            mode='markers',
            marker=dict(size=15, color='cyan', symbol='square', opacity=0.5),
            name='Social Component',
            showlegend=True
        ))
        
        # Connection lines legend
        fig.add_trace(go.Scatter(
            x=[None],
            y=[None],
            mode='lines',
            line=dict(color='lightblue', dash='dot', width=2),
            name='Connections',
            showlegend=True
        ))
        
        # Add inertia component vector (pink arrow)
        velocity = state['velocities'][selected_particle]
        inertia_velocity = niching_pso_config.w * velocity
        
        # Draw inertia vector as an arrow from particle position
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
        
        # Add fitness annotations for selected particle
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
        
        # Social best fitness (below marker)
        annotations.append(
            dict(
                x=sbest_pos[0],
                y=sbest_pos[1],
                text=f'sb={sbest_fitnesses[selected_particle]:.2f}',
                showarrow=False,
                xshift=0,
                yshift=-15,
                font=dict(size=9, color='purple'),
                bgcolor='rgba(255, 255, 255, 0.8)',
                borderpad=2
            )
        )
    
    fig.update_layout(
        title=f"Niching PSO Iteration {state['iteration']}",
        xaxis_title='x',
        yaxis_title='y',
        height=600,
        showlegend=True,
        annotations=annotations,
        shapes=shapes,
        xaxis=dict(range=[niching_pso_config.bounds[0], niching_pso_config.bounds[1]]),
        yaxis=dict(range=[niching_pso_config.bounds[0], niching_pso_config.bounds[1]], scaleanchor="x", scaleratio=1)
    )
    
    return fig


# Slide 5 layout
def layout(language='en'):
    # Get content for selected language
    content = CONTENT.get(language, CONTENT['en'])
    
    return html.Div([
        # Stores for Niching PSO state
        dcc.Store(id='niching-pso-state', data=initialize_niching_pso_history(niching_pso_config, rastrigin_function)),
        dcc.Store(id='selected-particle-idx-niching', data=None),
        dcc.Interval(id='niching-pso-interval', interval=500, disabled=True, n_intervals=0),
        
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
                             html.Strong(content['bullet2_strong1']), 
                             content['bullet2_part2'],
                             html.Strong(content['bullet2_strong2']),
                             content['bullet2_part3']]),
                    html.Li([content['bullet3_part1'], 
                             html.Strong(content['bullet3_strong1']), 
                             content['bullet3_part2'],
                             html.Strong(content['bullet3_strong2']), 
                             content['bullet3_part3']]),
                ], style={'fontSize': '18px', 'lineHeight': '1.6'}),
                
                html.H4(content['how_heading'], style={'color': '#2c3e50'}),
                
                html.H5(content['velocity_heading'], style={'color': '#34495e', 'marginTop': '20px'}),
                
                html.Div([
                    dl.DashLatex(
                        r"$$\mathbf{v}_i(t+1) = w\mathbf{v}_i(t) + c_1 r_1 (\mathbf{p}_{best,i} - \mathbf{x}_i(t)) + c_2 r_2 (\mathbf{s}_{best,i} - \mathbf{x}_i(t))$$",
                        displayMode=True
                    ),
                ], style={'margin': '15px 0', "fontSize": "16px"}),
                
                html.H5(content['key_diff_heading'], style={'color': '#34495e', 'marginTop': '20px'}),
                
                html.Ul([
                    html.Li([dl.DashLatex(r"$\mathbf{s}_{best,i}$"), 
                            content['key_diff_text'],
                            dl.DashLatex(r"$\mathbf{g}_{best}$"), 
                            content['key_diff_text2']]),
                ], style={'fontSize': '18px', 'lineHeight': '1.6'}),
                
                html.H5(content['result_heading'], style={'color': '#34495e', 'marginTop': '20px'}),
                
                html.Ul([
                    html.Li([content['result1_part1'], 
                             html.Strong(content['result1_strong']), 
                             content['result1_part2']]),
                    html.Li([content['result2_part1'], 
                             html.Strong(content['result2_strong']), 
                             content['result2_part2']]),
                    html.Li([content['result3_part1'], 
                             html.Strong(content['result3_strong']), 
                             content['result3_part2']]),
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
                        id='particle-selector-niching',
                        options=[{'label': f'Particle {i+1}', 'value': i} for i in range(niching_pso_config.n_particles)],
                        placeholder=content['selector_placeholder'],
                        clearable=True,
                        style={'width': '200px', 'display': 'inline-block'}
                    )
                ], style={'textAlign': 'center', 'marginBottom': '10px'}),
                
                dcc.Graph(
                    id='niching-pso-plot',
                    figure=go.Figure(),  # Empty figure initially
                    style={'height': '600px'}
                ),
                
                # Information box (shown when particle is selected)
                html.Div(
                    id='component-info-niching',
                    style={'marginTop': '10px', 'padding': '15px', 'backgroundColor': '#f8f9fa', 'borderRadius': '5px', 'display': 'none'}
                ),
                
                # Control buttons
                html.Div([
                    html.Button(
                        '← Step Back',
                        id='niching-pso-step-back-button',
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
                        id='niching-pso-step-forward-button',
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
                        id='niching-pso-run-button',
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
                        id='niching-pso-reset-button',
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
    Output('selected-particle-idx-niching', 'data'),
    Input('particle-selector-niching', 'value')
)
def update_selected_particle(value):
    return value


# Callback to update component info box
@callback(
    Output('component-info-niching', 'children'),
    Output('component-info-niching', 'style'),
    Input('selected-particle-idx-niching', 'data')
)
def update_component_info(selected_particle):
    if selected_particle is None:
        # Hide the info box when no particle is selected
        return None, {'display': 'none'}
    
    # Show the info box with component descriptions
    content = html.Div([
        html.Div([
            html.Span("• ", style={'color': 'green', 'fontWeight': 'bold', 'fontSize': '18px'}),
            html.Strong("Cognitive Component: ", style={'color': '#2c3e50'}),
            html.Span("Area of all possible cognitive components in the next velocity vector.", 
                     style={'color': '#555'})
        ], style={'marginBottom': '8px'}),
        
        html.Div([
            html.Span("• ", style={'color': 'cyan', 'fontWeight': 'bold', 'fontSize': '18px'}),
            html.Strong("Social Component: ", style={'color': '#2c3e50'}),
            html.Span("Area of all possible social components (toward social best, not global best).", 
                     style={'color': '#555'})
        ], style={'marginBottom': '8px'}),
        
        html.Div([
            html.Span("• ", style={'color': 'hotpink', 'fontWeight': 'bold', 'fontSize': '18px'}),
            html.Strong("Inertia Component: ", style={'color': '#2c3e50'}),
            html.Span("Inertia component in the next velocity vector.", 
                     style={'color': '#555'})
        ], style={'marginBottom': '8px'}),
        
        html.Div([
            html.Span("• ", style={'color': 'lightblue', 'fontWeight': 'bold', 'fontSize': '18px'}),
            html.Strong("Connections: ", style={'color': '#2c3e50'}),
            html.Span("Dotted lines show which particles are connected (within radius).", 
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
    
    return content, style


# Callbacks for Niching PSO controls
@callback(
    [Output('niching-pso-state', 'data'),
     Output('niching-pso-plot', 'figure', allow_duplicate=True),
     Output('niching-pso-interval', 'disabled'),
     Output('niching-pso-step-back-button', 'disabled'),
     Output('niching-pso-step-forward-button', 'disabled')],
    [Input('niching-pso-step-back-button', 'n_clicks'),
     Input('niching-pso-step-forward-button', 'n_clicks'),
     Input('niching-pso-run-button', 'n_clicks'),
     Input('niching-pso-reset-button', 'n_clicks'),
     Input('niching-pso-interval', 'n_intervals'),
     Input('selected-particle-idx-niching', 'data')],
    [State('niching-pso-state', 'data'),
     State('niching-pso-interval', 'disabled')],
    prevent_initial_call=True
)
def update_niching_pso(back_clicks, forward_clicks, run_clicks, reset_clicks, n_intervals, selected_particle, history_state, interval_disabled):
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
                'sbest_positions': np.array(state['sbest_positions']),
                'sbest_fitnesses': np.array(state['sbest_fitnesses']),
                'connections': state['connections'],
                'iteration': state['iteration']
            }
            all_states[i] = converted_state
    else:
        # Initialize if needed
        history_state = initialize_niching_pso_history(niching_pso_config, rastrigin_function)
        all_states = history_state['all_states']
        current_index = history_state['current_index']
    
    ctx = callback_context
    if not ctx.triggered:
        current_state = all_states[current_index]
        back_disabled = current_index == 0
        forward_disabled = current_index >= len(all_states) - 1
        return history_state, create_niching_pso_plot(current_state, selected_particle), True, back_disabled, forward_disabled
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Particle selection changed - just update the plot
    if button_id == 'selected-particle-idx-niching':
        current_state = all_states[current_index]
        back_disabled = current_index == 0
        forward_disabled = current_index >= len(all_states) - 1
        return history_state, create_niching_pso_plot(current_state, selected_particle), True, back_disabled, forward_disabled
    
    # Reset button - generate new Niching PSO run
    if button_id == 'niching-pso-reset-button':
        new_history = initialize_niching_pso_history(niching_pso_config, rastrigin_function)
        current_state = new_history['all_states'][0]
        return new_history, create_niching_pso_plot(current_state, selected_particle), True, True, False
    
    # Step back button
    elif button_id == 'niching-pso-step-back-button':
        if current_index > 0:
            current_index -= 1
        history_state['current_index'] = current_index
        current_state = all_states[current_index]
        back_disabled = current_index == 0
        forward_disabled = current_index >= len(all_states) - 1
        return history_state, create_niching_pso_plot(current_state, selected_particle), True, back_disabled, forward_disabled
    
    # Step forward button
    elif button_id == 'niching-pso-step-forward-button':
        if current_index < len(all_states) - 1:
            current_index += 1
        history_state['current_index'] = current_index
        current_state = all_states[current_index]
        back_disabled = current_index == 0
        forward_disabled = current_index >= len(all_states) - 1
        return history_state, create_niching_pso_plot(current_state, selected_particle), True, back_disabled, forward_disabled
    
    # Run button - enable interval
    elif button_id == 'niching-pso-run-button':
        if current_index >= len(all_states) - 1:
            # Already at end
            return history_state, create_niching_pso_plot(all_states[current_index], selected_particle), True, False, True
        # Enable interval to auto-play
        current_state = all_states[current_index]
        back_disabled = current_index == 0
        forward_disabled = current_index >= len(all_states) - 1
        return history_state, create_niching_pso_plot(current_state, selected_particle), False, back_disabled, forward_disabled
    
    # Interval tick - auto-play mode
    elif button_id == 'niching-pso-interval':
        if current_index < len(all_states) - 1:
            current_index += 1
            history_state['current_index'] = current_index
        
        current_state = all_states[current_index]
        
        # Stop interval if we reached the end
        stop_interval = current_index >= len(all_states) - 1
        back_disabled = current_index == 0
        forward_disabled = current_index >= len(all_states) - 1
        
        return history_state, create_niching_pso_plot(current_state, selected_particle), stop_interval, back_disabled, forward_disabled
    
    # Default return
    current_state = all_states[current_index]
    back_disabled = current_index == 0
    forward_disabled = current_index >= len(all_states) - 1
    return history_state, create_niching_pso_plot(current_state, selected_particle), True, back_disabled, forward_disabled

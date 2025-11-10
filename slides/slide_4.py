from dash import html, dcc
import plotly.graph_objects as go
import numpy as np
import dash_latex as dl

# Content in multiple languages
CONTENT = {
    'en': {
        'title': 'Niching Optimization',
        'what_heading': 'What is Niching Optimization?',
        'bullet1_part1': 'Niching optimization finds ',
        'bullet1_strong': 'multiple diverse high-quality solutions',
        'bullet1_part2': ' in a single run.',
        'bullet2_part1': 'Useful when we need ',
        'bullet2_strong': 'alternative solutions',
        'bullet2_part2': ' or want to explore different regions.',
        'bullet3': 'Applications: multi-modal problems, design alternatives, diverse portfolios.',
        'prelim_heading': 'Preliminary Definitions:',
        'global_heading': 'Global Optimum:',
        'global_text_part1': 'A point ',
        'global_text_part2': ' is a global optimum if it has the best objective value across the entire search space ',
        'global_text_part3': '.',
        'local_heading': 'Local Optimum:',
        'local_text_part1': 'A point ',
        'local_text_part2': ' is a local optimum if it has the best objective value within a neighborhood of radius ',
        'local_text_part3': ' around it.',
        'math_heading': 'Mathematical Definition for Niching Optimization:',
        'math_text_part1': 'where ',
        'math_text_part2': ' represents the local optima, ',
        'math_text_part3': ' is the search space, and ',
        'math_text_part4': ' is the objective function.',
        'latex_global_def': r"$$x^* \text{ is a global minimum if:}$$",
        'latex_local_def': r"$$x^* \text{ is a local minimum if } \exists \delta > 0 \text{ such that:}$$",
        'latex_niching_def': r"$$\text{Find all } x^* \in S \text{ such that } x^* \text{ is a local optimum}$$"
    },
    'pt-br': {
        'title': 'Otimização por Nichos',
        'what_heading': 'O que é Otimização por Nichos?',
        'bullet1_part1': 'Otimização por Nichos encontra ',
        'bullet1_strong': 'múltiplas soluções diversas de alta qualidade',
        'bullet1_part2': ' em uma única execução.',
        'bullet2_part1': 'Útil quando precisamos de ',
        'bullet2_strong': 'soluções alternativas',
        'bullet2_part2': ' ou queremos explorar diferentes regiões.',
        'bullet3': 'Aplicações: problemas multi-modais, alternativas de design, portfólios diversos.',
        'prelim_heading': 'Definições Preliminares:',
        'global_heading': 'Ótimo Global:',
        'global_text_part1': 'Um ponto ',
        'global_text_part2': ' é um ótimo global se possui o melhor valor objetivo em todo o espaço de busca ',
        'global_text_part3': '.',
        'local_heading': 'Ótimo Local:',
        'local_text_part1': 'Um ponto ',
        'local_text_part2': ' é um ótimo local se possui o melhor valor objetivo dentro de uma vizinhança de raio ',
        'local_text_part3': ' ao seu redor.',
        'math_heading': 'Definição Matemática para Otimização por Nichos:',
        'math_text_part1': 'onde ',
        'math_text_part2': ' representa os ótimos locais, ',
        'math_text_part3': ' é o espaço de busca, e ',
        'math_text_part4': ' é a função objetivo.',
        'latex_global_def': r"$$x^* \text{ é um mínimo global se:}$$",
        'latex_local_def': r"$$x^* \text{ é um mínimo local se } \exists \delta > 0 \text{ de forma que:}$$",
        'latex_niching_def': r"$$\text{Ache todos os } x^* \in S \text{ de forma que } x^* \text{ é um ótimo local}$$"
    }
}

# Generate data for the Rastrigin function
def generate_rastrigin_function(x_range=(-5, 5), y_range=(-5, 5), resolution=50):
    x = np.linspace(x_range[0], x_range[1], resolution)
    y = np.linspace(y_range[0], y_range[1], resolution)
    X, Y = np.meshgrid(x, y)
    # Rastrigin function: f(x,y) = 20 + x² - 10*cos(2πx) + y² - 10*cos(2πy)
    Z = 20 + X**2 - 10*np.cos(2*np.pi*X) + Y**2 - 10*np.cos(2*np.pi*Y)
    return X, Y, Z

# Calculate Rastrigin function value
def rastrigin(x, y):
    return 20 + x**2 - 10*np.cos(2*np.pi*x) + y**2 - 10*np.cos(2*np.pi*y)

# Create the 3D Rastrigin function plot with local optima
def create_rastrigin_plot_with_optima():
    X, Y, Z = generate_rastrigin_function()
    
    fig = go.Figure(data=[go.Surface(
        x=X, y=Y, z=Z,
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(title='f(x,y)', len=1.0, y=0.4)
    )])
    
    # Define local optima positions (integer coordinates within [-5, 5])
    local_optima = []
    for i in range(-4, 5):
        for j in range(-4, 5):
            if i != 0 or j != 0:  # Exclude global optimum
                local_optima.append((i, j, rastrigin(i, j)))
    
    # Add markers for local optima (yellow/orange)
    if local_optima:
        x_coords = [opt[0] for opt in local_optima]
        y_coords = [opt[1] for opt in local_optima]
        z_coords = [opt[2] for opt in local_optima]
        
        fig.add_trace(go.Scatter3d(
            x=x_coords,
            y=y_coords,
            z=z_coords,
            mode='markers',
            marker=dict(
                size=8,
                color='orange',
                symbol='circle',
                line=dict(color='darkorange', width=2)
            ),
            name='Local Optima',
            showlegend=True
        ))
    
    # Add marker at global optimum (0, 0, 0) - larger and red
    fig.add_trace(go.Scatter3d(
        x=[0],
        y=[0],
        z=[0],
        mode='markers',
        marker=dict(
            size=15,
            color='red',
            symbol='circle',
            line=dict(color='darkred', width=2)
        ),
        name='Global Optimum',
        showlegend=True
    ))
    
    fig.update_layout(
        title='Rastrigin Function with Multiple Local Optima',
        scene=dict(
            xaxis_title='x',
            yaxis_title='y',
            zaxis_title='f(x,y)',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.3)
            )
        ),
        autosize=True,
        height=600,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    return fig

# Slide 4 layout
def layout(language='en'):
    # Get content for selected language
    content = CONTENT.get(language, CONTENT['en'])
    
    return html.Div([
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
                             content['bullet2_part2']]),
                    html.Li([content['bullet3']]),
                ], style={'fontSize': '18px', 'lineHeight': '1.6'}),
                
                html.H4(content['prelim_heading'], style={'color': '#34495e', 'marginTop': '20px'}),
                
                # Global Optimum Definition
                html.H5(content['global_heading'], style={'color': '#2c3e50', 'marginTop': '15px', 'fontSize': '18px', 'fontWeight': 'bold'}),
                
                html.Div([
                    dl.DashLatex(
                        content['latex_global_def'],
                        displayMode=True
                    ),
                    dl.DashLatex(
                        r"$$f(x^*) \leq f(x), \quad \forall x \in S$$",
                        displayMode=True
                    ),
                ], style={'margin': '10px 0', 'fontSize': '18px'}),
                
                html.P([
                    content['global_text_part1'],
                    dl.DashLatex(r"$x^*$"),
                    content['global_text_part2'],
                    dl.DashLatex(r"$S$"),
                    content['global_text_part3']
                ], style={'fontSize': '18px', 'lineHeight': '1.6', 'fontStyle': 'italic', 'marginBottom': '15px'}),
                
                # Local Optimum Definition
                html.H5(content['local_heading'], style={'color': '#2c3e50', 'marginTop': '15px', 'fontSize': '18px', 'fontWeight': 'bold'}),
                
                html.Div([
                    dl.DashLatex(
                        content['latex_local_def'],
                        displayMode=True
                    ),
                    dl.DashLatex(
                        r"$$f(x^*) \leq f(x), \quad \forall x \in S \text{ with } ||x - x^*|| < \delta$$",
                        displayMode=True
                    ),
                ], style={'margin': '10px 0', 'fontSize': '18px'}),
                
                html.P([
                    content['local_text_part1'],
                    dl.DashLatex(r"$x^*$"),
                    content['local_text_part2'],
                    dl.DashLatex(r"$\delta$"),
                    content['local_text_part3']
                ], style={'fontSize': '18px', 'lineHeight': '1.6', 'fontStyle': 'italic'}),
                
                html.H4(content['math_heading'], style={'color': '#34495e', 'marginTop': '25px'}),
                
                html.Div([
                    dl.DashLatex(
                        content['latex_niching_def'],
                        displayMode=True
                    ),
                ], style={'margin': '20px 0', 'fontSize': '18px'}),
                
                html.P([
                    content['math_text_part1'],
                    dl.DashLatex(r"$x^*$"),
                    content['math_text_part2'],
                    dl.DashLatex(r"$S$"),
                    content['math_text_part3'],
                    dl.DashLatex(r"$f(x)$"),
                    content['math_text_part4']
                ], style={'fontSize': '18px', 'lineHeight': '1.6'}),
                
            ], style={
                'width': '48%',
                'display': 'inline-block',
                'verticalAlign': 'top',
                'padding': '20px',
                'boxSizing': 'border-box'
            }),
            
            # Right column: 3D plot
            html.Div([
                dcc.Graph(
                    figure=create_rastrigin_plot_with_optima(),
                    style={'height': '600px'}
                )
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

from dash import html, dcc
import plotly.graph_objects as go
import numpy as np
import dash_latex as dl

# Generate data for the Rastrigin function
def generate_rastrigin_function(x_range=(-5, 5), y_range=(-5, 5), resolution=50):
    x = np.linspace(x_range[0], x_range[1], resolution)
    y = np.linspace(y_range[0], y_range[1], resolution)
    X, Y = np.meshgrid(x, y)
    # Rastrigin function: f(x,y) = 20 + x² - 10*cos(2πx) + y² - 10*cos(2πy)
    Z = 20 + X**2 - 10*np.cos(2*np.pi*X) + Y**2 - 10*np.cos(2*np.pi*Y)
    return X, Y, Z

# Create the 3D Rastrigin function plot
def create_rastrigin_plot():
    X, Y, Z = generate_rastrigin_function()
    
    fig = go.Figure(data=[go.Surface(
        x=X, y=Y, z=Z,
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(title='f(x,y)', len=1.0, y=0.4)
    )])
    
    # Add marker at global optimum (0, 0, 0)
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
        title='Rastrigin Function with Global Optimum',
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

# Content in multiple languages
CONTENT = {
    'en': {
        'title': 'Global Optimization',
        'heading': 'What is Global Optimization?',
        'bullet1_part1': 'Global optimization aims to find the ',
        'bullet1_strong': 'best solution',
        'bullet1_part2': ' across the entire search space.',
        'bullet2_part1': 'Optimization problem where we need a ',
        'bullet2_strong': 'single solution',
        'bullet2_part2': '.',
        'math_heading': 'Mathematical Definition:',
        'explanation_where': 'where ',
        'explanation_x': ' is the decision variable, ',
        'explanation_S': ' is the search space, and ',
        'explanation_f': ' is the objective function.',
        'plot_title': 'Rastrigin Function with Global Optimum',
        'plot_legend': 'Global Optimum'
    },
    'pt-br': {
        'title': 'Otimização Global',
        'heading': 'O que é Otimização Global?',
        'bullet1_part1': 'Otimização global visa encontrar a ',
        'bullet1_strong': 'melhor solução',
        'bullet1_part2': ' em todo o espaço de busca.',
        'bullet2_part1': 'Problema de otimização onde precisamos de uma ',
        'bullet2_strong': 'única solução',
        'bullet2_part2': '.',
        'math_heading': 'Definição Matemática:',
        'explanation_where': 'onde ',
        'explanation_x': ' é a variável de decisão, ',
        'explanation_S': ' é o espaço de busca, e ',
        'explanation_f': ' é a função objetivo.',
        'plot_title': 'Função de Rastrigin com Ótimo Global',
        'plot_legend': 'Ótimo Global'
    }
}

# Slide 1 layout
def layout(language='en'):
    # Get content for selected language
    content = CONTENT.get(language, CONTENT['en'])
    
    # Create plot with translated title and legend
    X, Y, Z = generate_rastrigin_function()
    
    fig = go.Figure(data=[go.Surface(
        x=X, y=Y, z=Z,
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(title='f(x,y)', len=1.0, y=0.4)
    )])
    
    # Add marker at global optimum (0, 0, 0)
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
        name=content['plot_legend'],
        showlegend=True
    ))
    
    fig.update_layout(
        title=content['plot_title'],
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
                html.H4(content['heading'], style={'color': '#2c3e50'}),

                html.Ul([
                    html.Li([content['bullet1_part1'],
                             html.Strong(content['bullet1_strong']),
                             content['bullet1_part2']]),
                    html.Li([content['bullet2_part1'], 
                             html.Strong(content['bullet2_strong']),
                             content['bullet2_part2']]),
                ], style={'fontSize': '18px', 'lineHeight': '1.6'}),
                
                html.H4(content['math_heading'], style={'color': '#34495e', 'marginTop': '20px'}),
                
                html.Div([
                    dl.DashLatex(
                        r"$$\min_{x \in S} f(x)$$",
                        displayMode=True
                    ),
                ], style={'margin': '20px 0', 'fontSize': '18px'}),
                
                html.P([
                    content['explanation_where'],
                    dl.DashLatex(r"$x$"),
                    content['explanation_x'],
                    dl.DashLatex(r"$S$"),
                    content['explanation_S'],
                    dl.DashLatex(r"$f(x)$"),
                    content['explanation_f']
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
                    figure=fig,
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

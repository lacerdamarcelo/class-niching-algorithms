import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

# Import slide layouts
from slides import slide_1, slide_2, slide_3, slide_4, slide_5, slide_6

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Define slides
SLIDES = [
    {"id": 1, "name": "Global Optimization", "layout": slide_1.layout},
    {"id": 2, "name": "Particle Swarm Optimization", "layout": slide_2.layout},
    {"id": 3, "name": "Niching Optimization Introduction", "layout": slide_3.layout},
    {"id": 4, "name": "Niching Optimization", "layout": slide_4.layout},
    {"id": 5, "name": "Niching PSO", "layout": slide_5.layout},
    {"id": 6, "name": "Wrap-Up", "layout": slide_6.layout},
    # Add more slides here as they are created
]

# App layout
app.layout = html.Div([
    # Store components
    dcc.Store(id='current-slide', data=1),
    dcc.Store(id='language', data='en'),
    
    # Header with title and language switcher
    html.Div([
        # Main title
        html.H1(
            id='main-title',
            children="Niching Optimization",
            style={
                'textAlign': 'center',
                'color': '#2c3e50',
                'marginBottom': '20px',
                'marginTop': '20px',
                'fontSize': '48px',
                'fontWeight': 'bold'
            }
        ),
        
        # Language switcher
        html.Div([
            html.Button(
                '🇺🇸 EN',
                id='lang-en-button',
                n_clicks=0,
                style={
                    'padding': '8px 15px',
                    'fontSize': '14px',
                    'marginRight': '5px',
                    'backgroundColor': '#3498db',
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '5px',
                    'cursor': 'pointer'
                }
            ),
            html.Button(
                '🇧🇷 PT',
                id='lang-pt-button',
                n_clicks=0,
                style={
                    'padding': '8px 15px',
                    'fontSize': '14px',
                    'backgroundColor': '#95a5a6',
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '5px',
                    'cursor': 'pointer'
                }
            )
        ], style={
            'position': 'absolute',
            'top': '30px',
            'right': '30px'
        })
    ], style={'position': 'relative'}),
    
    # Slide indicator
    html.Div(
        id='slide-indicator',
        style={
            'textAlign': 'center',
            'color': '#7f8c8d',
            'marginBottom': '20px',
            'fontSize': '14px'
        }
    ),
    
    # Slide content container
    html.Div(
        id='slide-content',
        style={
            'maxWidth': '1400px',
            'margin': '0 auto',
            'padding': '20px'
        }
    ),
    
    # Navigation buttons
    html.Div([
        html.Button(
            '← Previous',
            id='prev-button',
            n_clicks=0,
            style={
                'padding': '10px 30px',
                'fontSize': '16px',
                'marginRight': '20px',
                'backgroundColor': '#3498db',
                'color': 'white',
                'border': 'none',
                'borderRadius': '5px',
                'cursor': 'pointer'
            }
        ),
        html.Button(
            'Next →',
            id='next-button',
            n_clicks=0,
            style={
                'padding': '10px 30px',
                'fontSize': '16px',
                'backgroundColor': '#3498db',
                'color': 'white',
                'border': 'none',
                'borderRadius': '5px',
                'cursor': 'pointer'
            }
        )
    ], style={
        'textAlign': 'center',
        'marginTop': '30px',
        'marginBottom': '30px'
    })
])

# Callback to handle language switching
@app.callback(
    [Output('language', 'data'),
     Output('lang-en-button', 'style'),
     Output('lang-pt-button', 'style'),
     Output('main-title', 'children'),
     Output('prev-button', 'children'),
     Output('next-button', 'children')],
    [Input('lang-en-button', 'n_clicks'),
     Input('lang-pt-button', 'n_clicks')],
    [State('language', 'data')]
)
def switch_language(en_clicks, pt_clicks, current_lang):
    ctx = dash.callback_context
    
    # Default styles
    active_style = {
        'padding': '8px 15px',
        'fontSize': '14px',
        'marginRight': '5px',
        'backgroundColor': '#3498db',
        'color': 'white',
        'border': 'none',
        'borderRadius': '5px',
        'cursor': 'pointer'
    }
    inactive_style = {
        'padding': '8px 15px',
        'fontSize': '14px',
        'marginRight': '5px',
        'backgroundColor': '#95a5a6',
        'color': 'white',
        'border': 'none',
        'borderRadius': '5px',
        'cursor': 'pointer'
    }
    
    if not ctx.triggered:
        if current_lang == 'en':
            return 'en', active_style, inactive_style, "Niching Optimization", "← Previous", "Next →"
        else:
            return 'pt-br', inactive_style, active_style, "Otimização por Nichos", "← Anterior", "Próximo →"
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'lang-en-button':
        return 'en', active_style, inactive_style, "Niching Optimization", "← Previous", "Next →"
    elif button_id == 'lang-pt-button':
        return 'pt-br', inactive_style, active_style, "Otimização por Nichos", "← Anterior", "Próximo →"
    
    return current_lang, active_style, inactive_style, "Niching Optimization", "← Previous", "Next →"


# Callback to update slide content and indicator
@app.callback(
    [Output('slide-content', 'children'),
     Output('slide-indicator', 'children'),
     Output('prev-button', 'disabled'),
     Output('next-button', 'disabled')],
    [Input('current-slide', 'data'),
     Input('language', 'data')]
)
def update_slide(current_slide_num, language):
    # Find the current slide
    current_slide = next((s for s in SLIDES if s['id'] == current_slide_num), SLIDES[0])
    
    # Get slide layout with language parameter
    # Try to pass language, if slide doesn't support it, use default
    try:
        layout = current_slide['layout'](language=language)
    except TypeError:
        # Slide doesn't support language parameter yet
        layout = current_slide['layout']()
    
    # Create slide indicator
    if language == 'pt-br':
        indicator = f"Slide {current_slide_num} de {len(SLIDES)}"
    else:
        indicator = f"Slide {current_slide_num} of {len(SLIDES)}"
    
    # Disable buttons at boundaries
    prev_disabled = current_slide_num == 1
    next_disabled = current_slide_num == len(SLIDES)
    
    return layout, indicator, prev_disabled, next_disabled

# Callback to handle navigation
@app.callback(
    Output('current-slide', 'data'),
    [Input('prev-button', 'n_clicks'),
     Input('next-button', 'n_clicks')],
    [State('current-slide', 'data')]
)
def navigate_slides(prev_clicks, next_clicks, current_slide):
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return current_slide
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'prev-button' and current_slide > 1:
        return current_slide - 1
    elif button_id == 'next-button' and current_slide < len(SLIDES):
        return current_slide + 1
    
    return current_slide

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8050)

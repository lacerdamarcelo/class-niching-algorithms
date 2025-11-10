from dash import html

# Content in multiple languages
CONTENT = {
    'en': {
        'heading': 'Cool but...',
        'bullet1_part1': 'What if ',
        'bullet1_strong1': 'multiple',
        'bullet1_part2': ' and ',
        'bullet1_strong2': 'diverse',
        'bullet1_part3': ' solutions are needed?',
        'bullet2_part1': 'How to find ',
        'bullet2_strong': 'multiple optima',
        'bullet2_part2': ' in a single run?'
    },
    'pt-br': {
        'heading': 'Legal, mas...',
        'bullet1_part1': 'E se ',
        'bullet1_strong1': 'múltiplas',
        'bullet1_part2': ' e ',
        'bullet1_strong2': 'diversas',
        'bullet1_part3': ' soluções forem necessárias?',
        'bullet2_part1': 'Como encontrar ',
        'bullet2_strong': 'múltiplos ótimos',
        'bullet2_part2': ' em uma única execução?'
    }
}

# Slide 3 layout
def layout(language='en'):
    # Get content for selected language
    content = CONTENT.get(language, CONTENT['en'])
    
    return html.Div([
        
        # Single column centered content
        html.Div([
            html.H3(content['heading'], style={'color': '#34495e', 'marginTop': '40px'}),
            
            html.Ul([
                html.Li([content['bullet1_part1'], 
                        html.Strong(content['bullet1_strong1']), 
                        content['bullet1_part2'],
                        html.Strong(content['bullet1_strong2']), 
                        content['bullet1_part3']]),
                html.Li([content['bullet2_part1'], 
                        html.Strong(content['bullet2_strong']), 
                        content['bullet2_part2']]),
            ], style={'fontSize': '24px', 'lineHeight': '1.8'})
            
        ], style={
            'maxWidth': '800px',
            'margin': '0 auto',
            'padding': '40px',
            'textAlign': 'left'
        })
    ])

from dash import html

# Content in multiple languages
CONTENT = {
    'en': {
        'title': 'Wrap-Up',
        'subtitle': 'Niching Optimization: Pros & Challenges',
        'advantages_heading': '✓ Advantages',
        'adv1_strong': 'Multiple solutions: ',
        'adv1_text': 'Find diverse optima in a single run',
        'adv2_strong': 'Better exploration: ',
        'adv2_text': 'Improved coverage of the search space',
        'adv3_strong': 'Robustness: ',
        'adv3_text': 'Less likely to get stuck in a single basin',
        'adv4_strong': 'Practical applications: ',
        'adv4_text': 'Design alternatives, portfolio optimization, multi-modal problems',
        'challenges_heading': '⚠ Challenges',
        'chal1_strong': 'Parameter tuning: ',
        'chal1_text': 'Radius r and neighborhood size n are problem-dependent',
        'chal2_strong': 'Computational cost: ',
        'chal2_text': 'More complex than standard algorithms',
        'chal3_strong': 'Niche maintenance: ',
        'chal3_text': 'Difficult to maintain stable niches over time',
        'chal4_strong': 'Convergence speed: ',
        'chal4_text': 'May converge slower than focused global optimization',
        'takeaway_heading': '🎯 Key Takeaway',
        'takeaway_part1': 'Use ',
        'takeaway_strong1': 'niching methods',
        'takeaway_part2': ' when you need ',
        'takeaway_strong2': 'multiple diverse solutions',
        'takeaway_part3': ' or want to explore ',
        'takeaway_strong3': 'different regions',
        'takeaway_part4': ' of the search space. Use ',
        'takeaway_strong4': 'global optimization',
        'takeaway_part5': ' when a ',
        'takeaway_strong5': 'single best solution',
        'takeaway_part6': ' is sufficient.'
    },
    'pt-br': {
        'title': 'Conclusão',
        'subtitle': 'Otimização por Nichos: Vantagens & Desafios',
        'advantages_heading': '✓ Vantagens',
        'adv1_strong': 'Múltiplas soluções: ',
        'adv1_text': 'Encontrar diversos ótimos em uma única execução',
        'adv2_strong': 'Melhor exploração: ',
        'adv2_text': 'Cobertura melhorada do espaço de busca',
        'adv3_strong': 'Robustez: ',
        'adv3_text': 'Menos propenso a ficar preso em uma única bacia',
        'adv4_strong': 'Aplicações práticas: ',
        'adv4_text': 'Alternativas de design, otimização de portfólio, problemas multi-modais',
        'challenges_heading': '⚠ Desafios',
        'chal1_strong': 'Ajuste de parâmetros: ',
        'chal1_text': 'Raio r e tamanho de vizinhança n dependem do problema',
        'chal2_strong': 'Custo computacional: ',
        'chal2_text': 'Mais complexo que algoritmos padrão',
        'chal3_strong': 'Manutenção de nichos: ',
        'chal3_text': 'Difícil manter nichos estáveis ao longo do tempo',
        'chal4_strong': 'Velocidade de convergência: ',
        'chal4_text': 'Pode convergir mais lentamente que otimização global focada',
        'takeaway_heading': '🎯 Ponto Principal',
        'takeaway_part1': 'Use ',
        'takeaway_strong1': 'métodos de otimização por nichos',
        'takeaway_part2': ' quando precisar de ',
        'takeaway_strong2': 'múltiplas soluções diversas',
        'takeaway_part3': ' ou quiser explorar ',
        'takeaway_strong3': 'diferentes regiões',
        'takeaway_part4': ' do espaço de busca. Use ',
        'takeaway_strong4': 'otimização global',
        'takeaway_part5': ' quando uma ',
        'takeaway_strong5': 'única melhor solução',
        'takeaway_part6': ' for suficiente.'
    }
}

# Slide 6 layout
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
        
        # Single column centered content
        html.Div([
            html.H3(content['subtitle'], 
                   style={'color': '#2c3e50', 'textAlign': 'center', 'marginBottom': '30px'}),
            
            # Advantages Section
            html.Div([
                html.H4(content['advantages_heading'], style={'color': '#27ae60', 'marginBottom': '15px'}),
                
                html.Ul([
                    html.Li([html.Strong(content['adv1_strong']), content['adv1_text']]),
                    html.Li([html.Strong(content['adv2_strong']), content['adv2_text']]),
                    html.Li([html.Strong(content['adv3_strong']), content['adv3_text']]),
                    html.Li([html.Strong(content['adv4_strong']), content['adv4_text']]),
                ], style={'fontSize': '20px', 'lineHeight': '1.8', 'marginBottom': '30px'})
            ]),
            
            # Challenges Section
            html.Div([
                html.H4(content['challenges_heading'], style={'color': '#e67e22', 'marginBottom': '15px'}),
                
                html.Ul([
                    html.Li([html.Strong(content['chal1_strong']), content['chal1_text']]),
                    html.Li([html.Strong(content['chal2_strong']), content['chal2_text']]),
                    html.Li([html.Strong(content['chal3_strong']), content['chal3_text']]),
                    html.Li([html.Strong(content['chal4_strong']), content['chal4_text']]),
                ], style={'fontSize': '20px', 'lineHeight': '1.8', 'marginBottom': '30px'})
            ]),
            
            # Key Takeaway
            html.Div([
                html.H4(content['takeaway_heading'], style={'color': '#3498db', 'marginBottom': '15px'}),
                
                html.P([
                    content['takeaway_part1'],
                    html.Strong(content['takeaway_strong1']),
                    content['takeaway_part2'],
                    html.Strong(content['takeaway_strong2']),
                    content['takeaway_part3'],
                    html.Strong(content['takeaway_strong3']),
                    content['takeaway_part4'],
                    html.Strong(content['takeaway_strong4']),
                    content['takeaway_part5'],
                    html.Strong(content['takeaway_strong5']),
                    content['takeaway_part6']
                ], style={'fontSize': '20px', 'lineHeight': '1.8', 'textAlign': 'center', 
                         'padding': '20px', 'backgroundColor': '#ecf0f1', 'borderRadius': '10px'})
            ])
            
        ], style={
            'maxWidth': '900px',
            'margin': '0 auto',
            'padding': '40px',
            'textAlign': 'left'
        })
    ])

from dash import dcc, html

layout = html.Div([
    html.H1('GraphMuse', style={'textAlign': 'center', 'fontFamily': 'Arial'}),

    html.Div([
        html.Div([
            html.Label('Stat'),
            dcc.Dropdown(
                id='stat-dropdown',
                options=[
                    {'label': 'Points', 'value': 'PTS'},
                    {'label': 'Assists', 'value': 'AST'},
                    {'label': 'Rebounds', 'value': 'REB'},
                    {'label': 'Steals', 'value': 'STL'},
                    {'label': 'Blocks', 'value': 'BLK'},
                ],
                value='PTS',
                clearable=False
            ),
        ], style={'width': '30%', 'display': 'inline-block', 'margin': '10px'}),

        html.Div([
            html.Label('Type'),
            dcc.Dropdown(
                id='type-dropdown',
                options=[
                    {'label': 'Total', 'value': 'total'},
                    {'label': 'Per Game', 'value': 'per_game'},
                ],
                value='total',
                clearable=False
            ),
        ], style={'width': '30%', 'display': 'inline-block', 'margin': '10px'}),

        html.Div([
            html.Label('Number of Players'),
            dcc.Input(
                id='count-input',
                type='number',
                value=10,
                min=1,
                max=50,
                step=1,
                style={'width': '100%', 'padding': '8px', 'fontSize': '14px'}
            ),
        ], style={'width': '30%', 'display': 'inline-block', 'margin': '10px', 'verticalAlign': 'top'}),

    ], style={'textAlign': 'center'}),

    html.Div([
        html.Button('Generate', id='generate-button', n_clicks=0, style={
            'padding': '10px 30px',
            'fontSize': '16px',
            'backgroundColor': '#007AC1',
            'color': 'white',
            'border': 'none',
            'borderRadius': '5px',
            'cursor': 'pointer',
            'marginTop': '10px'
        })
    ], style={'textAlign': 'center'}),

    dcc.Graph(id='bar-chart')
])
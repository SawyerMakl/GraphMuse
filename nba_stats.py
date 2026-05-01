from nba_api.stats.endpoints import leagueleaders
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, State
import sqlite3
from layout import layout

# Connect to database (creates nba_stats.db file if it doesn't exist)
conn = sqlite3.connect('nba_stats.db')

# Pull data from API and save to database
df = leagueleaders.LeagueLeaders().get_data_frames()[0]

# Calculate per game stats
df['PTS_PG'] = (df['PTS'] / df['GP']).round(2)
df['AST_PG'] = (df['AST'] / df['GP']).round(2)
df['REB_PG'] = (df['REB'] / df['GP']).round(2)
df['STL_PG'] = (df['STL'] / df['GP']).round(2)
df['BLK_PG'] = (df['BLK'] / df['GP']).round(2)

# Save to SQL database
df.to_sql('players', conn, if_exists='replace', index=False)

# Makes sure data is read from database, not API
df = pd.read_sql('SELECT * FROM players', conn)

team_colors = {
    'ATL': '#E03A3E', 'BOS': '#007A33', 'BKN': '#000000',
    'CHA': '#1D1160', 'CHI': '#CE1141', 'CLE': '#860038',
    'DAL': '#00538C', 'DEN': '#0E2240', 'DET': '#C8102E',
    'GSW': '#1D428A', 'HOU': '#CE1141', 'IND': '#002D62',
    'LAC': '#C8102E', 'LAL': '#552583', 'MEM': '#5D76A9',
    'MIA': '#98002E', 'MIL': '#00471B', 'MIN': '#0C2340',
    'NOP': '#0C2340', 'NYK': '#F58426', 'OKC': '#007AC1',
    'ORL': '#0077C0', 'PHI': '#006BB6', 'PHX': '#1D1160',
    'POR': '#E03A3E', 'SAC': '#5A2D81', 'SAS': '#C4CED4',
    'TOR': '#CE1141', 'UTA': '#002B5C', 'WAS': '#002B5C',
}

app = Dash(__name__)
app.layout = layout

@app.callback(
    Output('bar-chart', 'figure'),
    Input('generate-button', 'n_clicks'),
    State('stat-dropdown', 'value'),
    State('type-dropdown', 'value'),
    State('count-input', 'value')
)
def update_chart(n_clicks, stat, type, count):
    if n_clicks == 0:
        return {}

    col = f'{stat}_PG' if type == 'per_game' else stat

    local_conn = sqlite3.connect('nba_stats.db')
    query = f'SELECT * FROM players ORDER BY {col} DESC LIMIT {count}'
    top_n = pd.read_sql(query, local_conn)
    local_conn.close()

    color_map = dict(zip(top_n['PLAYER'], top_n['TEAM'].map(team_colors)))

    fig = px.bar(top_n, x='PLAYER', y=col,
                 title=f'Top {count} NBA Players by {col}',
                 labels={col: col, 'PLAYER': 'Player'},
                 color='PLAYER',
                 color_discrete_map=color_map)
    fig.update_layout(showlegend=False)
    return fig


if __name__ == '__main__':
    app.run(debug=True)
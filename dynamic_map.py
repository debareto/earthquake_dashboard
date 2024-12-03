import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
from read_data import get_earthquake_data


app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Earthquake Data Dashboard"),
    dcc.DatePickerSingle(
        id='date-picker',
        min_date_allowed=pd.to_datetime('2000-01-01'),  # Adjust as needed
        max_date_allowed=pd.to_datetime('2024-12-31'),  # Adjust as needed
        initial_visible_month=pd.to_datetime('2024-01-01'),
        date=pd.to_datetime('2024-01-05'),
    ),
    dcc.Graph(id='earthquake-map'),
    html.Div(id='stats')
])


@app.callback(
    [Output('earthquake-map', 'figure'),
     Output('stats', 'children')],
    Input('date-picker', 'date')
)

def update_dashboard(selected_date):
    # Fetch data for the selected date
    df_earthquakes = get_earthquake_data(selected_date)
    df_earthquakes['color'] = pd.cut(df_earthquakes['magnitude'], bins=[0,3,5,100], labels=['green', 'orange', 'red'])
    df_earthquakes.loc[df_earthquakes['magnitude'] <= 0, 'magnitude'] = 0.1
    
    # Create Map
    map_figure = go.Figure(
        go.Scattergeo(
            lon=df_earthquakes["longitude"],
            lat=df_earthquakes["latitude"],
            text=df_earthquakes["location"] + "<br>Magnitude: " + df_earthquakes["magnitude"].astype(str),
            marker=dict(
                size=(df_earthquakes['magnitude'] * 3),
                color=df_earthquakes["color"],
                line=dict(width=1, color="black"),
            ),
        )
    )
    map_figure.update_layout(
        height=500,
        width= 1000,
        margin={"r":0, "t":0, "l":0, "b":0},
        geo=dict(projection_type="orthographic")
    )

    # Generate statistics
    stats_text = df_earthquakes.describe().to_html()

    return map_figure, stats_text


if __name__ == '__main__':
    app.run_server(debug=True)
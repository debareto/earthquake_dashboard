import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
from read_data import get_earthquake_data

app = dash.Dash(__name__)

# # Custom CSS
# app.css.append_css({
#     'external_url': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css'
# })

app.layout = html.Div([
    html.Div([
        html.H1("Earthquake Data Dashboard", style={
            'textAlign': 'center',
            'fontFamily': 'Arial, sans-serif',
            'color': '#333', 
            'fontSize':'20px'
        }),
        html.P("Select a date to view earthquake data", style={
            'textAlign': 'center',
            'fontFamily': 'Arial, sans-serif',
            'color': '#777',
            'fontSize': '16px'
        })
    ], style={'padding': '20px', 'backgroundColor': '#f7f7f7'}),
    html.Div([
        
        dcc.DatePickerSingle(
            id='date-picker',
            min_date_allowed=pd.to_datetime('2000-01-01'),
            max_date_allowed=pd.to_datetime('2024-12-31'),
            initial_visible_month=pd.to_datetime('2024-01-01'),
            date=pd.to_datetime('2024-01-05'),
            display_format='DD/MM/YYYY', 
            style={
                'display': 'inline-block',
                'margin': '10px auto',
                'borderRadius': '5px',
                'border': '1px solid #ddd',
                'fontSize': '14px',  # Increased font size for better visibility
                'backgroundColor': '#fff'
            }
        ) ,
    ], style={'textAlign': 'center', 'paddingBottom': '20px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),  # Flexbox for alignment
    
    html.Div([
        dcc.Graph(id='earthquake-map', style={
            'height': '400px',
            'width': '100%',
            'MaxWidth': '600px',
            'border': '1px solid #ddd',
            'borderRadius': '10px',
        })
    ], style={'padding': '0 20px', 'textAlign': 'center'}),

   
])


@app.callback(
    Output('earthquake-map', 'figure'),
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
                opacity=0.7
            ),
        )
    )
    
    map_figure.update_layout(
        # height=400,
        # width=400,
        margin={"r":0, "t":0, "l":0, "b":0},
        # geo=dict(projection_type="orthographic"),
        # title="Earthquake Locations and Magnitudes",
        title_x=0.5,
        # title_font=dict(size=20, color='rgb(0, 0, 0)', family="Arial"),
    )
    
    map_figure.update_geos(showcountries=True, countrycolor="grey")

    return map_figure


if __name__ == '__main__':
    app.run_server(debug=True)

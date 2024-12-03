import pandas as pd
from read_data import get_earthquake_data
import plotly.express as px
import plotly.graph_objects as go



date ='2024-01-05'
df_earthquakes = get_earthquake_data(date)

df_earthquakes['color'] =pd.cut(df_earthquakes['magnitude'], bins=[0,3,5,100], labels=['green', 'orange', 'red'])

print(df_earthquakes.head())

print(df_earthquakes.describe())
df_sample = df_earthquakes.copy()

df_sample.loc[df_sample['magnitude']<=0, 'magnitude'] = 0.1

# Create Scattergeo plot
map = go.Figure()

map.add_trace(
    go.Scattergeo(
        lon=df_sample["longitude"],
        lat=df_sample["latitude"],
        text=df_sample["location"] + "<br>Magnitude: " + df_sample["magnitude"].astype(str),
        marker=dict(
            size=(df_sample['magnitude']*3),
            color=df_sample["color"],
            line=dict(width=1, color="black"),
        ),
    )
)
map.update_geos(projection_type="orthographic")


map.update_layout(height=700, width=1200, margin={"r":0,"t":0,"l":0,"b":0})
map.show()
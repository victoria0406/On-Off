import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import pandas as pd

your_id = 2
color_2d = [[0, 'rgb(255,255,255)'], [1.0, 'rgb(252,156,26)']]

group_df = pd.read_csv('datas/total_user_usage.csv')
your_ust = group_df.loc[your_id, 'usage_time']
your_sdt = group_df.loc[your_id, 'session_duration_time']
group_ust_mean = group_df["usage_time"].mean()
group_sdt_mean = group_df["session_duration_time"].mean()

fig1 = go.Figure(go.Histogram2dContour(
                    x = group_df["usage_time"],
                    y = group_df["session_duration_time"],
                    colorscale=color_2d,
                    showscale=False))
fig1.update_traces(contours_showlines=False, legendwidth=400)
fig1.add_trace(go.Scatter(x=[your_ust], y=[your_sdt], mode = 'markers', 
                          marker=dict(
                              color='#0F4997', 
                              size=10
                              )
                          ))
fig1.update_layout(
    title="your group: RISK Group"
    )

fig2 = go.Figure(go.Bar(
                    x=[group_sdt_mean],
                    y=['Others'],
                    orientation='h',
                    marker_color='#FC9C1A',
                    opacity=0.8
                ))
fig2.add_trace(go.Bar(
                    x=[your_sdt],
                    y=['You'],
                    orientation='h',
                    marker_color='#0F4997',
                    opacity=0.8
                ))
fig2.update_layout(plot_bgcolor = 'white', title="Weekly Average Session Time", 
                   bargap=0, showlegend=False)
fig2.update_yaxes(showline=True, linewidth=2, linecolor='black',)
fig2.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e5e5e5')

app_df = pd.read_csv('datas/weekly_average.csv')
# fig3 = px.bar(app_df, x="day", y="usage_time", barmode='group', color='type')
fig3 = go.Figure(go.Bar(
                    x=app_df.day,
                    y=app_df.user_usage_time,
                    marker_color='#0F4997',
                    opacity=0.8
                ))
fig3.add_trace(go.Bar(
                    x=app_df.day,
                    y=app_df.group_usage_time,
                    marker_color='#FC9C1A',
                    opacity=0.8
                ))
fig3.update_layout(plot_bgcolor = 'white', title="Weekly Usage Time",
                   showlegend=False, barmode='group')
fig3.update_xaxes(showline=True, linewidth=2, linecolor='black',)
fig3.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e5e5e5')





dash.register_page(__name__)

layout = html.Div(children=[
    html.Div(
        dbc.Row([
            dbc.Col(
                html.H1('Compare your usage with others :)')
            ),
            dbc.Col(
                dcc.Link(html.Button("Check Your Usage Pattern!"), href="/report")
            )
        ]),
    ),

    dbc.Row([
        dbc.Col(
            dcc.Graph(figure = fig1)
        ),
        dbc.Col(
            dcc.Graph(figure = fig2)
        )
    ]),
    dbc.Row([
        dcc.Graph(figure = fig3)
    ])

])
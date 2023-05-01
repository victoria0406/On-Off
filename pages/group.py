import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import pandas as pd

user_square_style = {
    'width': '20px',
    'height': '20px',
    'background-color': '#0F4997'
}

others_square_style = {
    'width': '20px',
    'height': '20px',
    'background-color': '#FC9C1A'
}

col_style = {
    'background-color': '#f8f9fa',
    'border-radius': '10px',
    'padding': '10px',
    'display': 'flex',
    'flex-direction': 'row',
}

col_item_style = {
    'display': 'flex',
    'flex-direction': 'row',
}

button_style = {
    'font-family': 'Arial',
    'width': '100%',
    'outline': 'None',
    'background-color': '#f8f9fa',
    'font-family': 'Arial',
    'color': '#000000',
    'border': 'none'
}


child_classes = 'm-2'

your_id = 2
color_2d = [[0, 'rgb(255,255,255)'], [1.0, 'rgb(252,156,26)']]

group_df = pd.read_csv('datas/total_user_usage.csv')
your_ust = group_df.loc[your_id, 'usage_time']
your_sdt = group_df.loc[your_id, 'session_duration_time']
group_ust_mean = group_df["usage_time"].mean()
group_ust_median = group_df['usage_time'].median()
group_sdt_mean = group_df["session_duration_time"].mean()
group_sdt_median = group_df['session_duration_time'].median()

fig1 = go.Figure(go.Histogram2dContour(
                    x = group_df["usage_time"],
                    y = group_df["session_duration_time"],
                    colorscale=color_2d,
                    showscale=False))
fig1.update_traces(contours_showlines=False, legendwidth=400)
fig1.add_trace(go.Scatter(x=[your_ust], y=[your_sdt], mode = 'markers+text', 
                          text=["You"], textposition="bottom center",
                          textfont=dict(
                              family="Arial",
                              size=12,
                              color="#0F4997"
                              ),
                          marker=dict(
                              color='#0F4997', 
                              size=10
                              )
                          ))
fig1.add_vline(x=group_ust_median)
fig1.add_hline(y=group_sdt_median)
fig1.add_trace(go.Scatter(x=[group_ust_median, group_ust_median, max(group_df['usage_time']), max(group_df['usage_time']), group_ust_median], y=[group_sdt_median, max(group_df['session_duration_time']), max(group_df['session_duration_time']), group_sdt_median, group_sdt_median], fill="toself"))
fig1.update_layout(
    title="your group: RISK Group",
    width=500, height=375,
    showlegend=False,
    )

fig2 = go.Figure(go.Bar(
                    x=[group_sdt_mean],
                    y=['Others'],
                    orientation='h',
                    marker_color='#FC9C1A',
                    opacity=0.8,
                    text=[group_sdt_mean],
                    hoverinfo='none'
                ))
fig2.add_trace(go.Bar(
                    x=[your_sdt],
                    y=['You'],
                    orientation='h',
                    marker_color='#0F4997',
                    opacity=0.8,
                    text=[your_sdt],
                    hoverinfo='none'
                ))
fig2.update_layout(plot_bgcolor = 'white', title="Weekly Average Session Time", 
                   bargap=0.2, showlegend=False, width=448, height=237,)
fig2.update_yaxes(showline=True, showticklabels=False, linewidth=2, linecolor='black',)
fig2.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e5e5e5')

app_df = pd.read_csv('datas/weekly_average.csv')
fig3 = go.Figure(go.Bar(
                    x=app_df.day,
                    y=app_df.user_usage_time,
                    marker_color='#0F4997',
                    opacity=0.8,
                    hoverinfo='none',
                    text=app_df.user_usage_time
                ))
fig3.add_trace(go.Bar(
                    x=app_df.day,
                    y=app_df.group_usage_time,
                    marker_color='#FC9C1A',
                    opacity=0.8,
                    hoverinfo='none',
                    text=app_df.group_usage_time
                ))
fig3.update_layout(plot_bgcolor = 'white', title="Weekly Usage Time",
                   showlegend=False, barmode='group', width=1051, height=410)
fig3.update_xaxes(showline=True, linewidth=2, linecolor='black',)
fig3.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e5e5e5')


dash.register_page(__name__)

layout = html.Div(children=[
    html.Div(
        dbc.Row([
            dbc.Col([
                html.H1('Compare your usage with others :)')
            ]),
            dbc.Col(
                dbc.Row([
                    dbc.Col(
                        html.Div(style=col_style, children=[
                            dcc.Link(dbc.Button("Check Your Usage Pattern!", outline=False, style=button_style, color='primary'), href="/report", style={'width': '100%'}),
                        ])
                    ),
                    dbc.Col(style=col_style, children=[
                        html.Div(style=col_item_style, children=[
                            html.Div(
                                html.Div(style=user_square_style),
                                className=child_classes
                            ),
                            html.P(': You', className=child_classes),
                            html.Div(
                                html.Div(style=others_square_style),
                                className=child_classes
                            ),
                            html.P(': Others', className=child_classes)
                        ]), 
                    ])
                ])
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
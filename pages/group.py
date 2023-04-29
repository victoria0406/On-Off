import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go


x = np.random.uniform(-1, 1, size=500)
y = np.random.uniform(-1, 1, size=500)
fig1 = go.Figure(go.Histogram2dContour(
                    x = x, 
                    y = y,
                ))
fig1.update_traces(contours_coloring="fill", contours_showlabels = True)
fig1.update_layout(title="your group:          RISK Group")


fig2 = go.Figure(go.Bar(
                    x=[20, 14],
                    y=['orangutans', 'monkeys'],
                    orientation='h'
                ))
fig2.update_layout(title="Weekly Average Session Time")

df = px.data.tips()
fig3 = px.bar(df, x="sex", y="total_bill",
             title="Weekly Usage Time", color='smoker', barmode='group',
             height=400)





dash.register_page(__name__)

layout = html.Div(children=[
    html.Div(
        dbc.Row([
            dbc.Col(
                html.H1('This is our group page')
            ),
            dbc.Col(
                html.Button('Submit', id='submit-val'),
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
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

dash.register_page(__name__, path='/')

layout = html.Div([
    html.Div(html.Img(src='assets/root.png', className="container_img")),
    # html.H1(
    #         children=["WELCOME TO ",html.Span("ON/OFF :)", style={'color': '#7B9265'})],
    #         style={
    #             'font-weight':'bold',
    #             'padding-top':'30vh',
    #             'textAlign': 'center',
    #             }
    # ),
    # html.H5('Check your phone usage pattern!',style={'padding-top':'20px','text-align':'center'})
], className="container",style={'text-align': 'center'})


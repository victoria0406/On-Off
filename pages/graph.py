import dash
from dash import html, dcc, callback, Input, Output
from inputdata.goalsettingdata import usage_time_info, unlock_info, app_usage_info
from component.todaygoal import today_goal_not_setting
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

from inputdata.data import app_usage_time, today_index, unlock



dash.register_page(__name__)

weekly_usage = app_usage_time[today_index-6:today_index+1]
weekly_usage['date']=pd.to_datetime(weekly_usage['date'], format = "%Y %m %d")
weekly_usage['date']=weekly_usage['date'].dt.strftime('%m/%d')

def usage_graph():
    COLORS = ['rgb(164,189,133,0.6)'] * 7
   
    
    fig = px.bar(weekly_usage, x="date", y="Total", width=750, height=400, color_discrete_sequence=COLORS)
    
    fig.update_layout(
        xaxis = dict(
            title = None,
            tickmode = 'array',
            showline=True, linewidth=1, linecolor='#BEBEBE',
            
        ),
        yaxis = dict(
            # title = "Usage Time (hour)",
            title=dict(
                text="Usage Time (hour)",
                font=dict(
                    size=12,
            )),
            tickmode = 'array',
            tickvals = [0,120,240,360,480,600,720],
            ticktext = ['0', '2', '4', '6', '8', '10','12'],
            showgrid=True, linewidth=1,gridcolor='#E0E0E0',
            tickfont = dict(size=9)
        )
    )
    fig.update_layout(showlegend=False, plot_bgcolor='white',paper_bgcolor="rgb(0,0,0,0)",bargap=0.3)
    
    return fig 
    
def unlock_graph():
    weekly_unlock = unlock[today_index-6:today_index+1]
    weekly_unlock['date']=weekly_usage['date']

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=weekly_unlock['date'], y=weekly_unlock['unlock'], mode='lines+markers', line_color='#E4AE44',
                            marker=dict(
                                    color='white',
                                    size=14,
                                    line=dict(color='#E4AE44',width=2)
                                )))

    fig.update_layout(
        xaxis = dict(
            title = None,
            tickmode = 'array',
            showline=True, linewidth=1, linecolor='#BEBEBE',
        ),
        yaxis =dict(
            showgrid=True, linewidth=1,gridcolor='#E0E0E0',
        )
    )

    fig.update_layout(showlegend=False, plot_bgcolor='white',paper_bgcolor="rgb(0,0,0,0)",width=510, height=320)
    
    return fig 

layout = html.Div(children=[
    
     html.Div(dcc.Graph(figure = usage_graph(), config={'displayModeBar': False})),
     html.Div(dcc.Graph(figure = unlock_graph(), config={'displayModeBar': False}), style={'margin-top':'-50px'})
])
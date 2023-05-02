import dash
from dash.dependencies import Input, Output, State
from dash import html, dcc
from inputdata.goalsettingdata import usage_time_info, unlock_info, app_usage_info, is_goal_setted
from component.goaldonutplot import goal_donut_plot

def unlock_component():
    data = 4;
    component = html.Div([
        html.P('Unlocks', className='goal-title'),
        html.Div([
            html.Div([], className='goal-state-check'),
            html.Span(f"{data} / {unlock_info['time']} times ({(data / unlock_info['time']):.1f}%)")
        ], className='goal-list unlock')
    ])
    return component;

def usage_time_component():
    data = 2;
    usage_time = usage_time_info['hour'] + usage_time_info['minite'] / 60
    component = html.Div([
        html.P('Usage Time',className='goal-title'),
        html.Div([
            html.Div([], className='goal-state-check'),
            html.Span(f"{data} / {usage_time} h ({(data / usage_time):.1f}%)")
        ], className='goal-list usage')
    ])
    return component;

def app_usage_component():
    data = 1;
    usage_time = app_usage_info['hour'] + app_usage_info['minite'] / 60
    component = html.Div([
        html.P(f"App Usage Time for {app_usage_info['app']}",className='goal-title'),
        html.Div([
            html.Div([], className='goal-state-check'),
            html.Span(f"{data} / {usage_time} h ({(data / usage_time):.1f}%)")
        ], className='goal-list app')
    ])
    return component;

def get_goal_info():
    return [
        [0, 4, unlock_info['time']-4] if unlock_info['checked'] else None,
        [0, 2, usage_time_info['hour'] + usage_time_info['minite'] / 60 - 2] if usage_time_info['checked'] else None,
        [0, 1, app_usage_info['hour'] + app_usage_info['minite'] / 60 - 1] if app_usage_info['checked'] else None,
    ]

def today_goal_setting():
    return_children = [html.P('Today Goal', style={'font-weight': 'bold'})]
    fig = goal_donut_plot(*get_goal_info())
    fig.update_layout(showlegend=False, plot_bgcolor='rgb(0,0,0,0)',paper_bgcolor="rgb(0,0,0,0)",width=400, height=400)
    return_children.append(dcc.Graph(figure = fig, config={'displayModeBar': False}, className='today-goal-fig'))
    if unlock_info['checked']:
        return_children.append(unlock_component())
    if usage_time_info['checked']:
        return_children.append(usage_time_component())
    if app_usage_info['checked']:
        return_children.append(app_usage_component())
    component = html.Div(return_children, className='today-goal-list')
    return component
    
today_goal_not_setting = [
    html.P('Today Goal', style={'font-weight': 'bold'}),
    html.A('+', className='set-goal-button',href='/goalsetting'),
    html.P('Set Your Goal!', style={'margin-bottom': '120px'})
]
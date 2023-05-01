import dash
from dash.dependencies import Input, Output, State
from dash import html
from inputdata.goalsettingdata import usage_time_info, unlock_info, app_usage_info, is_goal_setted

def unlock_component():
    data = 4;
    component = html.Div([
        html.P('Unlocks'),
        html.Div([
            html.Div([], className='goal-state-check'),
            html.Span(f"{data} / {unlock_info['time']} times ({(data / unlock_info['time']):.1f}%)")
        ], className='goal-list')
    ])
    return component;

def usage_time_component():
    data = 2;
    usage_time = usage_time_info['hour'] + usage_time_info['minite'] / 60
    component = html.Div([
        html.P('Usage Time'),
        html.Div([
            html.Div([], className='goal-state-check'),
            html.Span(f"{data} / {usage_time} h ({(data / usage_time):.1f}%)")
        ], className='goal-list')
    ])
    return component;

def app_usage_component():
    data = 3;
    usage_time = app_usage_info['hour'] + app_usage_info['minite'] / 60
    component = html.Div([
        html.P(f"App Usage Time for {app_usage_info['app']}"),
        html.Div([
            html.Div([], className='goal-state-check'),
            html.Span(f"{data} / {usage_time} h ({(data / usage_time):.1f}%)")
        ], className='goal-list')
    ])
    return component;

def today_goal_setting():
    return_children = [html.P('Today Goal')]
    if usage_time_info['checked']:
        return_children.append(usage_time_component())
    if unlock_info['checked']:
        return_children.append(unlock_component())
    if app_usage_info['checked']:
        return_children.append(app_usage_component())
    print(return_children);
    component = html.Div(return_children)
    return component
    
today_goal_not_setting = html.Div([
    html.P('Today Goal'),
    html.A('Set Goal', className='link-button goal-setting main',href='/goalsetting'),
])
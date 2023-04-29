import dash
from dash import html, dcc, callback, Input, Output

def customcheckbox(checked):
    plus_layout = html.Div([
        '+'
    ], className="custom-checkbox plus")
    minus_layout = html.Div([
        '-'
    ], className="custom-checkbox minus")
    if (checked) :return plus_layout
    else : return minus_layout


def goalsettingcomponent (goal, desc, value_component, checked):
    layout = html.Div([
        customcheckbox(checked),
        html.Div([
            html.P(goal, className='goal'),
            html.P(desc, className='desc'),
        ])
        
    ], className=f"goal-setting-list-container { 'active' if (checked) else ''}")
    return layout
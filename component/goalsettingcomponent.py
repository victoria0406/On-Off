import dash
from dash import html, dcc, callback, Input, Output

def customcheckbox(type, checked):
    return html.Div([
        dcc.Checklist(
            id=f'goal-switch-input-{type}',
            options=[{'label': 
                html.Div(id=f'goal-switch-output-{type}'),
            'value': 'on'}],
            value=[f"{'on' if checked else None}"],
            className='custom-checkbox-container'
        ),
    ])


def goalsettingcomponent (goal, desc, value_component, checked, type):
    layout = html.Div([
        customcheckbox(type, checked),
        html.Div([
            html.P(goal, className='goal'),
            html.P(desc, className='desc'),
        ]),
        html.Div(value_component, className='value-component')
        
    ],
    id=f"goal-setting-list-container-{type}",
    className=f"goal-setting-list-container { 'active' if (checked) else ''}")
    return layout
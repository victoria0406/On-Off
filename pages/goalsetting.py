import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output

from component.goalsettingcomponent import goalsettingcomponent
from inputdata.goalsettingdata import usage_time_info, unlock_info, app_usage_info

dash.register_page(__name__, path='/goal/setting')

app_list = ['Instagram', 'Youtube', 'KakaoTalk', 'KLMS', 'Naver']
goalsettingcontext = [
    {
        'goal': 'Number of Unlocks',
        'desc': [
            'The average of number of unlocks last week was ',
            html.Span('43 times', style={'color': '#B40000'}),
            '.'
        ],
        'value_component': [
            dbc.Input(type='number', min=0, value=unlock_info['time'], id='goal-switch-disable-unlock-1'),
            'times'
        ],
        'checked': unlock_info['checked'],
        'type': 'unlock'
    },
    {
        'goal': 'Total Usage Time',
        'desc': [
            'The average of total usage time last week was ',
            html.Span('6h 49m', style={'color': '#B40000'}),
            '.'
        ],
        'value_component': [
            dbc.Input(type='number', min=0, max=24, value=usage_time_info['hour'], id='goal-switch-disable-usage-time-1'),
            'h',
            dbc.Input(type='number', min=0, max=30, step=30, value=usage_time_info['minite'], id='goal-switch-disable-usage-time-2'),
            'm',
        ],
        'checked': usage_time_info['checked'],
        'type': 'usage-time',
    },
    {
        'goal': [
            'App Usage Time for ',
            dcc.Dropdown(
                id='app-dropdown',
                className='app-dropdown',
                options=app_list,
                value=app_usage_info['app'],
            )
        ],
        'desc': [
            'The average of the app usage time for ',
            html.Span(id='selected-app'),
            ' last week was ',
            html.Span('1h 14m', style={'color': '#B40000'}),
            '.'
        ],
        'value_component': [
            dbc.Input(type='number', min=0, max=24, value=app_usage_info['hour'], id='goal-switch-disable-app-usage-2'),
            'h',
            dbc.Input(type='number', min=0, max=30, step=30, value=app_usage_info['minite'], id='goal-switch-disable-app-usage-3'),
            'm',
        ],
        'checked': app_usage_info['checked'],
        'type': 'app-usage',
    },
]

layout = html.Div([
    html.P('Set Your Goals!'),
    html.Div([
        goalsettingcomponent(context['goal'], context['desc'], context['value_component'], context['checked'], context['type'])
        for context in goalsettingcontext
    ]),
    dbc.Nav([
        html.A('Cormfirm', className='link-button goal-setting main', href='/goal'),
        html.A('Cancel', className='link-button goal-setting sub'),
    ]),
    ],
    className='goal-setting-container'
)
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output
from component.goalsettingcomponent import goalsettingcomponent

dash.register_page(__name__, path='/goal/setting')

app_list = ['Instagram', 'Youtube', 'KakaoTalk', 'KLMS', 'Naver']

def app_dropdown(disabled):
    return dcc.Dropdown(
        id='app-dropdown',
        className='app-dropdown',
        options=app_list,
        value='Instagram',
        disabled=disabled,
    )

goalsettingcontext = [
    {
        'goal': 'Number of Unlocks',
        'desc': [
            'The average of number of unlocks last week was ',
            html.Span('43 times', style={'color': '#B40000'}),
            '.'
        ],
        'value_component': '',
        'checked': True,
    },
    {
        'goal': 'Total Usage Time',
        'desc': [
            'The average of total usage time last week was ',
            html.Span('6h 49m', style={'color': '#B40000'}),
            '.'
        ],
        'value_component': '',
        'checked': True,
    },
    {
        'goal': [
            'App Usage Time for ',
            app_dropdown(not False),
        ],
        'desc': [
            'The average of the app usage time for ',
            html.Span(id='selected-app'),
            ' last week was ',
            html.Span('1h 14m', style={'color': '#B40000'}),
            '.'
        ],
        'value_component': '',
        'checked': False
    },
]

layout = html.Div([
    html.P('Set Your Goals!', style={''}),
    html.Div([
        goalsettingcomponent(context['goal'], context['desc'], context['value_component'], context['checked'])
        for context in goalsettingcontext
    ]),
    dbc.Nav([
        html.Button('Cormfirm', className='link-button goal-setting main'),
        html.Button('Cancel', className='link-button goal-setting sub'),
    ]),
    ],
    className='goal-setting-container'
)

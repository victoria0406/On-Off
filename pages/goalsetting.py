import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output
import pandas as pd 

from component.goalsettingcomponent import goalsettingcomponent
from inputdata.goalsettingdata import usage_time_info, unlock_info, app_usage_info
from inputdata.data import top

dash.register_page(__name__, path='/goal/setting')

app_usage_df = pd.read_csv('./datas/usage_time.csv')
unlock_df = pd.read_csv('./datas/unlock.csv')
# print(app_usage_df.iloc[:, 1:6].mean().sort_values(ascending=False))
app_list = app_usage_df.iloc[-2, 2:].drop(['Total', 'Others']).dropna().sort_values(ascending=False).index.tolist()
avg_unlock = unlock_df['unlock'].mean()
avg_total_usage = app_usage_df['Total'].mean()
def avg_app_usage(app):
    return app_usage_df[app].mean()
goalsettingcontext = [
    {
        'goal': 'Number of Unlocks',
        'desc': [
            'The average of number of unlocks last week was ',
            html.Span(f'{avg_unlock: .0f} times', style={'color': '#B40000'}),
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
            html.Span(f'{avg_total_usage // 60: .0f}h {avg_total_usage % 60: .0f}m', style={'color': '#B40000'}),
            '.'
        ],
        'value_component': [
            dbc.Input(type='number', min=0, max=23, value=usage_time_info['hour'], id='goal-switch-disable-usage-time-1'),
            'h',
            dbc.Input(type='number', min=0, max=30, step=30, value=usage_time_info['minute'], id='goal-switch-disable-usage-time-2'),
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
                clearable=False,
            )
        ],
        'desc': [
            'The average of the app usage time for ',
            html.Span(id='selected-app'),
            ' last week was ',
            html.Span('', style={'color': '#B40000'}, id='avg-app-usage'),
            '.'
        ],
        'value_component': [
            dbc.Input(type='number', min=0, max=23, value=app_usage_info['hour'], id='goal-switch-disable-app-usage-2'),
            'h',
            dbc.Input(type='number', min=0, max=30, step=30, value=app_usage_info['minute'], id='goal-switch-disable-app-usage-3'),
            'm',
        ],
        'checked': app_usage_info['checked'],
        'type': 'app-usage',
    },
]

layout = html.Div([
    html.P('Set Your Goals!', style={'width': '100%', 'font-weight': 'bold'}),
    html.Div([
        goalsettingcomponent(context['goal'], context['desc'], context['value_component'], context['checked'], context['type'])
        for context in goalsettingcontext
    ]),
    dbc.Nav([
        html.Button('Cormfirm', className='link-button goal-setting main', id='goal-confirm', n_clicks=0),
        html.A('Cancel', className='link-button goal-setting sub', href='/goal?setting=False'),
    ]),
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Confirm Goal")),
            dbc.ModalBody([
                'Would you like to set a daily goal?',
                html.Br(),
                'If you confirm,',
                html.B('the goal cannot be changed until the end of today'),
                '.'
            ]),
            dbc.ModalFooter([
                html.A(
                    "Yes", id="goal-confirm-final", n_clicks=0,
                    href='/goal?setting=True', 
                    className='link-button main',
                ),
                html.Button(
                    "No", id="close", n_clicks=0,
                    className='link-button sub',
                )
            ]),
        ],
        id="modal",
        centered=True,
        is_open=False,
    ),
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Setting Wrong Value")),
            dbc.ModalBody([
                'Your goal setting value is not valid.',
                html.Br(),
                html.Br(),
                'Please check the following:',
                html.Ul([
                    html.Li("If you haven't registered any goals."),
                    html.Li("If the time or count is set in invalid range."),
                    html.Li("If the application is empty."),
                ])
            ]),
            dbc.ModalFooter([
                dbc.Button(
                    "Close", id="close-fault", n_clicks=0,
                    className='link-button sub',
                )
            ], style={}),
        ],
        id="modal-fault",
        centered=True,
        is_open=False,
    ),
    ],
    className='goal-setting-container'
)

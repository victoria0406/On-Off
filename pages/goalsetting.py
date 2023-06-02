import dash
import dash_bootstrap_components as dbc
import pandas as pd 
from dash import html, dcc, callback, Input, Output, State
from component.goalsettingcomponent import goalsettingcomponent
from inputdata.goalsettingdata import usage_time_info, unlock_info, app_usage_info

dash.register_page(__name__, path='/goal/setting')

app_usage_df = pd.read_csv('./data/usage_time.csv')
unlock_df = pd.read_csv('./data/unlock.csv')
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
                'If you confirm, ',
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

@callback(
    [Output("modal", "is_open"), Output('modal-fault', 'is_open'), Output("goal-confirm", "n_clicks"), Output("close", "n_clicks"), Output("close-fault", "n_clicks"),
     Output('unlock_info', 'data'), Output('usage_time_info', 'data'), Output('app_usage_info', 'data'),
    ],
    [Input("goal-confirm", "n_clicks"), Input("close", "n_clicks"), Input("close-fault", "n_clicks")],
    [
        State('goal-switch-disable-unlock-1', 'value'),
        State('goal-switch-disable-usage-time-1', 'value'),
        State('goal-switch-disable-usage-time-2', 'value'),
        State('app-dropdown', 'value'),
        State('goal-switch-disable-app-usage-2', 'value'),
        State('goal-switch-disable-app-usage-3', 'value'),
    ],
)

def goal_setting(n1, n2, n_fault, unlock_time, usage_hour, usage_minute, app_usage_app, app_usage_hour, app_usage_minute):
    global unlock_info
    global usage_time_info
    global app_usage_info
    if (n2 or n_fault):
        return [False, False, 0, 0, 0, dash.no_update, dash.no_update, dash.no_update]
    if (n1):
        if not (unlock_info['checked'] or usage_time_info['checked'] or app_usage_info['checked']):
            return [False, True, 0, 0, 0, dash.no_update, dash.no_update, dash.no_update]
        if (unlock_info['checked'] and unlock_time == 0):
            return [False, True, 0, 0, 0, dash.no_update, dash.no_update, dash.no_update]
        if (usage_time_info['checked'] and ((usage_hour == 0 and usage_minute == 0) or usage_hour == None or usage_minute == None)):
            return [False, True, 0, 0, 0, dash.no_update, dash.no_update, dash.no_update]
        if (app_usage_info['checked'] and app_usage_app == None):
            return [False, True, 0, 0, 0, dash.no_update, dash.no_update, dash.no_update]
        if (app_usage_info['checked'] and ((app_usage_hour == 0 and app_usage_minute == 0) or app_usage_hour == None or app_usage_minute == None)):
            return [False, True, 0, 0, 0, dash.no_update, dash.no_update, dash.no_update]
        unlock_info['time'] = unlock_time
        usage_time_info['hour'] = usage_hour
        usage_time_info['minute'] = usage_minute
        app_usage_info['app'] = app_usage_app
        app_usage_info['hour'] = app_usage_hour
        app_usage_info['minute'] = app_usage_minute
        return [True, False, 0, 0, 0, unlock_info, usage_time_info, app_usage_info]
    else:
        return [False, False, 0, 0, 0, dash.no_update, dash.no_update, dash.no_update]
    
@callback(
    [Output('selected-app', 'children'), Output('avg-app-usage', 'children')],
    Input('app-dropdown', 'value'),
)
def selected_app(value):
    usage = app_usage_df[value].mean()
    return [value, f'{usage // 60:.0f}h {usage % 60:.0f}m']

plus_layout = html.Div([
'+'
], className="custom-checkbox plus")
minus_layout = html.Div([
    '-'
], className="custom-checkbox minus")
@callback(
    [
        Output('goal-switch-output-usage-time', 'children'),
        Output('goal-switch-disable-usage-time-1', 'disabled'),
        Output('goal-switch-disable-usage-time-2', 'disabled'),
        Output('goal-setting-list-container-usage-time', 'className'),
    ],
    Input('goal-switch-input-usage-time', 'value')
)
def usage_time_switch(value):
    global usage_time_info
    if 'on' in value:
        usage_time_info['checked'] = True
        return [[plus_layout], False, False, 'goal-setting-list-container active']
    else:
        usage_time_info['checked'] = False
        return [[minus_layout], True, True, 'goal-setting-list-container']
@callback(
    [
        Output('goal-switch-output-unlock', 'children'),
        Output('goal-switch-disable-unlock-1', 'disabled'),
        Output('goal-setting-list-container-unlock', 'className'),
    ],
    Input('goal-switch-input-unlock', 'value')
)
def unlock_switch(value):
    global unlock_info
    if 'on' in value:
        unlock_info['checked'] = True
        return [[plus_layout], False, 'goal-setting-list-container active']
    else:
        unlock_info['checked'] = False
        return [[minus_layout], True, 'goal-setting-list-container']
@callback(
    [
        Output('goal-switch-output-app-usage', 'children'),
        Output('app-dropdown', 'disabled'),
        Output('goal-switch-disable-app-usage-2', 'disabled'),
        Output('goal-switch-disable-app-usage-3', 'disabled'),
        Output('goal-setting-list-container-app-usage', 'className'),
    ],
    Input('goal-switch-input-app-usage', 'value')
)
def app_usage_switch(value):
    global app_usage_info
    if 'on' in value:
        app_usage_info['checked'] = True
        return [[plus_layout], False, False, False, 'goal-setting-list-container active']
    else:
        app_usage_info['checked'] = False
        return [[minus_layout], True, True, True, 'goal-setting-list-container']

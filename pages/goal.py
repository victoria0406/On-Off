import calendar
import dash
from dash import html, dcc
from inputdata.goalsettingdata import usage_time_info, unlock_info, app_usage_info
from component.todaygoal import today_goal_not_setting, get_goal_today, get_goal_state
from component.goaldonutplot import goal_donut_plot

year = 2023
month = 5
cal = calendar.monthcalendar(year, month)
today_day = 10

def get_calendar_donut_plot(day):
    if (day >= today_day): return None
    goal_state = get_goal_state(day)
    if goal_state == None : return None
    fig = goal_donut_plot(*goal_state)
    donut = dcc.Graph(figure = fig, config={'displayModeBar': False}, className='calendar-donut')
    return donut

# HTML 요소로 변환합니다.
table = html.Table(className=f'goal-calendar', children=[
    html.Thead(children=[
        html.Tr(children=[
            html.Th('Sun'), html.Th('Mon'), html.Th('Tue'),
            html.Th('Wed'), html.Th('Thr'), html.Th('Fri'),
            html.Th('Sat')
        ])
    ]),
    html.Tbody(children=[
        html.Tr(children=[
            html.Td(children=[
                str(day),
                get_calendar_donut_plot(day)
            ], className='today' if (day == today_day) else ''
            , id='today-goal-status' if (day == today_day) else '') if day != 0 else html.Td('')
            for day in week
        ])
        for week in cal
    ])
])

dash.register_page(__name__)

layout = html.Div(children=[
    html.Div(today_goal_not_setting, id='today-goal',),
    html.Div([
        html.P('May 2023', style={'font-weight': 'bold'})
    , table], className='calendar-container', id='calendar-container'),
], style={'display': 'flex', 'justify-content': 'space-between'})
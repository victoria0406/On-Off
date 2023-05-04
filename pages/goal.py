import datetime
import calendar
import dash
from dash import html, dcc
from inputdata.goalsettingdata import usage_time_info, unlock_info, app_usage_info
from component.todaygoal import today_goal_not_setting, get_goal_info
from component.goaldonutplot import goal_donut_plot
import pandas as pd


goal_states_df= pd.read_csv('./datas/goal_states.csv')
goal_states_df['day'] = pd.to_datetime(goal_states_df['date']).dt.day

# 2023년 5월의 달력을 생성합니다.
year = 2023
month = 5
cal = calendar.monthcalendar(year, month)
today_day = 10


def get_goal_state(day):
    day_goal_state = goal_states_df[goal_states_df['day'] == day]
    return_data = [None, None, None];
    if day_goal_state.size == 0 : return None
    day_goal_state = day_goal_state.fillna(-1, axis=1)
    unlock_real = day_goal_state['unlock_real'].values[0]
    unlock_goal = day_goal_state['unlock_goal'].values[0]
    usage_real = day_goal_state['total_usage_real'].values[0]
    usage_goal = day_goal_state['total_usage_goal'].values[0]
    app_real = day_goal_state['app_usage_real'].values[0]
    app_goal = day_goal_state['app_usage_goal'].values[0]
    if (unlock_real> 0):
        exceed = max(unlock_real-unlock_goal, 0)
        real = max(0, min(unlock_real, 2 * unlock_goal - unlock_real))
        goal = max(0, unlock_goal - unlock_real)
        return_data[0] = [exceed, real, goal]
    if (usage_real > 0):
        exceed = max(usage_real-usage_goal, 0)
        real = max(0, min(usage_real, 2 * usage_goal - usage_real))
        goal = max(0, usage_goal - usage_real)
        return_data[1] = [exceed, real, goal]
    if (app_real > 0):
        exceed = max(app_real-app_goal, 0)
        real = max(0, min(app_real, 2 * app_goal - app_real))
        goal = max(0, app_goal - app_real)
        return_data[2] = [exceed, real, goal]
    return return_data

def get_calender_donut_plot(day):
    if (day == today_day) : goal_state = get_goal_info()
    else: goal_state = get_goal_state(day)
    if goal_state == None : return None
    fig = goal_donut_plot(*goal_state)
    donut = dcc.Graph(figure = fig, config={'displayModeBar': False}, className='calender-donut')
    return donut

# HTML 요소로 변환합니다.
table = html.Table(className=f'goal-calender', children=[
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
                get_calender_donut_plot(day)
            ], className='today' if (day == today_day) else '' ) if day != 0 else html.Td('')
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
    , table], className='calander-container'),
], style={'display': 'flex', 'justify-content': 'space-between'})
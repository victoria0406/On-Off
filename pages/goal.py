import datetime
import calendar
import dash
from dash import html, dcc
from inputdata.goalsettingdata import usage_time_info, unlock_info, app_usage_info
from component.todaygoal import today_goal_not_setting
from component.goaldonutplot import goal_donut_plot
import pandas as pd


goal_states_df= pd.read_csv('./datas/goal_states.csv')
goal_states_df['day'] = pd.to_datetime(goal_states_df['date']).dt.day

# 2023년 5월의 달력을 생성합니다.
year = 2023
month = 5
cal = calendar.monthcalendar(year, month)


def get_goal_state(day):
    day_goal_state = goal_states_df[goal_states_df['day'] == day]
    return_data = [None, None, None];
    if day_goal_state.size == 0 : return None
    day_goal_state = day_goal_state.fillna(-1, axis=1)
    if (day_goal_state['unlock_real'].values[0] > 0):
        exceed = max(day_goal_state['unlock_real'].values[0]-day_goal_state['unlock_goal'].values[0], 0)
        real = min(day_goal_state['unlock_real'].values[0], day_goal_state['unlock_goal'].values[0])
        goal = max(0, day_goal_state['unlock_goal'].values[0] - day_goal_state['unlock_real'].values[0])
        return_data[0] = [exceed, real, goal]
    if (day_goal_state['total_usage_real'].values[0] > 0):
        exceed = max(day_goal_state['total_usage_real'].values[0]-day_goal_state['total_usage_goal'].values[0], 0)
        real = min(day_goal_state['total_usage_real'].values[0], day_goal_state['total_usage_goal'].values[0])
        goal = max(0, day_goal_state['total_usage_goal'].values[0] - day_goal_state['total_usage_real'].values[0])
        return_data[1] = [exceed, real, goal]
    if (day_goal_state['app_usage_real'].values[0] > 0):
        exceed = max(day_goal_state['app_usage_real'].values[0]-day_goal_state['app_usage_goal'].values[0], 0)
        real = min(day_goal_state['app_usage_real'].values[0], day_goal_state['app_usage_goal'].values[0])
        goal = max(0, day_goal_state['app_usage_goal'].values[0] - day_goal_state['app_usage_real'].values[0])
        return_data[2] = [exceed, real, goal]
    return return_data

def get_calender_donut_plot(day):
    goal_state = get_goal_state(day)
    if goal_state == None : return None
    fig = goal_donut_plot(*goal_state)
    donut = dcc.Graph(figure = fig, config={'displayModeBar': False}, className='calender-donut')
    return donut

# HTML 요소로 변환합니다.
table = html.Table(className='goal-calender', children=[
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
            ]) if day != 0 else html.Td('')
            for day in week
        ])
        for week in cal
    ])
])

dash.register_page(__name__)


layout = html.Div(children=[
    html.Div(today_goal_not_setting, id='today-goal'),
    html.Div(['May 2023', table], className='calander'),
], style={'display': 'flex', 'justify-content': 'space-between'})
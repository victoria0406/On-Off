import datetime
import calendar
import dash
from dash import html, dcc
from inputdata.goalsettingdata import usage_time_info, unlock_info, app_usage_info
from component.todaygoal import today_goal_not_setting, get_goal_info
from component.goaldonutplot import goal_donut_plot
import pandas as pd
import numpy as np


goal_states_df= pd.read_csv('./datas/goal_states.csv')
## goal_states_df = goal_states_df.fillna(-1, axis=1)
goal_states_df['day'] = pd.to_datetime(goal_states_df['date']).dt.day
goal_states_df['exceed-unlock'] = (goal_states_df['unlock_real'] - goal_states_df['unlock_goal']).apply(lambda x: 0 if x <= 0 else x)
goal_states_df['real-unlock'] = goal_states_df.apply(lambda row: min(row['unlock_real'], 2*row['unlock_goal']-row['unlock_real']) if (row['unlock_real'] and 2*row['unlock_goal']-row['unlock_real']) >= 0 else 0, axis=1)
goal_states_df['goal-unlock'] = (goal_states_df['unlock_goal'] - goal_states_df['unlock_real']).apply(lambda x: 0 if x <= 0 else x)
goal_states_df['exceed-total_usage'] = (goal_states_df['total_usage_real'] - goal_states_df['total_usage_goal']).apply(lambda x: 0 if x <= 0 else x)
goal_states_df['real-total_usage'] = goal_states_df.apply(lambda row: min(row['total_usage_real'], 2*row['total_usage_goal']-row['total_usage_real']) if (row['total_usage_real'] and 2*row['total_usage_goal']-row['total_usage_real']) >= 0 else 0, axis=1)
goal_states_df['goal-total_usage'] = (goal_states_df['total_usage_goal'] - goal_states_df['total_usage_real']).apply(lambda x: 0 if x <= 0 else x)
goal_states_df['exceed-app_usage'] = (goal_states_df['app_usage_real'] - goal_states_df['app_usage_goal']).apply(lambda x: 0 if x <= 0 else x)
goal_states_df['real-app_usage'] = goal_states_df.apply(lambda row: min(row['app_usage_real'], 2*row['app_usage_goal']-row['app_usage_real']) if (row['app_usage_real'] and 2*row['app_usage_goal']-row['app_usage_real']) >= 0 else 0, axis=1)
goal_states_df['goal-app_usage'] = (goal_states_df['app_usage_goal'] - goal_states_df['app_usage_real']).apply(lambda x: 0 if x <= 0 else x)
goal_states_df = goal_states_df.fillna(-1, axis=1)

# 2023년 5월의 달력을 생성합니다.
year = 2023
month = 5
cal = calendar.monthcalendar(year, month)
today_day = 10


def get_goal_state(day): # 코드 고치기
    day_goal_state = goal_states_df[goal_states_df['day'] == day]
    if day_goal_state.size == 0 : return None
    day_goal_array = np.array(day_goal_state[[
        'exceed-unlock', 'real-unlock', 'goal-unlock',
        'exceed-total_usage','real-total_usage', 'goal-total_usage',
        'exceed-app_usage','real-app_usage','goal-app_usage'
    ]]).reshape(3, 3)
    for i in range(0, 3):
        if (day_goal_array[i][0] < 0):
            day_goal_array[i] = None
    return day_goal_array.tolist()

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
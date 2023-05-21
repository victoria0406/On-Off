import calendar
import dash
import datetime as dt
import pandas as pd
from dash import html, dcc
from inputdata.goalsettingdata import usage_time_info, unlock_info, app_usage_info
from component.todaygoal import today_goal_not_setting, get_goal_today, get_goal_state, today
from component.goaldonutplot import goal_donut_plot

month_to_string = ['', 'JAN.', 'Feb.', 'MAR.', 'APR.', 'MAY', 'JUN.', 'JUL.', 'AUG.', 'SEP.', 'OCT.', 'NOV.', 'DEC.']
calendar_sunday = calendar.Calendar(firstweekday=6)
# cal = calendar_sunday.monthdatescalendar(today.year, today.month)


# start_of_month = cal[0].index(1)
# prev_month_range = calendar.monthrange(year, month - 1);
# print(prev_month_range)
# for i in range(0, start_of_month):
#     cal[0][i] = prev_month_range[1] + 1 - start_of_month + i;
# start_of_next_month = cal[-1].index(0)
# print(start_of_next_month)
# for i in range(start_of_next_month, 7):
#     cal[-1][i] = i - start_of_next_month + 1

def get_calendar_donut_plot(date):
    if (date >= today): return None
    goal_state = get_goal_state(date)
    if goal_state == None : return None
    fig = goal_donut_plot(*goal_state)
    donut = dcc.Graph(figure = fig, config={'displayModeBar': False}, className='calendar-donut')
    return donut

# HTML 요소로 변환합니다.
def get_calendar(month):
    cal = calendar_sunday.monthdatescalendar(today.year, month)
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
                    html.P(str(date.day), style={'opacity': 0.6, 'font-weight': 'lighter'} if date.month != month else {}),
                    get_calendar_donut_plot(date)
                ], className='today' if (date == today) else ''
                , id='today-goal-status' if (date == today) else '')
                for date in week
            ])
            for week in cal
        ])
    ])
    component = html.Div([
        html.Div([
            html.Button('〈', id='prev-calender', disabled=True if month == 1 else False),
            html.P(f"{month_to_string[month]} {today.year}", style={'font-weight': 'bold'}),
            html.Button('〉', id='next-calender', disabled=True if month == 12 else False),
        ], id='month-title', key=str(month))
    , table], className='calendar-container')
    return component
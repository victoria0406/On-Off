import dash
import datetime as dt
from dash import html, dcc
from component.goaldonutplot import goal_donut_plot, week_donut_plot
from component.graph import usage_graph, unlock_graph, app_usage_graph
import pandas as pd
import numpy as np
from inputdata.data import unlocks as unlock_df, usage_time as app_usage_df
from inputdata.goalsettingdata import goal_states_resample, goal_states_df

today = pd.to_datetime(goal_states_resample.iloc[-1, :]['date']).date()
today_str = today.strftime("%Y-%m-%d")

today_df = app_usage_df.iloc[-1]
# print(today_df['Total'])
total_usage = today_df['Total']
def app_usage(app):
    return today_df[app]
unlock = unlock_df.iloc[-1].values[0]

color_info_component = html.Div([
    html.Div([html.Div("", className="square"),"Unlocks"], className="unlock"),
    html.Div([html.Div("", className="square"),"Total Usage Time"], className="usage"),
    html.Div([html.Div("", className="square"),"App Usage Time"], className="app"),
    html.Div([html.Div("", className="square"),"Exceed"], className="exceed"),
], className='today-goal-list goal-label')


def unlock_component(unlock_info, highlighted=None):
    data = unlock;
    component = html.Div([
        html.P('Unlocks', className='goal-title'),
        html.A([
            html.Img(src="./assets/icons/check-unlock.png", className='goal-state-check')
            if unlock_info['time'] >= data
            else html.Img(src="./assets/icons/close.png", className='goal-state-check exceed'),
            html.Span([html.B(data), f" / {unlock_info['time']} times ({(data / unlock_info['time'] * 100):.1f}%)"])
        ], className=f"goal-list {'active' if (highlighted == 'unlock') else ''}",
        href='/goal?setting=True' if (highlighted == 'unlock') else '/goal?setting=True?unlock')
    ], className="unlock")
    return component

def usage_time_component(usage_time_info, highlighted=None):
    data = float(total_usage) / 60;
    usage_goal_minute = float(usage_time_info['hour']) + float(usage_time_info['minute']) / 60
    component = html.Div([
        html.P('Usage Time',className='goal-title'),
        html.A([
            html.Img(src="./assets/icons/check-usage.png", className='goal-state-check')
            if usage_goal_minute >= data
            else html.Img(src="./assets/icons/close.png", className='goal-state-check exceed'),
            html.Span([html.B(round(data, 1)), f" / {usage_goal_minute} h ({(data / usage_goal_minute * 100):.1f}%)"])
        ], className= f"goal-list {'active' if (highlighted == 'usage') else ''}",
        href='/goal?setting=True' if (highlighted == 'usage') else '/goal?setting=True?usage')
    ], className="usage")
    return component

def app_usage_component(app_usage_info, highlighted=None):
    data = float(app_usage(app_usage_info['app'])) / 60;
    usage_goal_minute = float(app_usage_info['hour']) + float(app_usage_info['minute']) / 60
    component = html.Div([
        html.P(f"App Usage Time for {app_usage_info['app']}",className='goal-title'),
        html.A([
            html.Img(src="./assets/icons/check-app.png", className='goal-state-check')
            if usage_goal_minute > data
            else html.Img(src="./assets/icons/close.png", className='goal-state-check exceed'),
            html.Span([html.B(round(data, 1)), f" / {usage_goal_minute} h ({(data / usage_goal_minute * 100):.1f}%)"])
        ], className=f"goal-list {'active' if (highlighted == 'app') else ''}",
        href='/goal?setting=True' if (highlighted == 'app') else '/goal?setting=True?app')
    ], className="app")
    return component

def resample_goal(unlock_info, usage_time_info, app_usage_info):
    print(unlock_info, usage_time_info, app_usage_info)
    return_data = [None, None, None];
    if (unlock_info['checked']):
        exceed = max(unlock - unlock_info['time'], 0)
        real = max(min(unlock, 2 * unlock_info['time'] - unlock), 0)
        goal = max(0, unlock_info['time']-unlock)
        return_data[0] = [exceed, real, goal]
    if (usage_time_info['checked']):
        usage_by_m = usage_time_info['hour'] * 60 + usage_time_info['minute'];
        exceed = max(total_usage - usage_by_m, 0)
        real = max(0, min(total_usage, 2 * usage_by_m - total_usage))
        goal = max(0, usage_by_m-total_usage)
        return_data[1] = [exceed, real, goal]
    if (app_usage_info['checked']):
        app_usage_by_m = app_usage_info['hour'] * 60 + app_usage_info['minute'];
        today_app_usage = app_usage(app_usage_info['app'])
        exceed = max(today_app_usage - app_usage_by_m, 0)
        real = max(0, min(today_app_usage, 2 * app_usage_by_m - today_app_usage))
        goal = max(0, app_usage_by_m-today_app_usage)
        return_data[2] = [exceed, real, goal]
    print(return_data)
        
    return return_data
def resample_goal_index(data, index):
    if (data['checked'] and index == 0):
        exceed = max(unlock - data['time'], 0)
        real = max(min(unlock, 2 * data['time'] - unlock), 0)
        goal = max(0, data['time']-unlock)
        return [exceed, real, goal]
    if (data['checked'] and index == 1):
        usage_by_m = data['hour'] * 60 + data['minute'];
        exceed = max(total_usage - usage_by_m, 0)
        real = max(0, min(total_usage, 2 * usage_by_m - total_usage))
        goal = max(0, usage_by_m-total_usage)
        return [exceed, real, goal]
    if (data['checked'] and index == 2):
        app_usage_by_m = data['hour'] * 60 + data['minute'];
        today_app_usage = app_usage(data['app'])
        exceed = max(today_app_usage - app_usage_by_m, 0)
        real = max(0, min(today_app_usage, 2 * app_usage_by_m - today_app_usage))
        goal = max(0, app_usage_by_m-today_app_usage)
        return [exceed, real, goal]
    return None

def today_goal_setting(unlock_info, usage_time_info, app_usage_info, highlighted=None):
    return_children = [html.P('Today Goal', style={'font-weight': 'bold'})]
    fig = goal_donut_plot(*(resample_goal(unlock_info, usage_time_info, app_usage_info)), highlighted)
    return_children.append(dcc.Graph(figure = fig, config={'displayModeBar': False}, className='today-goal-fig'))
    return_children.append(color_info_component)
    goal_list = []
    if unlock_info['checked']:
        goal_list.append(unlock_component(unlock_info, highlighted))
    if usage_time_info['checked']:
        goal_list.append(usage_time_component(usage_time_info, highlighted))
    if app_usage_info['checked']:
        goal_list.append(app_usage_component(app_usage_info, highlighted))
    return_children.append(html.Div(goal_list, className="today-goal-list"))
    return return_children


# 날짜는 오늘 이전만 사용 가능!
def get_goal_state(date):
    # print(date)
    day_goal_state = goal_states_resample[goal_states_resample['date'] == date.strftime("%Y-%m-%d")]
    if day_goal_state.size == 0 : return None
    day_goal_array = np.array(day_goal_state[[
        'exceed-unlock', 'real-unlock', 'goal-unlock',
        'exceed-total_usage','real-total_usage', 'goal-total_usage',
        'exceed-app_usage','real-app_usage','goal-app_usage'
    ]]).reshape(3, 3).tolist()
    for i in range(0, 3):
        if (day_goal_array[i][0] < 0):
            day_goal_array[i] = None
    return day_goal_array

def raw_goal_today(data, index):
    if (index == 0):
        return [unlock, data['time']]
    elif (index == 1):
        return [total_usage, data['hour'] * 60 + data['minute']]
    elif (index == 2):
        return [app_usage(data['app']), data['hour'] * 60 + data['minute']]
    return [None, None]

def raw_goal_state(date):
    if (date > today) : return None
    day_goal_state = goal_states_df[goal_states_df['date'] == date.strftime('%Y-%m-%d')]
    if day_goal_state.size == 0 : return None
    day_goal_array = np.array(day_goal_state[[
        'unlock_real', 'unlock_goal',
        'total_usage_real', 'total_usage_goal',
        'app_usage_real', 'app_usage_goal'
    ]]).reshape(3, 2).tolist()
    for i in range(0, 3):
        if (day_goal_array[i][0] < 0):
            day_goal_array[i] = None
    return day_goal_array

def convert_time(minute):
    if minute >= 60:
        if minute % 60 != 0: return str(minute // 60)+"h "+str(minute % 60)+"m"
        else: return str(minute // 60)+"h"
    else: return str(minute % 60)+"m"

# date는 오늘 이전만

def get_calendar_donut_plot_today(today_data, index):
    goal_state = resample_goal_index(today_data, index)
    fig = week_donut_plot(goal_state, index)
    if (goal_state):
        [real_data, goal_data] = raw_goal_today(today_data, index)
        if index == 2: colors = ['#B40000','#686986', '#68698650']
        elif index == 1: colors = ['#B40000','#A4BD85', '#A4BD8550']
        elif index == 0: colors = ['#B40000','#E4AE44', '#E4AE4450']
        fig.add_annotation(
            text="<b>"+convert_time(int(real_data))+"<b>"+"<br> " if index == 1 or index == 2 else "<b>"+str(int(real_data))+"<b>"+"<br> ",
            showarrow=False,
            font=dict(
                size=14,
                color=colors[1],
            )
        )
        fig.add_annotation(
            text=" "+"<br>/ "+convert_time(int(goal_data)) if index == 1 or index == 2 else " "+"<br>/ "+str(int(goal_data)),
            showarrow=False, 
            font=dict(
                size=12,
                color=colors[1]
            )
        )
    donut = dcc.Graph(figure = fig, config={'displayModeBar': False}, className='calendar-donut')
    return donut

def get_calendar_donut_plot(date, index):
    if (date > today): return None
    goal_state = get_goal_state(date)
    # print(goal_state)
    if goal_state == None : return None
    fig = week_donut_plot(goal_state[index], index)
    if (goal_state[index] != None):
        [real_data, goal_data] = raw_goal_state(date)[index]
        if index == 2: colors = ['#B40000','#686986', '#68698650']
        elif index == 1: colors = ['#B40000','#A4BD85', '#A4BD8550']
        elif index == 0: colors = ['#B40000','#E4AE44', '#E4AE4450']
        fig.add_annotation(
            text="<b>"+convert_time(int(real_data))+"<b>"+"<br> " if index == 1 or index == 2 else "<b>"+str(int(real_data))+"<b>"+"<br> ",
            showarrow=False,
            font=dict(
                size=14,
                color=colors[1],
            )
        )
        fig.add_annotation(
            text=" "+"<br>/ "+convert_time(int(goal_data)) if index == 1 or index == 2 else " "+"<br>/ "+str(int(goal_data)),
            showarrow=False, 
            font=dict(
                size=12,
                color=colors[1]
            )
        )
    donut = dcc.Graph(figure = fig, config={'displayModeBar': False}, className='calendar-donut')
    return donut


def unlock_weekly_calendar(today_data, highlighted=None):
    date_list = [today - dt.timedelta(days=x) for x in range(7)]
    date_list.reverse()
    
    table = html.Table(className=f'weekly-calendar', children=[
        html.Thead(children=[
            html.Tr(children=[
                html.Th(str(day.month)+"/"+str(day.day), 
                        style={'color': '#FF6F66'} if (day.weekday() == 6) else ({'color': '#FDB03D'} if (day.weekday() == 5) else {}))
                for day in date_list
            ])
        ]),
        html.Tbody(children=[
            html.Tr(children=[
                html.Td(children=[
                    get_calendar_donut_plot(day, 0) if (day != today) else get_calendar_donut_plot_today(today_data, 0)
                ], className='today' if (day == today) else '' )
                for day in date_list
            ])
        ])
    ])
    
    return_children = [
        html.Div([html.P('Your Weekly - Unlock', className='weekly-calendar-title'), table],
                    className='weekly-calendar-container',),
        html.Div(children=[
            html.P('Unlock', style={'font-size': '20px'}),
            html.Div(dcc.Graph(figure = unlock_graph(today_data), config={'displayModeBar': False}),style={'margin-top':'-90px'})
        ], className='weekly-graph-container')
    ]
    return return_children

def usage_weekly_calendar(today_data, highlighted=None):
    date_list = [today - dt.timedelta(days=x) for x in range(7)]
    date_list.reverse()
    
    table = html.Table(className=f'weekly-calendar', children=[
        html.Thead(children=[
            html.Tr(children=[
                html.Th(str(day.month)+"/"+str(day.day), 
                        style={'color': '#FF6F66'} if (day.weekday() == 6) else ({'color': '#FDB03D'} if (day.weekday() == 5) else {}))
                for day in date_list
            ])
        ]),
        html.Tbody(children=[
            html.Tr(children=[
                html.Td(children=[
                    get_calendar_donut_plot(day, 1) if (day != today) else get_calendar_donut_plot_today(today_data, 1)
                ], className='today' if (day == today) else '' )
                for day in date_list
            ])
        ])
    ])
    
    return_children = [
        html.Div([html.P('Your Weekly - Usage Time', className='weekly-calendar-title'), table],
                    className='weekly-calendar-container',),
        html.Div(children=[
            html.P('Usage Time', style={'font-size': '20px'}),
            html.Div(dcc.Graph(figure = usage_graph(today_data), config={'displayModeBar': False},style={'margin-top':'-60px'})),
        ], className='weekly-graph-container')
    ]
    return return_children

def app_weekly_calendar(today_data, highlighted=None):
    date_list = [today - dt.timedelta(days=x) for x in range(7)]
    date_list.reverse()
    
    table = html.Table(className=f'weekly-calendar', children=[
        html.Thead(children=[
            html.Tr(children=[
                html.Th(str(day.month)+"/"+str(day.day), 
                        style={'color': '#FF6F66'} if (day.weekday() == 6) else ({'color': '#FDB03D'} if (day.weekday() == 5) else {}))
                for day in date_list
            ])
        ]),
        html.Tbody(children=[
            html.Tr(children=[
                html.Td(children=[
                    get_calendar_donut_plot(day, 2) if (day != today) else get_calendar_donut_plot_today(today_data, 2)
                ], className='today' if (day == today) else '' )
                for day in date_list
            ])
        ])
    ])
    
    return_children = [
        html.Div([html.P('Your Weekly - App Usage Time', className='weekly-calendar-title'), table],
                    className='weekly-calendar-container',),
        html.Div(children=[
            html.P('App Usage', style={'font-size': '20px'}),
            html.Div(dcc.Graph(figure = app_usage_graph(today_data), config={'displayModeBar': False},style={'margin-top':'-60px'})),
        ], className='weekly-graph-container')
    ]
    return return_children

today_goal_not_setting = [
    html.P('Set Your Goal', style={'font-weight': 'bold'}),
    html.A('+', className='set-goal-button',href='/goal/setting'),
    color_info_component,
    html.Div([
        html.Div([
            html.Img(src="./assets/icons/info.png", style={"height": "24px", "width": "24px"}),
            html.P('INFO', style={"font-weight": "600", "margin-left": "6px", "font-size": "20px", "line-height": "20px"}) 
        ], style={'display': 'flex', "color": "#515151"}),
        html.P(['You could set daily goals.',html.Br(),'Once you set your goal for the day, you cannot change it.'], style={"font-size": "14px"}),
    ], className="today-goal-info")
]
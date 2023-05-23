import pandas as pd
goal_states_df= pd.read_csv('./data/goal_states.csv')
goal_states_df['day'] = pd.to_datetime(goal_states_df['date']).dt.day

last_goal = goal_states_df[goal_states_df['day'] == 6]
last_goal = last_goal.fillna(-1, axis=1)
unlock = last_goal['unlock_goal'].values[0]
usage = last_goal['total_usage_goal'].values[0]
goal_app = last_goal['app_usage_app'].values[0]
if goal_app == -1:
    app_usage_df = pd.read_csv('./data/usage_time.csv')
    goal_app = app_usage_df.columns[2]
app_usage = last_goal['app_usage_goal'].values[0]

usage_time_info = {
    'checked': False if usage < 0 else True,
    'hour': 0 if usage < 0 else usage // 60,
    'minute': 0 if usage < 0 else usage % 60,
}

unlock_info = {
    'checked': False if unlock < 0 else True,
    'time': 0 if unlock < 0 else unlock,
}

app_usage_info = {
    'checked': False if app_usage < 0 else True,
    'app': goal_app,
    'hour': 0 if app_usage < 0 else app_usage // 60,
    'minute': 0 if app_usage < 0 else app_usage % 60,
}

def get_usage_time_info():
    return usage_time_info
def get_unlock_info():
    return unlock_info
def get_app_usage_info():
    return app_usage_info
import pandas as pd
goal_states_df= pd.read_csv('./data/goal_states.csv')
goal_states_resample = pd.DataFrame();

def update_goal_states_resample():
    goal_states_resample = pd.DataFrame();
    ## goal_states_df = goal_states_df.fillna(-1, axis=1)
    goal_states_resample['date'] = goal_states_df['date']
    goal_states_resample['exceed-unlock'] = (goal_states_df['unlock_real'] - goal_states_df['unlock_goal']).apply(lambda x: 0 if x <= 0 else x)
    goal_states_resample['real-unlock'] = goal_states_df.apply(lambda row: min(row['unlock_real'], 2*row['unlock_goal']-row['unlock_real']) if (row['unlock_real'] and 2*row['unlock_goal']-row['unlock_real']) >= 0 else 0, axis=1)
    goal_states_resample['goal-unlock'] = (goal_states_df['unlock_goal'] - goal_states_df['unlock_real']).apply(lambda x: 0 if x <= 0 else x)
    goal_states_resample['exceed-total_usage'] = (goal_states_df['total_usage_real'] - goal_states_df['total_usage_goal']).apply(lambda x: 0 if x <= 0 else x)
    goal_states_resample['real-total_usage'] = goal_states_df.apply(lambda row: min(row['total_usage_real'], 2*row['total_usage_goal']-row['total_usage_real']) if (row['total_usage_real'] and 2*row['total_usage_goal']-row['total_usage_real']) >= 0 else 0, axis=1)
    goal_states_resample['goal-total_usage'] = (goal_states_df['total_usage_goal'] - goal_states_df['total_usage_real']).apply(lambda x: 0 if x <= 0 else x)
    goal_states_resample['exceed-app_usage'] = (goal_states_df['app_usage_real'] - goal_states_df['app_usage_goal']).apply(lambda x: 0 if x <= 0 else x)
    goal_states_resample['real-app_usage'] = goal_states_df.apply(lambda row: min(row['app_usage_real'], 2*row['app_usage_goal']-row['app_usage_real']) if (row['app_usage_real'] and 2*row['app_usage_goal']-row['app_usage_real']) >= 0 else 0, axis=1)
    goal_states_resample['goal-app_usage'] = (goal_states_df['app_usage_goal'] - goal_states_df['app_usage_real']).apply(lambda x: 0 if x <= 0 else x)
    goal_states_resample = goal_states_resample.fillna(-1, axis=1)
    return goal_states_resample
goal_states_resample = update_goal_states_resample()

def update_goal_df():
    print('update')
    goal_states_df.iloc[-2]['total_usage_goal'] = 10000000
    return goal_states_df
    

last_goal = goal_states_df.iloc[-1]
last_goal = last_goal.fillna(-1)
print(last_goal['unlock_real'])
unlock = last_goal['unlock_goal']
usage = last_goal['total_usage_goal']
goal_app = last_goal['app_usage_app']
if goal_app == -1:
    app_usage_df = pd.read_csv('./data/usage_time.csv')
    goal_app = app_usage_df.columns[2]
app_usage = last_goal['app_usage_goal']

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
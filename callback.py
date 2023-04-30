from dash.dependencies import Input, Output
from dash import html
from inputdata.goalsettingdata import usage_time_info, unlock_info, app_usage_info

def selected_app_callback_factory():
    output = Output('selected-app', 'children'),
    input = Input('app-dropdown', 'value'),
    def update_output(value):
        return [value]
    
    return [
        output,
        input,
        update_output
    ]
    
plus_layout = html.Div([
'+'
], className="custom-checkbox plus")
minus_layout = html.Div([
    '-'
], className="custom-checkbox minus")
    
def usage_time_switch_callback_factory():
    output=[
        Output('goal-switch-output-usage-time', 'children'),
        Output('goal-switch-disable-usage-time-1', 'disabled'),
        Output('goal-switch-disable-usage-time-2', 'disabled'),
        Output('goal-setting-list-container-usage-time', 'className'),
    ]
    input=Input('goal-switch-input-usage-time', 'value')
    def update_output(value):
        if 'on' in value:
            usage_time_info['checked'] = True;
            return [[plus_layout], False, False, 'goal-setting-list-container active']
        else:
            usage_time_info['checked'] = False;
            return [[minus_layout], True, True, 'goal-setting-list-container']
        
    return [
        output,
        input,
        update_output
    ]
def unlock_switch_callback_factory():
    output=[
        Output('goal-switch-output-unlock', 'children'),
        Output('goal-switch-disable-unlock-1', 'disabled'),
        Output('goal-setting-list-container-unlock', 'className'),
    ]
    input=Input('goal-switch-input-unlock', 'value')
    def update_output(value):
        if 'on' in value:
            unlock_info['checked'] = True;
            return [[plus_layout], False, 'goal-setting-list-container active']
        else:
            unlock_info['checked'] = False;
            return [[minus_layout], True, 'goal-setting-list-container']
        
    return [
        output,
        input,
        update_output
    ]
def app_usage_switch_callback_factory():
    output=[
        Output('goal-switch-output-app-usage', 'children'),
        Output('app-dropdown', 'disabled'),
        Output('goal-switch-disable-app-usage-2', 'disabled'),
        Output('goal-switch-disable-app-usage-3', 'disabled'),
        Output('goal-setting-list-container-app-usage', 'className'),
    ]
    input=Input('goal-switch-input-app-usage', 'value')
    def update_output(value):
        if 'on' in value:
            app_usage_info['checked'] = True;
            return [[plus_layout], False, False, False, 'goal-setting-list-container active']
        else:
            app_usage_info['checked'] = False;
            return [[minus_layout], True, True, True, 'goal-setting-list-container']
        
    return [
        output,
        input,
        update_output
    ]
    
def get_callbacks():
    return [
        selected_app_callback_factory(),
        usage_time_switch_callback_factory(),
        unlock_switch_callback_factory(),
        app_usage_switch_callback_factory(),
    ]
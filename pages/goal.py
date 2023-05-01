import dash
from dash import html, dcc, callback, Input, Output
from inputdata.goalsettingdata import usage_time_info, unlock_info, app_usage_info


dash.register_page(__name__)

def component():
    usage_time_component = html.Div(
        f"usage_time_info: {usage_time_info['hour']}h {usage_time_info['minite']}m",
    )
    unlock_component = html.Div(
        f"unlock_info: {unlock_info['time']}times",
    )
    app_usage_component = html.Div(
        f"app_time_info for {app_usage_info['app']}: {app_usage_info['hour']}h {app_usage_info['minite']}m",
    )
    return_children = []
    if usage_time_info['checked']:
        return_children.append(usage_time_component)
    if unlock_info['checked']:
        return_children.append(unlock_component)
    if app_usage_info['checked']:
        return_children.append(app_usage_component)
    return return_children



layout = html.Div(children=[
    html.A('Set Goal', className='link-button goal-setting main',href='/goalsetting'),
    html.Div(children='hihi', id='today-goal')
])
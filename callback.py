import dash
from dash.dependencies import Input, Output, State
    
def goal_update_sidebar_callback_factory():
    output=Output('goal-link', 'href')
    input=Input('url', 'pathname')
    state=State('url', 'search')
    def update_output(pathname, search):
        if pathname == '/goal' and search == '?setting=True':
            # print(pathname, search)
            return '/goal?setting=True'
        else:  return dash.no_update
    return [
        update_output,
        output,
        input,
        state,
    ]
    
def update_mention_header_callback_factory():
    output = Output('header-mention', 'children')
    input=Input('url', 'pathname')
    def update_output(pathname):
        if pathname == '/goal' or pathname == '/goal/setting':
            return 'Set goal to use your phone well!'
        elif pathname == '/report/group':
            return 'Compare your usage with others :)'
        elif pathname == '/report/weekly':
            return 'Let’s check your phone usage this week!'
        elif pathname == '/report':
            return 'Let’s check your phone usage today!'
        else : return 'Hello'
    return [
        update_output,
        output,
        input,
    ]
    
def get_callbacks():
    return [
        goal_update_sidebar_callback_factory(),
        update_mention_header_callback_factory(),
    ]
import plotly.graph_objects as go

fig = go.Figure()

# 첫번째 layer
fig.add_trace(go.Pie(
    values=[20, 40, 60, 80],
    marker=dict(colors=['red', 'orange', 'yellow', 'green']),
    hole=0.6,  # hole 조절
    domain=dict(x=[0.3, 0.7], y=[0.3, 0.7]),  # domain 조절
    name='Layer 1'
 ))

# 두번째 layer
fig.add_trace(go.Pie(
    values=[30, 50, 70],
    marker=dict(colors=['purple', 'blue', 'lightblue']),
    hole=0.75,
    domain=dict(x=[0.15, 0.85], y=[0.15, 0.85]),
    name='Layer 2'
))

# 세번째 layer
fig.add_trace(go.Pie(
    values=[10, 20, 30, 40],
    marker=dict(colors=['pink', 'brown', 'gray', 'black']),
    hole=0.85,
    domain=dict(x=[0, 1], y=[0, 1]),
    name='Layer 3'
))

def goal_donut_plot(unlock_data, usage_data, app_usage_data):
    fig = go.Figure()
    if (app_usage_data != None):
        print(app_usage_data)
        fig.add_trace(go.Pie(
        values=app_usage_data,
        marker=dict(colors=['#B40000','#686986', '#68698650']),
        hole=0.85,
        sort=False,
        domain=dict(x=[0, 1], y=[0, 1]),
        direction='clockwise'
        ))
    if (usage_data != None):
        fig.add_trace(go.Pie(
        values=usage_data,
        marker=dict(colors=['#B40000','#A4BD85', '#A4BD8550']),
        hole=0.75,
        sort=False,
        domain=dict(x=[0.15, 0.85], y=[0.15, 0.85]),
        direction='clockwise'
        ))
    if (unlock_data != None):
        fig.add_trace(go.Pie(
        values=unlock_data,
        marker=dict(colors=['#B40000','#E4AE44', 'E4AE4450']),
        hole=0.6,  # hole 조절
        sort=False,
        domain=dict(x=[0.3, 0.7], y=[0.3, 0.7]),  # domain 조절
        direction='clockwise'
        ))
    fig.update_traces(textinfo='none')
    return fig

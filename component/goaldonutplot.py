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

def goal_donut_plot(unlock_data, usage_data, app_usage_data, highlighted = None):
    # print(highlighted)
    fig = go.Figure()
    if (app_usage_data != None):
        fig.add_trace(go.Pie(
        values=app_usage_data,
        marker=dict(colors=['#B40000','#686986', '#68698650']),
        hole=0.85,
        sort=False,
        domain=dict(x=[0, 1], y=[0, 1]),
        direction='clockwise',
        opacity=1 if ((highlighted == None) or (highlighted == 'app')) else 0.3,
        ))
    if (usage_data != None):
        fig.add_trace(go.Pie(
        values=usage_data,
        marker=dict(colors=['#B40000','#A4BD85', '#A4BD8550']),
        hole=0.75,
        sort=False,
        domain=dict(x=[0.15, 0.85], y=[0.15, 0.85]),
        direction='clockwise',
        opacity=1 if ((highlighted == None) or (highlighted == 'usage')) else 0.3,
        ))
    if (unlock_data != None):
        fig.add_trace(go.Pie(
        values=unlock_data,
        marker=dict(colors=['#B40000','#E4AE44', 'E4AE4450']),
        hole=0.6,  # hole 조절
        sort=False,
        domain=dict(x=[0.3, 0.7], y=[0.3, 0.7]),  # domain 조절
        direction='clockwise',
        opacity=1 if ((highlighted == None) or (highlighted == 'unlock')) else 0.3,
        ))
    fig.update_traces(textinfo='none')
    fig.update_layout(showlegend=False, plot_bgcolor='rgb(0,0,0,0)',paper_bgcolor="rgb(0,0,0,0)",)
    return fig

def week_donut_plot(data, index):
    fig = go.Figure()
    if index == 2: colors = ['#B40000','#686986', '#68698650']
    elif index == 1: colors = ['#B40000','#A4BD85', '#A4BD8550']
    elif index == 0: colors = ['#B40000','#E4AE44', '#E4AE4450']

    if data == None:
        fig.add_shape(
            type="circle",
            xref="x", yref="y",
            x0=-0.3, y0=-1, x1=5.3, y1=4,
            line=dict(
                color=colors[1],
                dash="dot"
            ))
        fig.update_layout(plot_bgcolor='rgb(0,0,0,0)',
                        paper_bgcolor="rgb(0,0,0,0)",
                        width=260,
                        height=260,
                        xaxis={
                            'visible': False
                        },
                        yaxis={
                            'visible': False
                        }
                        )
    else:
        fig.add_trace(go.Pie(
            values=data,
            marker=dict(colors=colors),
            hole=0.7,
            sort=False,
            domain=dict(x=[0, 1], y=[0, 1]),
            direction='clockwise',
            opacity=1
            ))
        fig.update_traces(textinfo='none')
    return fig
## 위쪽 코드 해석
# 초과하기 않을 때: 총 사용량 = data[1] / 목표 사용량 = (목표 사용량 - 총 사용량 = data[2]) + (총 사용량 = data[1]) (이때 data[0] = 0)
# 초과할 때: 총 사용량 = (총 사용량 - 목표 사용량 = data[0]) + (목표 사용량 = data[1])  목표 사용량 = data[1] (이때 data[2] = 0)
# 2배 이상 초과할 때 = 
# 일반화하면 총 사용량 = data[0] + data[1] 목표 사용량 = data[1] + data[2]
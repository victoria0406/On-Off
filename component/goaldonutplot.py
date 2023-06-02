import plotly.graph_objects as go
labels = ['exceed', 'used', 'rest']

def goal_donut_plot(unlock_data, usage_data, app_usage_data, highlighted = None):
    print(unlock_data, usage_data, app_usage_data)
    if unlock_data == [None, None, None]: unlock_data = None
    if usage_data == [None, None, None]: usage_data = None
    if app_usage_data == [None, None, None]: app_usage_data = None
    for i in range(0, 3):
        if unlock_data != None: unlock_data[i] /=60;
        if usage_data != None: usage_data[i] /=60;
        if app_usage_data != None: app_usage_data[i] /=60;
    
    fig = go.Figure()
    if (app_usage_data != None):
        fig.add_trace(go.Pie(
        values=app_usage_data,
        labels=labels,
        marker=dict(colors=['#B40000','#686986', '#68698650']),
        hole=0.85,
        sort=False,
        domain=dict(x=[0, 1], y=[0, 1]),
        direction='clockwise',
        opacity=1 if ((highlighted == None) or (highlighted == 'app')) else 0.3,
        text=["App Usage Time", "App Usage Time", "App Usage Time"]
        ))
    else:
        fig.add_shape(
            type="circle",
            xref="paper", yref="paper",
            x0=0.05, y0=0.05, x1=0.95, y1=0.95,
            line=dict(
                color='#686986',
                dash="dot"
            ))
    if (usage_data != None):
        fig.add_trace(go.Pie(
        values=usage_data,
        labels=labels,
        marker=dict(colors=['#B40000','#A4BD85', '#A4BD8550']),
        hole=0.75,
        sort=False,
        domain=dict(x=[0.15, 0.85], y=[0.15, 0.85]),
        direction='clockwise',
        opacity=1 if ((highlighted == None) or (highlighted == 'usage')) else 0.3,
        text=["Total Usage Time","Total Usage Time","Total Usage Time"]
        ))
    else:
        fig.add_shape(
            type="circle",
            xref="paper", yref="paper",
            x0=0.2, y0=0.2, x1=0.8, y1=0.8,
            line=dict(
                color='#A4BD85',
                dash="dot"
            ))
    if (unlock_data != None):
        fig.add_trace(go.Pie(
        values=unlock_data,
        labels=labels,
        marker=dict(colors=['#B40000','#E4AE44', 'E4AE4450']),
        hole=0.6,  # hole 조절
        sort=False,
        domain=dict(x=[0.3, 0.7], y=[0.3, 0.7]),  # domain 조절
        direction='clockwise',
        opacity=1 if ((highlighted == None) or (highlighted == 'unlock')) else 0.3,
        text=["Unlocks", "Unlocks", "Unlocks"]
        ))
    else:
        fig.add_shape(
            type="circle",
            xref="paper", yref="paper",
            x0=0.36, y0=0.36, x1=0.64, y1=0.64,
            line=dict(
                color='#E4AE44',
                dash="dot"
            ),
            )
    fig.update_traces(
        textinfo='none',
        hovertemplate='%{text}<br>%{label}:%{value:.1f}(h)<extra></extra>',
    )
    fig.update_layout(
        margin_l=12,
        margin_r=12,
        margin_b=12,
        margin_t=12,
        showlegend=False,
        plot_bgcolor='rgb(0,0,0,0)',
        paper_bgcolor="rgb(0,0,0,0)",
        hoverlabel_font_size=12,
        )
    return fig

def convert_time(minute):
    if minute >= 60:
        if minute % 60 != 0: return str(minute // 60)+"h "+str(minute % 60)+"m"
        else: return str(minute // 60)+"h"
    else: return str(minute % 60)+"m"

def week_donut_plot(data, index):
    fig = go.Figure()
    if index == 2: colors = ['#B40000','#686986', '#68698650']
    elif index == 1: colors = ['#B40000','#A4BD85', '#A4BD8550']
    elif index == 0: colors = ['#B40000','#E4AE44', '#E4AE4450']
    text=['Unlocks', 'Total Usage Time', 'App Usage Time']
    
    if data == None:
        fig.add_shape(
            type="circle",
            xref="x", yref="y",
            x0=0, y0=-0, x1=1, y1=1,
            line=dict(
                color=colors[1],
                dash="dot"
            ))
        fig.update_layout(plot_bgcolor='rgb(0,0,0,0)',
                        paper_bgcolor="rgb(0,0,0,0)",
                        xaxis={
                            'visible': False
                        },
                        yaxis={
                            'visible': False
                        }
                        )
    else:
        for i in range(0, 3):
            data[i]/=60;
        fig.add_trace(go.Pie(
            values=data,
            marker=dict(colors=colors),
            hole=0.7,
            sort=False,
            domain=dict(x=[0, 1], y=[0, 1]),
            direction='clockwise',
            opacity=1,
            labels=labels,
            text=[text[index] for i in range(0, 3)]
            ))
        fig.update_traces(
            textinfo='none',
            hovertemplate='%{text}<br>%{label}:%{value:.1f}(h)<extra></extra>',
        )
        fig.update_layout(showlegend=False, 
                        plot_bgcolor='rgb(0,0,0,0)',
                        paper_bgcolor="rgb(0,0,0,0)",
                        margin_l=12,
                        margin_r=12,
                        margin_b=12,
                        margin_t=12,
                        # annotations=[dict(text=str(int(data[1]))+"<br>/"+str(int(data[2])), showarrow=False)]
                        )
    return fig
## 위쪽 코드 해석
# 초과하기 않을 때: 총 사용량 = data[1] / 목표 사용량 = (목표 사용량 - 총 사용량 = data[2]) + (총 사용량 = data[1]) (이때 data[0] = 0)
# 초과할 때: 총 사용량 = (총 사용량 - 목표 사용량 = data[0]) + (목표 사용량 = data[1])  목표 사용량 = data[1] (이때 data[2] = 0)
# 2배 이상 초과할 때 = 
# 일반화하면 총 사용량 = data[0] + data[1] 목표 사용량 = data[1] + data[2]
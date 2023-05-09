import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

user_square_style = {
    'width': '20px',
    'height': '20px',
    'background-color': '#A7A8C1'
}

others_square_style = {
    'width': '20px',
    'height': '20px',
    'background-color': '#F8D294'
}

col_style = {
    'background-color': '#f8f9fa',
    'border-radius': '10px',
    'padding': '16px',
    'display': 'flex',
    'flex-direction': 'row',
}

col_item_style = {
    'display': 'flex',
    'flex-direction': 'row',
}

button_style = {
    'margin' : '-4.5rem 2rem 1.5rem 0',
    'width' : '15rem',
    'float': 'right',
    'background-color': '#EBEBF0',
    'color': '#000',
    'text-align': 'center',
    'border-radius': '5px',
    'height': '40px',
    'border': 'none'
}

menu_style = {
    'margin' : '-4.5rem -7rem 0 0',
    'width' : '20rem',
    'background-color': '#EBEBF0',
    'text-align': 'center',
    'border-radius': '5px',
    'height': '40px',
    "float":"right",
    'border': 'none',
    'display': 'flex',
    'justify-content': 'center'
}

content_style = {
    'display': 'flex',
    "background-color": "#FFFFFF",
    "height": "21rem",
    "border-radius": "5px",
    'margin-left': '1rem',
    "margin-bottom": '1rem',
}

graph_wrapper = {
	'display': 'flex',
}

child_classes = 'm-2'

# Load data
group_df = pd.read_csv('datas/total_user_usage.csv')

# Get your usage and session duration times
your_id = 2
your_ust = group_df.loc[your_id, 'usage_time']
your_sdt = group_df.loc[your_id, 'session_duration_time']

# Get group mean and median values
min_ust = group_df['usage_time'].min()
max_ust = group_df['usage_time'].max()
min_sdt = group_df['session_duration_time'].min()
max_sdt = group_df['session_duration_time'].max()
group_ust_mean = group_df["usage_time"].mean()
group_ust_median = group_df['usage_time'].median()
group_sdt_mean = group_df["session_duration_time"].mean()
group_sdt_median = group_df['session_duration_time'].median()

# Set range of axis
xlb, xrb = -100, max_ust*1.2
ybb, ytb = -10, max_sdt*1.2
xlim = [xlb, xrb]
ylim = [ybb, ytb]

# Define plot colorscale
color_2d = [[0, 'rgb(255,255,255)'], [1.0, 'rgb(252,156,26)']]

# Create histogram plot
fig1 = go.Figure(go.Histogram2dContour(
                    x = group_df["usage_time"],
                    y = group_df["session_duration_time"],
                    colorscale=color_2d,
                    showscale=False,
                    ))
fig1.update_traces(contours_showlines=False, legendwidth=400)


# Define group names and colors
group_names = ["RISK", "SPRINT", "SAFE", "ON/OFF"]
group_colors = ['rgba(50,50,50,0.3)', 'rgba(50,50,50,0.3)', 'rgba(50,50,50,0.3)', 'rgba(50,50,50,0.3)']
size = [25, 25, 25, 25]

# Determine the group that the user belongs to based on usage time and session duration time medians
if your_sdt > group_sdt_median:
    if your_ust > group_ust_median:
        user_group_index = 0  # RISK
    else:
        user_group_index = 1  # SPRINT
else:
    if your_ust > group_ust_median:
        user_group_index = 3  # ON/OFF
    else:
        user_group_index = 2  # SAFE

# Add the group names to the plot
x = [(group_ust_median + xrb)/2, (group_ust_median + xlb)/2, (group_ust_median + xlb)/2, (group_ust_median + xrb)/2]
y = [(group_sdt_median + ytb)/2, (group_sdt_median + ytb)/2, (group_sdt_median + ybb)/2, (group_sdt_median + ybb)/2]
size[user_group_index] = 45
group_colors[user_group_index] = 'rgba(255,130,0,0.8)'
texts = ['<b>' + group_names[i] + '</b>' if i == user_group_index else group_names[i] for i in range(4)]
fig1.add_trace(go.Scatter(x=x, y=y, mode='text', text=texts, textposition='middle center',
                           textfont_size=size, textfont_family='Sherif', textfont_color=group_colors,
                           showlegend=False))

x0 = [group_ust_median, xlb, xlb, group_ust_mean]
y0 = [group_sdt_median, group_sdt_median, ybb, ybb]
x1 = [xrb, group_ust_median, group_ust_median, xrb]
y1 = [ytb, ytb, group_sdt_median, group_sdt_median]

# Add rectangular shape
fig1.add_shape(type='rect', xref='x', yref='y',
               x0=x0[user_group_index], y0=y0[user_group_index],
               x1=x1[user_group_index], y1=y1[user_group_index],
               fillcolor="#A7A8C1", opacity=0.3, line=dict(width=0))

# Add your marker and median lines
fig1.add_trace(go.Scatter(x=[your_ust], y=[your_sdt], mode='markers+text', 
                          text=["<b>You</b>"], textposition="bottom center",
                          textfont=dict(family="Arial", size=15, color="#10135B"),
                          marker=dict(color='#10135B', size=10)))
fig1.add_vline(x=group_ust_median, line_dash="dot", line_color="#7C6542", line_width=1)
fig1.add_hline(y=group_sdt_median, line_dash="dot", line_color="#7C6542", line_width=1)

# Define plot layout
fig1.update_layout(
    title="your group: RISK Group",
    width=488, height=336,
    showlegend=False,
    hovermode=False,
    xaxis={
        'automargin': True,
        'title': {
            'text': 'Usage Time (m)',
            'font': {'family': 'Arial', 'size': 12, 'color': '#10135B'},
        },
        'range': [xlim[0],xlim[1]],
        'tickfont': {
            'color': '#ffffff'
        }
    },
    yaxis={
        'automargin': True,
        'title': {
            'text': 'Session Duration Time (m)',
            'font': {'family': 'Arial', 'size': 12, 'color': '#10135B'},
        },
        'tickfont': {
            'color': '#ffffff'
        },
        'range': [ylim[0],ylim[1]],
    },
    margin=dict(b=30, t=60,)
)

fig2 = go.Figure()

group_sdt_mean_bar = go.Bar(
                        x=[group_sdt_mean],
                        y=['Others'],
                        orientation='h',
                        marker_color='#F8D294',
                        opacity=0.8,
                        # text=[group_sdt_mean],
                    )
fig2.add_trace(group_sdt_mean_bar)

your_sdt_bar = go.Bar(
                x=[your_sdt],
                y=['You'],
                orientation='h',
                marker_color='#A7A8C1',
                opacity=0.8,
                # text=[your_sdt],
            )
fig2.add_trace(your_sdt_bar)
fig2.update_traces(
    hoverlabel={
    'bordercolor': "rgba(0,0,0,0)",
    'font': {
      'color': "#FFF"
    }
    },
    hovertemplate="%{x}<extra></extra>"
    )

fig2.update_layout(plot_bgcolor = 'white', title="Weekly Average Session Time", 
                   bargap=0.2, showlegend=False, width=616, height=336,
                  )
fig2.update_yaxes(showline=True, showticklabels=False, linewidth=2, linecolor='black',)
fig2.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e5e5e5')

app_df = pd.read_csv('datas/weekly_average.csv')

fig3 = go.Figure()

for col in app_df.columns[1:]:
    fig3.add_trace(
        go.Bar(
            x=app_df['day'],
            y=app_df[col],
            marker_color='#A7A8C1' if col == 'user_usage_time' else '#F8D294',
            opacity=0.8,
            hoverinfo='none',
            # text=app_df[col],
            name='You' if col == 'user_usage_time' else 'Others'
        )
    )
    
fig3.update_traces(
    hoverlabel={
    'bordercolor': "rgba(0,0,0,0)",
    'font': {
      'color': "#FFF"
    }
    },
    hovertemplate="%{y}<extra></extra>"
    )

fig3.update_layout(
    plot_bgcolor='white',
    title="Weekly Usage Time",
    showlegend=False,
    barmode='group',
    width=1136,
    height=256,
    xaxis=dict(
        showline=True,
        linewidth=2,
        linecolor='black'
    ),
    yaxis=dict(
        showgrid=True,
        gridwidth=1,
        gridcolor='#e5e5e5'
    ),
    margin=dict(b=0, t=60)
)
dash.register_page(__name__)

layout = html.Div(children=[
     html.Div([
        html.Div(
            html.A(
                html.Button("Check Your Usage Pattern!",style=button_style), href="/report"
        )),
        html.Div([
            html.Div(style=col_item_style, children=[
                html.Div(children=[
                    html.Div(
                    html.Div(style=user_square_style),
                        className=child_classes
                    ),
                    html.P('You', className=child_classes),
                ], style={'display': 'flex', 'flex-direction': 'row'}),
                html.Div(children=[
                    html.Div(
                    html.Div(style=others_square_style),
                        className=child_classes
                    ),
                    html.P('Others', className=child_classes)
                ], style={'margin-left': '3rem', 'display': 'flex', 'flex-direction': 'row'})
            ])
        ], style=menu_style),
        ], style={'display': 'flex', 'width': '1024px', 'justify-content': 'flex-end'}
    ),
    html.Div(children=[
        html.Div(children=[
            dcc.Graph(figure = fig1)
        ], style={'width': '504px', 'margin-right': '16px'}),
        html.Div(children=[
            dcc.Graph(figure = fig2)
        ], style={'width': '616px'})
    ], style=graph_wrapper),
    html.Div(children=[
        dcc.Graph(figure = fig3)
    ], style={'width': '1136px', 'height': '256px', 'margin-top': '16px'})
])
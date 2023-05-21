import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
from datetime import timezone, timedelta, datetime

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
    'margin' : '-4.5rem 15rem 1.5rem 0',
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
your_id = 64
your_ust = group_df.loc[your_id, 'usage_time']
your_sdt = group_df.loc[your_id, 'session_duration_time']

# Get group mean and median values
min_ust = group_df['usage_time'].min()
max_ust = group_df['usage_time'].max()
min_sdt = group_df['session_duration_time'].min()
max_sdt = group_df['session_duration_time'].max()
group_ust_mean = group_df["usage_time"].mean()
group_ust_median = group_df['usage_time'].median()
group_sdt_mean = int(group_df["session_duration_time"].mean().round())
group_sdt_median = group_df['session_duration_time'].median()

# Set range of axis
xlb, xrb = -100, max_ust*0.9
ybb, ytb = -20, max_sdt*0.4
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
                    hoverinfo='none'
                    ))
fig1.update_traces(contours_showlines=False, legendwidth=400)


# Define group names and colors
group_names = ["RISK", "SPRINT", "SAFE", "ON/OFF"]
group_colors = ['rgba(50,50,50,0.3)', 'rgba(50,50,50,0.3)', 'rgba(50,50,50,0.3)', 'rgba(50,50,50,0.3)']
group_descriptions = [
    "RISK group's usage pattern could indicate, a high level of device <br>dependency, signaling potential risk factors for digital wellness.",
    "SPRINT group's usage pattern might reflect a preference for <br>fewer, but longer, periods of engagement with their devices.",
    "SAFE group's usage pattern might indicate a balanced relationship <br>with their devices, reducing potential risks associated with excessive screen time.",
    "ON/OFF group shows a pattern of frequent checking or multitasking,<br>with shorter periods of engagement spread throughout the day.",
    ]
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
                           showlegend=False, hovertext=group_descriptions, hoverinfo='text',  
                           hoverlabel=dict(
                            bordercolor="rgba(0, 0, 0, 0.6)",
                            bgcolor="rgba(255, 255, 255,0.8)",
                            font_size=14,
                            ),))

x0 = [group_ust_median, xlb, xlb, group_ust_median]
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
                          marker=dict(color='#10135B', size=10), hoverinfo='none'))
fig1.add_vline(x=group_ust_median, line_dash="dot", line_color="#7C6542", line_width=1)
fig1.add_hline(y=group_sdt_median, line_dash="dot", line_color="#7C6542", line_width=1)

user_group_description = group_descriptions[user_group_index]
# Define plot layout
fig1.update_layout(
    title={
        'text': f"Your group - {group_names[user_group_index]}<br><span style='font-size: 10px;'>{user_group_description}</span>",
        'y':0.9,
        },
    autosize=False, width=488, height=336,
    showlegend=False,
    plot_bgcolor='white', 
    paper_bgcolor='white', 
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
    margin=dict(autoexpand=False, b=30, t=90),
)

if user_group_index == 0 or user_group_index == 1:
    group_sdt_mean = group_df[group_df["session_duration_time"] > group_sdt_median]["session_duration_time"].mean().round()
elif user_group_index == 2 or user_group_index == 3:
    group_sdt_mean = group_df[group_df["session_duration_time"] <= group_sdt_median]["session_duration_time"].mean().round()

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
    hovertemplate="%{x}m<extra></extra>"
    )

fig2.update_layout(plot_bgcolor = 'white', title="Weekly Average Session Time", 
                   bargap=0.2, showlegend=False, width=616, height=336,
                  )
fig2.update_yaxes(showline=True, showticklabels=False, linewidth=2, linecolor='black',)
fig2.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e5e5e5')

user = group_df.loc[your_id, 'User']
print(user)
df = pd.read_csv('datas/total_user_usage_whole.csv')

df['Date'] = pd.to_datetime(df['Date'])
df['Day'] = df['Date'].dt.day_name().str[:3]

def assign_group(row):
    if row['usage_time'] > group_ust_median:
        return 1  # RISK/ON/OFF
    else:
        return 0  # SPRINT/SAFE

group_df['group'] = group_df.apply(assign_group, axis=1)
if group_df.loc[your_id, 'usage_time'] > group_ust_median:
    user_group = 1  # RISK/ON/OFF
else:
    user_group = 0  # SPRINT/SAFE
same_group_users = group_df[group_df['group'] == user_group]['User'].tolist()
print(same_group_users)
df = df[df['User'].isin(same_group_users)]
print(df)

user_usage_time = df[df['User'] == user].groupby('Day')['TotalUsageTime'].sum()
group_usage_time = df.groupby('Day')['TotalUsageTime'].mean().round()
app_df = pd.merge(user_usage_time, group_usage_time, on='Day').reset_index()
app_df.columns = ['day', 'user_usage_time', 'group_usage_time']

day_order = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
day_mapping = {day: i for i, day in enumerate(day_order)}
app_df['day_id'] = app_df['day'].map(day_mapping)
app_df = app_df.sort_values('day_id')
app_df = app_df.drop('day_id', axis=1)

def convert_time(minute):
    if minute >= 60:
        if minute % 60 != 0: return str(int(minute // 60))+"h "+str(int(minute % 60))+"m"
        else: return str(int(minute // 60))+"h"
    else: return str(int(minute % 60))+"m"
app_df['converted_user_usage_time'] = app_df['user_usage_time'].apply(lambda x: convert_time(x))
app_df['converted_group_usage_time'] = app_df['group_usage_time'].apply(lambda x: convert_time(x))

fig3 = go.Figure()
for col in ['converted_user_usage_time', 'converted_group_usage_time']:
    fig3.add_trace(
        go.Bar(
            x=app_df['day'],
            y=app_df[col.split('_')[1] + '_usage_time'],  # Use original data for plotting
            marker_color='#A7A8C1' if 'user' in col else '#F8D294',
            opacity=0.8,
            hoverinfo='none',
            name='You' if 'user' in col else 'Others',
            hovertext=app_df[col]  # Use converted data for hover text
        )
    )
    
fig3.update_traces(
    hoverlabel={
    'bordercolor': "rgba(0,0,0,0)",
    'font': {
      'color': "#FFF"
    }
    },
    hovertemplate="%{hovertext}<extra></extra>"
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

dash.register_page(__name__, path='/report/group')

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
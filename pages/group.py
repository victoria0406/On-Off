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
    'padding': '10px',
    'display': 'flex',
    'flex-direction': 'row',
}

col_item_style = {
    'display': 'flex',
    'flex-direction': 'row',
}

button_style = {
    'font-family': 'Arial',
    'width': '100%',
    'outline': 'None',
    'background-color': '#f8f9fa',
    'font-family': 'Arial',
    'color': '#000000',
    'border': 'none'
}

child_classes = 'm-2'

# Load data
group_df = pd.read_csv('datas/total_user_usage.csv')

# Get your usage and session duration times
your_id = 2
your_ust = group_df.loc[your_id, 'usage_time']
your_sdt = group_df.loc[your_id, 'session_duration_time']

# Get group mean and median values
group_ust_mean = group_df["usage_time"].mean()
group_ust_median = group_df['usage_time'].median()
group_sdt_mean = group_df["session_duration_time"].mean()
group_sdt_median = group_df['session_duration_time'].median()

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

# Add group names in the background
fig1.add_trace(go.Scatter(x=[(group_ust_median+max(group_df['usage_time']))/2], 
                          y=[(group_sdt_median+max(group_df['session_duration_time']))/2], mode='text',
                          text='RISK', textposition='middle center', textfont_size=25, textfont_family='Sherif', 
                          textfont_color='rgba(50,50,50,0.3)', showlegend=False))
fig1.add_trace(go.Scatter(x=[(group_ust_median)/2], 
                          y=[(group_sdt_median+max(group_df['session_duration_time']))/2], mode='text',
                          text='SPRINT', textposition='middle center', textfont_size=25, textfont_family='Sherif', 
                          textfont_color='rgba(50,50,50,0.3)', showlegend=False))
fig1.add_trace(go.Scatter(x=[(group_ust_median)/2], 
                          y=[(group_sdt_median)/2], mode='text',
                          text='SAFE', textposition='middle center', textfont_size=25, textfont_family='Sherif', 
                          textfont_color='rgba(50,50,50,0.3)', showlegend=False))
fig1.add_trace(go.Scatter(x=[(group_ust_median+max(group_df['usage_time']))/2], 
                          y=[(group_sdt_median)/2], mode='text',
                          text='ON/OFF', textposition='middle center', textfont_size=25, textfont_family='Sherif', 
                          textfont_color='rgba(50,50,50,0.3)', showlegend=False))

# Add rectangular shape
fig1.add_shape(type='rect', xref='x', yref='y',
               x0=group_ust_median, y0=group_sdt_median,
               x1=max(group_df['usage_time']), y1=max(group_df['session_duration_time']),
               fillcolor="#A7A8C1", opacity=0.5, line=dict(width=0))

# Add your marker and median lines
fig1.add_trace(go.Scatter(x=[your_ust], y=[your_sdt], mode='markers+text', 
                          text=["You"], textposition="bottom center",
                          textfont=dict(family="Arial", size=15, color="#10135B"),
                          marker=dict(color='#10135B', size=10)))
fig1.add_vline(x=group_ust_median, line_dash="dot", line_color="#7C6542", line_width=1)
fig1.add_hline(y=group_sdt_median, line_dash="dot", line_color="#7C6542", line_width=1)

# Define plot layout
fig1.update_layout(
    title="your group: RISK Group",
    width=500, height=375,
    showlegend=False,
    hovermode=False,
    xaxis={
        'title': {
            'text': 'Usage Time (m)',
            'font': {'family': 'Arial', 'size': 14, 'color': '#10135B'}
        },
        'showticklabels': False,
    },
    yaxis={
        'title': {
            'text': 'Session Duration Time (m)',
            'font': {'family': 'Arial', 'size': 14, 'color': '#10135B'}
        },
        'showticklabels': False
    },
)

fig2 = go.Figure()

group_sdt_mean_bar = go.Bar(
                        x=[group_sdt_mean],
                        y=['Others'],
                        orientation='h',
                        marker_color='#F8D294',
                        opacity=0.8,
                        text=[group_sdt_mean],
                        hoverinfo='none'
                    )
fig2.add_trace(group_sdt_mean_bar)

your_sdt_bar = go.Bar(
                x=[your_sdt],
                y=['You'],
                orientation='h',
                marker_color='#A7A8C1',
                opacity=0.8,
                text=[your_sdt],
                hoverinfo='none'
            )
fig2.add_trace(your_sdt_bar)

fig2.update_layout(plot_bgcolor = 'white', title="Weekly Average Session Time", 
                   bargap=0.2, showlegend=False, width=448, height=350,)
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
            text=app_df[col],
            name='You' if col == 'user_usage_time' else 'Others'
        )
    )

fig3.update_layout(
    plot_bgcolor='white',
    title="Weekly Usage Time",
    showlegend=False,
    barmode='group',
    width=1051,
    height=410,
    xaxis=dict(
        showline=True,
        linewidth=2,
        linecolor='black'
    ),
    yaxis=dict(
        showgrid=True,
        gridwidth=1,
        gridcolor='#e5e5e5'
    )
)
dash.register_page(__name__)

layout = html.Div(children=[
    html.Div(
        dbc.Row([
            dbc.Col([
                html.H4('Compare your usage with others :)')
            ]),
            dbc.Col(
                dbc.Row([
                    dbc.Col(
                        html.Div(style=col_style, children=[
                            dcc.Link(dbc.Button("Check Your Usage Pattern!", outline=False, style=button_style, color='primary'), href="/report", style={'width': '100%'}),
                        ])
                    ),
                    dbc.Col(style=col_style, children=[
                        html.Div(style=col_item_style, children=[
                            html.Div(
                                html.Div(style=user_square_style),
                                className=child_classes
                            ),
                            html.P(': You', className=child_classes),
                            html.Div(
                                html.Div(style=others_square_style),
                                className=child_classes
                            ),
                            html.P(': Others', className=child_classes)
                        ]), 
                    ])
                ])
            )
        ]),
    ),

    dbc.Row([
        dbc.Col(
            dcc.Graph(figure = fig1)
        ),
        dbc.Col(
            dcc.Graph(figure = fig2)
        )
    ]),
    dbc.Row([
        dcc.Graph(figure = fig3)
    ])

])
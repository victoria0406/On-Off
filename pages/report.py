import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd 
import math
import plotly.graph_objects as go


dash.register_page(__name__)

COLORS = ['#F2CB80','#DCD76E','#A7C670','#999BB8','#BBA083','#B5B5B5']


CONTENT_STYLE = {
    "background-color": "#F7F8FA",
    "height": "21rem",
    "border-radius": "5px",
    "margin-bottom": '1rem',
    
}

FCONTENT_STYLE = {
    "background-color": "white",
    "border-radius": "5px",
    "height": "21rem",
    'display': 'inline-block',
    "width" : "25rem",
    "margin-right" : "10px", 
    "float":"left" 
}

SCONTENT_STYLE ={
    "background-color": "white",
    "border-radius": "5px",
    "height": "21rem",
    'display': 'inline-block',
    "width" : "45rem",
    "float":"right" 
}

TCONTENT_STYLE = {
    "background-color": "white",
    "border-radius": "5px",
    "height": "16rem",
    'display': 'inline-block',
    "width" : "45rem",
    "margin-right" : "10px", "float":"left",
}

FHCONTENT_STYLE ={
    "background-color": "white",
    "border-radius": "5px",
    "height": "16rem",
    'display': 'inline-block',
    "width" : "25rem","float":"right",
}


BUTTON_STYLE = {
  'margin' : '-4.5rem 27rem 1.5rem 0',
  'width' : '15rem',
  'float': 'right',
  'background-color': '#EBEBF0',
  'color': '#000',
  'text-align': 'center',
  'border-radius': '5px',
  'height': '40px',
  'border': 'none'
}

TOGGLE_STYLE ={
    "margin": '-4.5rem -2rem 1.5rem 0',
    "width":"27rem",
    "float":"right",
}

APP_BUTTON_STYLE={
    "width": "85%",
    'margin':'0px 10px 10px 30px',
    'border':'none',
    'border-radius':'5px',
}
STATISTICS_STYLE={
    "width": "85%",
    'border':'none',
    'border-radius':'5px',
    'background-color': '#F7F8FA',
    'margin': '10px 0 0 20px',
    'height': '25%'
}


############# top 5 app ################
app_usage_time = pd.read_csv('./datas/app_usage_time.csv')
today = app_usage_time.loc[app_usage_time['date']=='2023-05-10']
yesterday = app_usage_time.loc[app_usage_time['date']=='2023-05-09']
top=list(app_usage_time)

fig = px.bar(today, y="date", x=[top[1],top[2],top[3],top[4],top[5],top[6]],orientation='h', color_discrete_sequence=COLORS, width=540, height=170)
fig.update_xaxes(title=None, showticklabels=False)
fig.update_yaxes(title=None, showticklabels=False,)
fig.update_layout(showlegend=False, plot_bgcolor='white',paper_bgcolor="rgb(0,0,0,0)")

hour = today['Total']//60
min = today['Total']%60

######## number of access #############
app_usage_hour = pd.read_csv('./datas/app_usage_hour.csv')

pd.to_datetime(app_usage_hour['time'], format = "%H:%M")
total = pd.DataFrame(data=None, index=None, columns=["time","top1","top2","top3","top4","top5"], dtype=None, copy=False)
top1=0
top2=0
top3=0
top4=0
top5=0

for idx, row in app_usage_hour.iterrows():
    minute=int(row[0].split(":")[0])*60+int(row[0].split(":")[1])
    if(not math.isnan(row[1])):
        top1 = top1+row[1]
        total = total.append({'time':minute, 'top1':top1, 'top2':top2, 'top3':top3, 'top4':top4, 'top5':top5},ignore_index=True)
    if(not math.isnan(row[2])):
        top2 = top2+row[2]
        total = total.append({'time':minute, 'top1':top1, 'top2':top2, 'top3':top3, 'top4':top4, 'top5':top5},ignore_index=True)
    if(not math.isnan(row[3])):
        top3 = top3+row[3]
        total = total.append({'time':minute, 'top1':top1, 'top2':top2, 'top3':top3, 'top4':top4, 'top5':top5},ignore_index=True)
    if(not math.isnan(row[4])):
        top4 = top4+row[4]
        total = total.append({'time':minute, 'top1':top1, 'top2':top2, 'top3':top3, 'top4':top4, 'top5':top5},ignore_index=True)
    if(not math.isnan(row[5])):
        top5 = top5+row[5]
        total = total.append({'time':minute, 'top1':top1, 'top2':top2, 'top3':top3, 'top4':top4, 'top5':top5},ignore_index=True)

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=total['time'], y=total['top1'], mode='lines', name=top[1],line_color=COLORS[0]))
fig1.add_trace(go.Scatter(x=total['time'], y=total['top2'], mode='lines', name=top[2],line_color=COLORS[1]))
fig1.add_trace(go.Scatter(x=total['time'], y=total['top3'], mode='lines', name=top[3],line_color=COLORS[2]))
fig1.add_trace(go.Scatter(x=total['time'], y=total['top4'], mode='lines', name=top[4],line_color=COLORS[3]))
fig1.add_trace(go.Scatter(x=total['time'], y=total['top5'], mode='lines', name=top[5],line_color=COLORS[4]))
fig1.update_layout(
    xaxis = dict(
        title = "Time of Day",
        tickmode = 'array',
        tickvals = [0,240,480,720,960,1200,1440],
        ticktext = ['0', '4', '8', '12', '16', '20','24'],
        showline=True, linewidth=1, linecolor='#BEBEBE',
        
    ),
    yaxis = dict(
        title = "Usage Time (hour)",
        tickmode = 'array',
        tickvals = [0,120,240,360,480,600,720],
        ticktext = ['0', '2', '4', '6', '8', '10','12'],
        linecolor="#BEBEBE",
        showgrid=True, linewidth=1,gridcolor='#F4F4F4'
    )
)

fig1.update_layout(showlegend=False, plot_bgcolor='white',paper_bgcolor="rgb(0,0,0,0)", font=dict(size=9),width=750, height=410)
# fig1.show() 
############ number of access ################
access = pd.read_csv('./datas/number_of_access.csv')
access_today=access.loc[today.index]
access_yesterday=access.loc[today.index-1]

fig2 = go.Figure()
fig2.add_traces(go.Bar(x=top[1:7], y=access_today.values.tolist()[0][1:7],  marker_color=COLORS))
fig2.update_layout(showlegend=False, plot_bgcolor='white',paper_bgcolor="rgb(0,0,0,0)",width=720, height=350)
fig2.update_layout(
    yaxis = dict(
        showgrid=True, gridcolor='#F4F4F4',
        zeroline=True, zerolinecolor='#A2A2A2'
    ),
    xaxis = dict(
        title=None, showticklabels=False,
    )
)
# fig2.show()
############## statistics ##################
differ=int(str(today['Total']).split()[1])-int(str(yesterday['Total']).split()[1])

if (differ>0):
    differ_usage ="+ "+str(differ//60)+"h "+str(differ%60)+"m"
    usage_color="#BBA083"
else:
    differ = -differ
    differ_usage = "- "+str(differ//60)+"h "+str(differ%60)+"m"
    usage_color="#AEBF9E"
    
access_differ=int(str(access_today['Total']).split()[1])-int(str(access_yesterday['Total']).split()[1])
if(access_differ>0):
    access_color ="#BBA083"
else:
    access_color="#AEBF9E"
    
unlock = pd.read_csv('./datas/unlock.csv')
unlock_today=unlock.loc[today.index]
unlock_yesterday=unlock.loc[today.index-1]

unlock_differ=int(str(unlock_today['unlock']).split()[1])-int(str(unlock_yesterday['unlock']).split()[1])
if(unlock_differ>0):
    unlock_color ="#BBA083"
else:
    unlock_color="#AEBF9E"
###############################################

layout = html.Div(children=[
    html.Div([html.Div(html.A(html.Button("Compare with Others!",style=BUTTON_STYLE), href="/group")),
            html.Div(dbc.Nav([
                dbc.NavLink('DAILY', href="/report", active="exact"),
                dbc.NavLink('WEEKLY', href="/weekly", active="exact"),
            ],
            className='report-nav'
        ), style=TOGGLE_STYLE)
        ],style={'display': 'inline-block','float':"right"}
    ),    
    html.Div([
        html.Div([html.P("Apps Top",style={"margin":"10px 0 -5px 10px"}), html.P(str(hour).split()[1]+"h "+str(min).split()[1]+"m Used",style={'font-weight':'bold','font-size':"20px","margin":"0px 20px -60px 15px",'text-align':'right'}),
            html.Div(dcc.Graph(figure = fig, config={'displayModeBar': False}),
            style={'margin-left': '-60px', 'margin-bottom':'-70px'}),
            html.Div([
              html.A(html.Button(top[1], style=APP_BUTTON_STYLE), href="/Apps/First"),
              html.A(html.Button(top[2], style=APP_BUTTON_STYLE ), href="/Apps/First"),
              html.A(html.Button(top[3], style=APP_BUTTON_STYLE), href="/Apps/First"),
              html.A(html.Button(top[4], style=APP_BUTTON_STYLE), href="/Apps/First"), 
              html.A(html.Button(top[5], style=APP_BUTTON_STYLE), href="/Apps/First"),
              html.A(html.Button(top[6], style=APP_BUTTON_STYLE), href="/Apps/First")
            ], style={'z-index':'1'})], style=FCONTENT_STYLE),
        html.Div([html.P("Usage Time",style={"margin":"10px 0 -10px 15px"}),
                html.Div(dcc.Graph(figure = fig1, config={'displayModeBar': False}),
                    style={'margin-top': '-80px'})
                ], style=SCONTENT_STYLE),
    ], style = CONTENT_STYLE
    ),
     html.Div([
        html.Div([html.P("Number of Access",style={"margin":"5px 0 -10px 15px"}),
                html.Div(dcc.Graph(figure = fig2, config={'displayModeBar': False}),
                    style={'margin-top': '-100px','padding-top':'20px','margin-bottom':'-140px'}
                )        
        
        ], style=TCONTENT_STYLE),
        html.Div([html.P("Statistics",style={"margin":"5px 0 -5px 15px"}),
                  html.Div([html.P("Usage Time",style={'margin-left':'15px','padding-top':'3px','font-size':'14px'}),
                           html.Div([html.P(str(hour).split()[1]+"h "+str(min).split()[1]+"m", style={'font-weight':"bold",'font-size':'18px','margin':'-12px 0 0 20px',"float":"left"}),
                                     html.Div([html.P(differ_usage,style={"float":"left","margin-right":"10px",'font-size':'15px','color':usage_color}),html.P(" yesterday",style={"float":"right",'font-size':'14px'})],style={"float":"right",'margin':'-12px 15px 0 0'})]) 
                        ],style=STATISTICS_STYLE),
                  html.Div([html.P("Access",style={'margin-left':'15px','padding-top':'3px','font-size':'14px'}),
                            html.Div([html.P(str(access_today['Total']).split()[1], style={'font-weight':"bold",'font-size':'18px','margin':'-12px 0 0 20px',"float":"left"}),
                                     html.Div([html.P(access_differ,style={"float":"left","margin-right":"10px",'font-size':'15px','color':access_color}),html.P(" yesterday",style={"float":"right",'font-size':'14px'})],style={"float":"right",'margin':'-12px 15px 0 0'})])
                        ],style=STATISTICS_STYLE),
                  html.Div([html.P("Unlock",style={'margin-left':'15px','padding-top':'3px','font-size':'14px'}),
                            html.Div([html.P(str(unlock_today['unlock']).split()[1], style={'font-weight':"bold",'font-size':'18px','margin':'-12px 0 0 20px',"float":"left"}),
                                     html.Div([html.P(unlock_differ,style={"float":"left","margin-right":"10px",'font-size':'15px','color':unlock_color}),html.P(" yesterday",style={"float":"right",'font-size':'14px'})],style={"float":"right",'margin':'-12px 15px 0 0'})])
                        ],style=STATISTICS_STYLE),  
                ], style=FHCONTENT_STYLE),
    ], style = CONTENT_STYLE
    ),
])
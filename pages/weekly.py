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
    "height": "16.5rem",
    'display': 'inline-block',
    "width" : "43rem",
    "margin-right" : "10px", "float":"left",
}

FHCONTENT_STYLE ={
    "background-color": "white",
    "border-radius": "5px",
    "height": "16.5rem",
    'display': 'inline-block',
    "width" : "27rem","float":"right",
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
AVERAGE_STYLE={
    'width':'90%',
    'height':'40px',
    'border-radius':'5px',
    'margin':'15px 0 0 20px',
    'background-color':'#F7F8FA'
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

############## usage ###################
app_usage_time = pd.read_csv('./datas/app_usage_time.csv')

today_index = int(str(today['Total']).split()[0])
weekly_usage = app_usage_time[today_index-6:today_index+1]
weekly_usage['date']=pd.to_datetime(weekly_usage['date'], format = "%Y %m %d")
weekly_usage['date']=weekly_usage['date'].dt.strftime('%b %d')

fig1 = px.bar(weekly_usage, x="date", y=[top[1], top[2], top[3],top[4],top[5],top[6]],color_discrete_sequence=COLORS,width=750, height=400)

fig1.update_layout(
    xaxis = dict(
        title = None,
        tickmode = 'array',
        showline=True, linewidth=1, linecolor='#BEBEBE',
        
    ),
    yaxis = dict(
        # title = "Usage Time (hour)",
        title=dict(
            text="Usage Time (hour)",
            font=dict(
                size=12,
        )),
        tickmode = 'array',
        tickvals = [0,120,240,360,480,600,720],
        ticktext = ['0', '2', '4', '6', '8', '10','12'],
        showgrid=True, linewidth=1,gridcolor='#F4F4F4',
        tickfont = dict(size=9)
    )
)

fig1.update_layout(showlegend=False, plot_bgcolor='white',paper_bgcolor="rgb(0,0,0,0)",bargap=0.3)
# fig1.show() 

############ number of access ################
access = pd.read_csv('./datas/number_of_access.csv')

weekly_access = access[today_index-6:today_index+1]
weekly_access['date']=weekly_usage['date']
fig2 = px.bar(weekly_access, x=weekly_access['date'], y=[top[1], top[2], top[3],top[4],top[5],top[6]],color_discrete_sequence=COLORS,width=750, height=340)
date = weekly_usage['date'].values.tolist()
print(date)
fig2.update_layout(
    xaxis = dict(
        title = None,
        tickmode = 'array',
        showline=True, linewidth=1, linecolor='#BEBEBE',
        
    ),
    yaxis = dict(
        title = None,
        tickmode = 'array',
        tickvals = [0,10,20,30,40,50,60,70],
        ticktext = ['0', '10', '20', '30', '40', '50','60','70'],
        showgrid=True, linewidth=1,gridcolor='#F4F4F4'
    )
)

fig2.update_layout(showlegend=False, plot_bgcolor='white',paper_bgcolor="rgb(0,0,0,0)",bargap=0.3)

# fig2.show()
################ screen on ####################
screen_on = 150
unlock = pd.read_csv('./datas/unlock.csv')

weekly_unlock = unlock[today_index-6:today_index+1]
weekly_unlock['date']=weekly_usage['date']

fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=weekly_unlock['date'], y=weekly_unlock['unlock'], mode='lines+markers', line_color='#686CAD',
                          marker=dict(
                                color='white',
                                size=14,
                                line=dict(color='#686CAD',width=2)
                            )))

fig3.update_layout(
    xaxis = dict(
        title = None,
        tickmode = 'array',
        showline=True, linewidth=1, linecolor='#BEBEBE',
    ),
    yaxis = dict(
        title = None,
        showticklabels=False,
    )
)

fig3.update_layout(showlegend=False, plot_bgcolor='white',paper_bgcolor="rgb(0,0,0,0)",width=510, height=320)
# fig3.show()
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
                    style={'margin-top': '-50px'})
                ], style=SCONTENT_STYLE),
    ], style = CONTENT_STYLE
    ),
     html.Div([
        html.Div([html.P("Number of Access",style={"margin":"10px 0 -10px 15px"}),
                html.Div(dcc.Graph(figure = fig2, config={'displayModeBar': False}),
                    style={'margin-top': '-75px','padding-top':'20px','margin-left':'-20px'}
                )        
        
        ], style=TCONTENT_STYLE),
        html.Div([html.P("Number of Screen On",style={"margin":"10px 0 -5px 15px"}),
                  html.Div([html.P("average",style={'color':'#686CAD','padding-top':"5px",'margin-left':'15px','float':'left'}),
                            html.P(screen_on,style={"font-size":"18px","font-weight":"bold","float":"right","margin-right":'15px',"padding-top":'5px'})],style=AVERAGE_STYLE),
                  html.Div(dcc.Graph(figure = fig3,config={'displayModeBar': False}),
                    style={'margin':'-85px 0 0 -50px'})
                ], style=FHCONTENT_STYLE),
    ], style = CONTENT_STYLE
    ),
])
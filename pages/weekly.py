import dash
from dash import html, dcc, callback, Input, Output, ctx
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import math
import plotly.graph_objects as go

dash.register_page(__name__)

click = [0,0,0,0,0,0]
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
    'margin':'0px 10px 12px 30px',
    'border':'none',
    'border-radius':'7px',
    'box-shadow': '0px 4px 4px 0px rgba(0, 0, 0, 0.25)',
    "height":"27px"
}
AVERAGE_STYLE={
    'width':'90%',
    'height':'40px',
    'border-radius':'5px',
    'margin':'15px 0 0 20px',
    'background-color':'#F7F8FA'
}


BUTTON1=APP_BUTTON_STYLE
BUTTON2=APP_BUTTON_STYLE
BUTTON3=APP_BUTTON_STYLE
BUTTON4=APP_BUTTON_STYLE
BUTTON5=APP_BUTTON_STYLE
BUTTON6=APP_BUTTON_STYLE


############# top 5 app ################
app_usage_time = pd.read_csv('./datas/app_usage_time.csv')
today = app_usage_time.loc[app_usage_time['date']=='2023-05-10']
yesterday = app_usage_time.loc[app_usage_time['date']=='2023-05-09']
top=list(app_usage_time)

hour = today['Total']//60
min = today['Total']%60



############## usage ###################
app_usage_time = pd.read_csv('./datas/app_usage_time.csv')

today_index = int(str(today['Total']).split()[0])
weekly_usage = app_usage_time[today_index-6:today_index+1]
weekly_usage['date']=pd.to_datetime(weekly_usage['date'], format = "%Y %m %d")
weekly_usage['date']=weekly_usage['date'].dt.strftime('%b %d')

############ number of access ################
access = pd.read_csv('./datas/number_of_access.csv')

weekly_access = access[today_index-6:today_index+1]
weekly_access['date']=weekly_usage['date']

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
top1 = weekly_usage[top[1]].values.tolist()
top2 = weekly_usage[top[2]].values.tolist()
top3 = weekly_usage[top[3]].values.tolist()
top4 = weekly_usage[top[4]].values.tolist()
top5 = weekly_usage[top[5]].values.tolist()
others = weekly_usage[top[6]].values.tolist()

top1.insert(7,sum(top1))
top2.insert(7,sum(top2))
top3.insert(7,sum(top3))
top4.insert(7,sum(top4))
top5.insert(7,sum(top5))
others.insert(7,sum(others))

total_time = top1[7]+top2[7]+top3[7]+top4[7]+top5[7]+others[7]


###############################################

def layout():
    return html.Div(children=[
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
            html.Div([html.P("Apps Top",style={"margin":"10px 0 -5px 10px"}), html.P("{}{}{}{}".format(total_time//60,"h ", total_time%60,"m Used"),style={'font-weight':'bold','font-size':"20px","margin":"0px 20px -60px 15px",'text-align':'right'}),
                html.Div(dcc.Graph(id='top5', config={'displayModeBar': False}),
                style={'margin-left': '-60px', 'margin-bottom':'-70px'}),
                html.Div([
                html.Button(html.Div([html.Div([html.Div("1",style={"text-align":"center","line-height":"20px","background-color":COLORS[0],"margin-top":"2px","height":'20px',"width":"30px","float":"left","border-radius":"5px"}),html.Div(top[1],style={"float":"right","margin-left":"10px","font-weight":"bold"})],style={"float":"left","margin-left":"10px"}),html.Div("{}{}{}{}".format(top1[7]//60,"h ", top1[7]%60,"m"),style={"float":"right","margin-right":"10px","font-weight":"bold"})]), id='btn-nclicks-1', n_clicks=0, style=BUTTON1),
                html.Button(html.Div([html.Div([html.Div("2",style={"text-align":"center","line-height":"20px","background-color":COLORS[1],"margin-top":"2px","height":'20px',"width":"30px","float":"left","border-radius":"5px"}),html.Div(top[2],style={"float":"right","margin-left":"10px","font-weight":"bold"})],style={"float":"left","margin-left":"10px"}),html.Div("{}{}{}{}".format(top2[7]//60,"h ", top2[7]%60,"m"),style={"float":"right","margin-right":"10px","font-weight":"bold"})]), id='btn-nclicks-2', n_clicks=0, style=BUTTON2),
                html.Button(html.Div([html.Div([html.Div("3",style={"text-align":"center","line-height":"20px","background-color":COLORS[2],"margin-top":"2px","height":'20px',"width":"30px","float":"left","border-radius":"5px"}),html.Div(top[3],style={"float":"right","margin-left":"10px","font-weight":"bold"})],style={"float":"left","margin-left":"10px"}),html.Div("{}{}{}{}".format(top3[7]//60,"h ", top3[7]%60,"m"),style={"float":"right","margin-right":"10px","font-weight":"bold"})]), id='btn-nclicks-3', n_clicks=0, style=BUTTON3),
                html.Button(html.Div([html.Div([html.Div("4",style={"text-align":"center","line-height":"20px","background-color":COLORS[3],"margin-top":"2px","height":'20px',"width":"30px","float":"left","border-radius":"5px"}),html.Div(top[4],style={"float":"right","margin-left":"10px","font-weight":"bold"})],style={"float":"left","margin-left":"10px"}),html.Div("{}{}{}{}".format(top4[7]//60,"h ", top4[7]%60,"m"),style={"float":"right","margin-right":"10px","font-weight":"bold"})]), id='btn-nclicks-4', n_clicks=0, style=BUTTON4),
                html.Button(html.Div([html.Div([html.Div("5",style={"text-align":"center","line-height":"20px","background-color":COLORS[4],"margin-top":"2px","height":'20px',"width":"30px","float":"left","border-radius":"5px"}),html.Div(top[5],style={"float":"right","margin-left":"10px","font-weight":"bold"})],style={"float":"left","margin-left":"10px"}),html.Div("{}{}{}{}".format(top5[7]//60,"h ", top5[7]%60,"m"),style={"float":"right","margin-right":"10px","font-weight":"bold"})]), id='btn-nclicks-5', n_clicks=0, style=BUTTON5),
                html.Button(html.Div([html.Div([html.Div("6",style={"text-align":"center","line-height":"20px","background-color":COLORS[5],"margin-top":"2px","height":'20px',"width":"30px","float":"left","border-radius":"5px"}),html.Div(top[6],style={"float":"right","margin-left":"10px","font-weight":"bold"})],style={"float":"left","margin-left":"10px"}),html.Div("{}{}{}{}".format(others[7]//60,"h ", others[7]%60,"m"),style={"float":"right","margin-right":"10px","font-weight":"bold"})]), id='btn-nclicks-6', n_clicks=0, style=BUTTON6),
                ], style={'z-index':'1'})], style=FCONTENT_STYLE),
            html.Div([html.P("Usage Time",style={"margin":"10px 0 -10px 15px"}),
                    html.Div(dcc.Graph(id="usage_time", config={'displayModeBar': False}),
                        style={'margin-top': '-50px'})
                    ], style=SCONTENT_STYLE),
        ], style = CONTENT_STYLE
        ),
        html.Div([
            html.Div([html.P("Number of Access",style={"margin":"10px 0 -10px 15px"}),
                    html.Div(dcc.Graph(id="graph", config={'displayModeBar': False}),
                        style={'margin-top': '-75px','padding-top':'20px','margin-left':'-20px'}
                    )        
            
            ], style=TCONTENT_STYLE),
            html.Div([html.P("Number of Screen On",style={"margin":"10px 0 -5px 15px"}),
                    html.Div([html.P("average",style={'color':'#686CAD','padding-top':"5px",'margin-left':'15px','float':'left'}),
                                html.P(screen_on,style={"font-size":"18px","font-weight":"bold","float":"right","margin-right":'15px',"padding-top":'5px'})],style=AVERAGE_STYLE),
                    html.Div(dcc.Graph(figure = fig3,config={'displayModeBar': False}),
                        style={'margin':'-85px 0 0 -50px'})
                    ], style=FHCONTENT_STYLE)
        ], style = CONTENT_STYLE
        ),
    ])


@callback(
    Output('top5','figure'),
    Output('usage_time','figure'),
    Output('graph','figure'),
    
    Input('btn-nclicks-1', 'n_clicks'),
    Input('btn-nclicks-2', 'n_clicks'),
    Input('btn-nclicks-3', 'n_clicks'),
    Input('btn-nclicks-4', 'n_clicks'),
    Input('btn-nclicks-5', 'n_clicks'),
    Input('btn-nclicks-6', 'n_clicks')
)

def update_graph(btn1, btn2, btn3, btn4, btn5, btn6):
    
    apps = top[1:7]
    APP_COLOR = COLORS
    GRAPH_COLOR =COLORS
    global click
    
    if "btn-nclicks-1" == ctx.triggered_id:
        if(click[0] %2 == 0):  
            APP_COLOR = [COLORS[0],'#F8F7E2','#EDF4E2','#EBEBF1','#F1ECE6','#F0F0F0']
            GRAPH_COLOR = [COLORS[0]]*6
            apps = top[1]
        click0 = click[0]+1
        click = [click0,0,0,0,0,0] 
    elif "btn-nclicks-2" == ctx.triggered_id:
        if(click[1] %2 == 0):  
            APP_COLOR = ['#F5EFE3',COLORS[1],'#EDF4E2','#EBEBF1','#F1ECE6','#F0F0F0']
            GRAPH_COLOR = [COLORS[1]]*6
            apps = top[2]
        click1 = click[1]+1
        click = [0,click1,0,0,0,0] 
    elif "btn-nclicks-3" == ctx.triggered_id:
        if(click[2] %2 == 0):  
            APP_COLOR = ['#F5EFE3','#F8F7E2',COLORS[2],'#EBEBF1','#F1ECE6','#F0F0F0']
            GRAPH_COLOR = [COLORS[2]]*6
            apps = top[3]
        click2 = click[2]+1
        click = [0,0,click2,0,0,0]  
    elif "btn-nclicks-4" == ctx.triggered_id:
        if(click[3] %2 == 0):  
            APP_COLOR = ['#F5EFE3','#F8F7E2','#EDF4E2',COLORS[3],'#F1ECE6','#F0F0F0']
            GRAPH_COLOR = [COLORS[3]]*6
            apps = top[4]
        click3 = click[3]+1
        click = [0,0,0,click3,0,0]  
    elif "btn-nclicks-5" == ctx.triggered_id: 
        if(click[4]%2==0):     
            APP_COLOR = ['#F5EFE3','#F8F7E2','#EDF4E2','#EBEBF1',COLORS[4],'#F0F0F0']
            GRAPH_COLOR = [COLORS[4]]*6
            apps = top[5]
        click4 = click[4]+1
        click = [0,0,0,0,click4,0]  
    elif "btn-nclicks-6" == ctx.triggered_id:
        if(click[5]%2==0):   
            APP_COLOR = ['#F5EFE3','#F8F7E2','#EDF4E2','#EBEBF1','#F1ECE6',COLORS[5]]
            GRAPH_COLOR = [COLORS[5]]*6
            apps = top[6]  
        click5 = click[5]+1
        click = [0,0,0,0,0,click5]  
        
    fig = px.bar(today, y="date", x=[top[1],top[2],top[3],top[4],top[5],top[6]],orientation='h', color_discrete_sequence=APP_COLOR, width=540, height=170)
    fig.update_xaxes(title=None, showticklabels=False)
    fig.update_yaxes(title=None, showticklabels=False,)
    fig.update_layout(showlegend=False, plot_bgcolor='white',paper_bgcolor="rgb(0,0,0,0)")
    
    fig1 = px.bar(weekly_usage, x="date", y=apps,color_discrete_sequence=GRAPH_COLOR,width=750, height=400)
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
    
    
    # fig2 = px.bar(weekly_access, x=['1','2','3','4','5','6','7','8','9'], y=apps)
    fig2 = px.bar(weekly_access, x=weekly_access['date'], y=apps, color_discrete_sequence=GRAPH_COLOR, width=740, height=340)
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

    
    return fig, fig1, fig2
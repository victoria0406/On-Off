import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, ctx
import plotly.express as px
import pandas as pd 
import math
import plotly.graph_objects as go

from inputdata.data import COLORS, click, app_usage_time, today, yesterday, top, hour, min, app_usage_hour, access, unlock


dash.register_page(__name__)



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

STATISTICS_STYLE={
    "width": "85%",
    'border':'none',
    'border-radius':'5px',
    'background-color': '#F7F8FA',
    'margin': '10px 0 0 20px',
    'height': '25%'
}


today_value=today.values.tolist()[0]

######## usage time #############


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

# fig1.show() 
############ number of access ################

access_today=access.loc[today.index]
access_yesterday=access.loc[today.index-1]

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
    
unlock_today=unlock.loc[today.index]
unlock_yesterday=unlock.loc[today.index-1]

unlock_differ=int(str(unlock_today['unlock']).split()[1])-int(str(unlock_yesterday['unlock']).split()[1])
if(unlock_differ>0):
    unlock_color ="#BBA083"
else:
    unlock_color="#AEBF9E"
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
            html.Div([html.P("Apps Top",style={"margin":"10px 0 -5px 10px"}), html.P(str(hour).split()[1]+"h "+str(min).split()[1]+"m Used",style={'font-weight':'bold','font-size':"20px","margin":"0px 20px -60px 15px",'text-align':'right'}),
                html.Div(dcc.Graph(id="app_graph", config={'displayModeBar': False}),
                style={'margin-left': '-60px', 'margin-bottom':'10px'}),
                html.Div([
                html.Button(id="btn-nclicks-1", n_clicks=0, className='APP_BUTTON_STYLE'),
                html.Button(id="btn-nclicks-2", n_clicks=0, className='APP_BUTTON_STYLE'),
                html.Button(id="btn-nclicks-3", n_clicks=0, className='APP_BUTTON_STYLE'),
                html.Button(id="btn-nclicks-4", n_clicks=0, className='APP_BUTTON_STYLE'),
                html.Button(id="btn-nclicks-5", n_clicks=0, className='APP_BUTTON_STYLE'),
                html.Button(id="btn-nclicks-6", n_clicks=0, className='APP_BUTTON_STYLE'),
                ])], style=FCONTENT_STYLE),
            html.Div([html.P("Usage Time",style={"margin":"10px 0 -10px 15px"}),
                    html.Div(dcc.Graph(id = 'usage_graph', config={'displayModeBar': False}),
                        style={'margin-top': '-80px'})
                    ], style=SCONTENT_STYLE),
        ], style = CONTENT_STYLE
        ),
        html.Div([
            html.Div([html.P("Number of Access",style={"margin":"5px 0 -10px 15px"}),
                    html.Div(dcc.Graph(id="access_graph", config={'displayModeBar': False}),
                        style={'margin-top': '-10px','padding-top':'30px','margin-bottom':'-140px'}
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

@callback(
    Output("app_graph", 'figure'),
    Output('btn-nclicks-1', 'children'),
    Output('btn-nclicks-1', 'style'),
    Output('btn-nclicks-2', 'children'),
    Output('btn-nclicks-2', 'style'),
    Output('btn-nclicks-3', 'children'),
    Output('btn-nclicks-3', 'style'),
    Output('btn-nclicks-4', 'children'),
    Output('btn-nclicks-4', 'style'),
    Output('btn-nclicks-5', 'children'),
    Output('btn-nclicks-5', 'style'),
    Output('btn-nclicks-6', 'children'),
    Output('btn-nclicks-6', 'style'),
    Output('usage_graph','figure'),
    Output('access_graph','figure'),
    
    Input('btn-nclicks-1', 'n_clicks'),
    Input('btn-nclicks-2', 'n_clicks'),
    Input('btn-nclicks-3', 'n_clicks'),
    Input('btn-nclicks-4', 'n_clicks'),
    Input('btn-nclicks-5', 'n_clicks'),
    Input('btn-nclicks-6', 'n_clicks')
)

def update_graph(btn1, btn2, btn3, btn4, btn5, btn6):
    
    # print(btn1)
    
    GRAPH_COLOR = COLORS
    mode = ['solid','solid','solid','solid','solid','solid']
    global click
    TEXT_COLOR = ['black','black','black','black','black','black']
    color = ['#F7F8FA', '#F7F8FA', '#F7F8FA', '#F7F8FA', '#F7F8FA', '#F7F8FA']
    
    if "btn-nclicks-1" == ctx.triggered_id:
        if(click[0] %2 == 0):
            GRAPH_COLOR = [COLORS[0],'#F8F7E2','#EDF4E2','#EBEBF1','#F1ECE6','#F0F0F0']
            mode = ['solid','dot','dot','dot','dot','dot']
            TEXT_COLOR = ['black','#7C7C7C','#7C7C7C','#7C7C7C','#7C7C7C','#7C7C7C']
            color = ['#FFF4DF', '#F7F8FA', '#F7F8FA', '#F7F8FA', '#F7F8FA', '#F7F8FA']
        click0 = click[0]+1
        click = [click0,0,0,0,0,0] 
    if "btn-nclicks-2" == ctx.triggered_id:
        if(click[1] %2 == 0):
            GRAPH_COLOR = ['#F5EFE3',COLORS[1],'#EDF4E2','#EBEBF1','#F1ECE6','#F0F0F0']
            mode = ['dot','solid','dot','dot','dot','dot']
            TEXT_COLOR = ['#7C7C7C','black','#7C7C7C','#7C7C7C','#7C7C7C','#7C7C7C']
            color = ['#F7F8FA', '#F5F3D4', '#F7F8FA', '#F7F8FA', '#F7F8FA', '#F7F8FA']
        click1 = click[1]+1
        click = [0,click1,0,0,0,0] 
    elif "btn-nclicks-3" == ctx.triggered_id:
        if(click[2] %2 == 0): 
            GRAPH_COLOR = ['#F5EFE3','#F8F7E2',COLORS[2],'#EBEBF1','#F1ECE6','#F0F0F0']
            mode = ['dot','dot','solid','dot','dot','dot']
            TEXT_COLOR = ['#7C7C7C','#7C7C7C','black','#7C7C7C','#7C7C7C','#7C7C7C']
            color = ['#F7F8FA', '#F7F8FA', '#E5EED5', '#F7F8FA', '#F7F8FA', '#F7F8FA']
        click2 = click[2]+1
        click = [0,0,click2,0,0,0]  
    elif "btn-nclicks-4" == ctx.triggered_id:
        if(click[3] %2 == 0):
            GRAPH_COLOR = ['#F5EFE3','#F8F7E2','#EDF4E2',COLORS[3],'#F1ECE6','#F0F0F0']
            mode = ['dot','dot','dot','solid','dot','dot']
            TEXT_COLOR = ['#7C7C7C','#7C7C7C','#7C7C7C','black','#7C7C7C','#7C7C7C']
            color = ['#F7F8FA', '#F7F8FA', '#F7F8FA', '#E1E1EA', '#F7F8FA', '#F7F8FA']
        click3 = click[3]+1
        click = [0,0,0,click3,0,0]  
    elif "btn-nclicks-5" == ctx.triggered_id:
        if(click[4] %2 == 0):
            GRAPH_COLOR = ['#F5EFE3','#F8F7E2','#EDF4E2','#EBEBF1',COLORS[4],'#F0F0F0']
            mode = ['dot','dot','dot','dot','solid','dot']
            TEXT_COLOR = ['#7C7C7C','#7C7C7C','#7C7C7C','#7C7C7C','black','#7C7C7C']
            color = ['#F7F8FA', '#F7F8FA', '#F7F8FA', '#F7F8FA', '#EBE3DA', '#F7F8FA']
        click4 = click[4]+1
        click = [0,0,0,0,click4,0] 
    elif "btn-nclicks-6" == ctx.triggered_id:
        if(click[5] %2 == 0): 
            GRAPH_COLOR = ['#F5EFE3','#F8F7E2','#EDF4E2','#EBEBF1','#F1ECE6',COLORS[5]]
            mode = ['dot','dot','dot','dot','dot','solid']
            TEXT_COLOR = ['#7C7C7C','#7C7C7C','#7C7C7C','#7C7C7C','#7C7C7C','black']
            color = ['#F7F8FA', '#F7F8FA', '#F7F8FA', '#F7F8FA', '#F7F8FA', '#E9E9E9']
        click5 = click[5]+1
        click = [0,0,0,0,0,click5]  
        
    fig = px.bar(today, y="date", x=[top[1],top[2],top[3],top[4],top[5],top[6]],orientation='h', color_discrete_sequence=GRAPH_COLOR, width=540, height=90)
    fig.update_xaxes(title=None, showticklabels=False)
    fig.update_yaxes(title=None, showticklabels=False,)
    fig.update_layout(showlegend=False, plot_bgcolor='white',paper_bgcolor="rgb(0,0,0,0)", margin=dict(b=0))
        
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=total['time'], y=total['top1'], mode='lines', name=top[1],line_color=GRAPH_COLOR[0], line=dict(dash=mode[0])))
    fig1.add_trace(go.Scatter(x=total['time'], y=total['top2'], mode='lines', name=top[2],line_color=GRAPH_COLOR[1], line=dict(dash=mode[1])))
    fig1.add_trace(go.Scatter(x=total['time'], y=total['top3'], mode='lines', name=top[3],line_color=GRAPH_COLOR[2], line=dict(dash=mode[2])))
    fig1.add_trace(go.Scatter(x=total['time'], y=total['top4'], mode='lines', name=top[4],line_color=GRAPH_COLOR[3], line=dict(dash=mode[3])))
    fig1.add_trace(go.Scatter(x=total['time'], y=total['top5'], mode='lines', name=top[5],line_color=GRAPH_COLOR[4], line=dict(dash=mode[4])))
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
            showgrid=True, linewidth=1,gridcolor='#E0E0E0'
        )
    )

    fig1.update_layout(showlegend=False, plot_bgcolor='white',paper_bgcolor="rgb(0,0,0,0)", font=dict(size=9),width=750, height=410)
    
    fig2 = go.Figure()
    fig2.add_traces(go.Bar(x=top[1:7], y=access_today.values.tolist()[0][1:7],  marker_color=GRAPH_COLOR))
    fig2.update_layout(showlegend=False, plot_bgcolor='white',paper_bgcolor="rgb(0,0,0,0)",width=720, height=270, margin=dict(t=0))
    fig2.update_layout(
        yaxis = dict(
            showgrid=True, gridcolor='#E0E0E0',
            zeroline=True, zerolinecolor='#A2A2A2'
        ),
        xaxis = dict(
            title=None, showticklabels=False,
        )
    )
                
    children1 = html.Div([html.Div([html.Div("1",style={"text-align":"center","line-height":"20px","background-color":COLORS[0],"margin-top":"2px","height":'20px',"width":"30px","float":"left","border-radius":"5px"}),html.Div(top[1],style={"float":"right","margin-left":"10px","font-weight":"bold", "color":TEXT_COLOR[0]})],style={"float":"left","margin-left":"10px"}),html.Div("{}{}{}{}".format(today_value[1]//60,"h ", today_value[1]%60,"m"),style={"float":"right","margin-right":"10px","font-weight":"bold", "color":TEXT_COLOR[0]})])
    children2 = html.Div([html.Div([html.Div("2",style={"text-align":"center","line-height":"20px","background-color":COLORS[1],"margin-top":"2px","height":'20px',"width":"30px","float":"left","border-radius":"5px"}),html.Div(top[2],style={"float":"right","margin-left":"10px","font-weight":"bold", "color":TEXT_COLOR[1]})],style={"float":"left","margin-left":"10px"}),html.Div("{}{}{}{}".format(today_value[2]//60,"h ", today_value[2]%60,"m"),style={"float":"right","margin-right":"10px","font-weight":"bold", "color":TEXT_COLOR[1]})])
    children3 = html.Div([html.Div([html.Div("3",style={"text-align":"center","line-height":"20px","background-color":COLORS[2],"margin-top":"2px","height":'20px',"width":"30px","float":"left","border-radius":"5px"}),html.Div(top[3],style={"float":"right","margin-left":"10px","font-weight":"bold", "color":TEXT_COLOR[2]})],style={"float":"left","margin-left":"10px"}),html.Div("{}{}{}{}".format(today_value[3]//60,"h ", today_value[3]%60,"m"),style={"float":"right","margin-right":"10px","font-weight":"bold", "color":TEXT_COLOR[2]})])
    children4 = html.Div([html.Div([html.Div("4",style={"text-align":"center","line-height":"20px","background-color":COLORS[3],"margin-top":"2px","height":'20px',"width":"30px","float":"left","border-radius":"5px"}),html.Div(top[4],style={"float":"right","margin-left":"10px","font-weight":"bold", "color":TEXT_COLOR[3]})],style={"float":"left","margin-left":"10px"}),html.Div("{}{}{}{}".format(today_value[4]//60,"h ", today_value[4]%60,"m"),style={"float":"right","margin-right":"10px","font-weight":"bold", "color":TEXT_COLOR[3]})])
    children5 = html.Div([html.Div([html.Div("5",style={"text-align":"center","line-height":"20px","background-color":COLORS[4],"margin-top":"2px","height":'20px',"width":"30px","float":"left","border-radius":"5px"}),html.Div(top[5],style={"float":"right","margin-left":"10px","font-weight":"bold", "color":TEXT_COLOR[4]})],style={"float":"left","margin-left":"10px"}),html.Div("{}{}{}{}".format(today_value[5]//60,"h ", today_value[5]%60,"m"),style={"float":"right","margin-right":"10px","font-weight":"bold", "color":TEXT_COLOR[4]})])
    children6 = html.Div([html.Div([html.Div("6",style={"text-align":"center","line-height":"20px","background-color":COLORS[5],"margin-top":"2px","height":'20px',"width":"30px","float":"left","border-radius":"5px"}),html.Div(top[6],style={"float":"right","margin-left":"10px","font-weight":"bold", "color":TEXT_COLOR[5]})],style={"float":"left","margin-left":"10px"}),html.Div("{}{}{}{}".format(today_value[6]//60,"h ", today_value[6]%60,"m"),style={"float":"right","margin-right":"10px","font-weight":"bold", "color":TEXT_COLOR[5]})])
    
    
    
    return fig, children1, {'background-color': color[0]},children2, {'background-color': color[1]}, children3,{'background-color': color[2]}, children4, {'background-color': color[3]}, children5, {'background-color': color[4]}, children6, {'background-color': color[5]}, fig1, fig2


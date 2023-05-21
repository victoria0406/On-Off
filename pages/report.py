import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, ctx
import plotly.express as px
import pandas as pd 
import math
import plotly.graph_objects as go
from datetime import date, timedelta, datetime

from inputdata.data import COLORS, click, top_apps, keys, top_access, unlocks, today_hour, weekly_hour


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
  'margin' : '-4.5rem 26rem 1.5rem 0',
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

def layout():
    return html.Div(children=[
        html.Div([
                html.Div([
                html.Div([html.Div(html.Img(src='assets/calendar.png', style={'width':'30px', 'height':'30px',}),style={"position":"absolute"}),
                          html.Div(dcc.DatePickerSingle(id="date-picker",clearable=False, with_portal=True, date=date(2019, 5, 6)),style={"position":"relative"}),
                          ],style={"float":"right", "margin-top":'-4.5rem',"width":"62%"}),
                html.Div([html.Div(html.A(html.Button("Compare with Others!",style=BUTTON_STYLE), href="/report/group")),
                html.Div(dbc.Nav([
                    dbc.NavLink("DAILY", href="/report", active="exact"),
                    dbc.NavLink('WEEKLY', href="/report/weekly", active="exact"),
                ],
                className='report-nav'
            ), style=TOGGLE_STYLE)], style={"width":"50%","float":"right"})])
            ], style={'display': 'inline-block','float':"right","width":"100%"}
        ),
        html.Div([
            html.Div([html.P("Apps Top",style={"margin":"10px 0 -5px 10px"}), html.P(id="total_time",style={'font-weight':'bold','font-size':"20px","margin":"-10px 20px -60px 15px",'text-align':'right'}),
                html.Div(dcc.Graph(id="app_graph", config={'displayModeBar': False}),
                style={'margin-left': '-60px', 'margin-bottom':'10px'}),
                html.Div([
                html.Button(id="btn-nclicks-1", n_clicks=0, className='APP_BUTTON_STYLE'),
                html.Button(id="btn-nclicks-2", n_clicks=0, className='APP_BUTTON_STYLE'),
                html.Button(id="btn-nclicks-3", n_clicks=0, className='APP_BUTTON_STYLE'),
                html.Button(id="btn-nclicks-4", n_clicks=0, className='APP_BUTTON_STYLE'),
                html.Button(id="btn-nclicks-5", n_clicks=0, className='APP_BUTTON_STYLE'),
                html.Button(id="btn-nclicks-6", n_clicks=0, className='OTHER_BUTTON_STYLE'),
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
                            html.Div([html.P(id="usage_value"),html.Div(id="usage_differ")]) 
                            ],style=STATISTICS_STYLE),
                    html.Div([html.P("Access",style={'margin-left':'15px','padding-top':'3px','font-size':'14px'}),
                                html.Div([html.P(id="access_value"),html.Div(id="access_differ")])
                            ],style=STATISTICS_STYLE),   
                    html.Div([html.P("Unlock",style={'margin-left':'15px','padding-top':'3px','font-size':'14px'}),
                                html.Div([html.P(id="unlock_value"), html.Div(id="unlock_differ")])
                            ],style=STATISTICS_STYLE),  
                    ], style=FHCONTENT_STYLE),
        ], style = CONTENT_STYLE
        ),
    ])
    
@callback(
    Output("total_time", "children"),
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
    Output('usage_value','children'),
    Output('usage_differ','children'),
    Output('access_value','children'),
    Output('access_differ','children'),
    Output('unlock_value','children'),
    Output('unlock_differ','children'),
        
    Input("date-picker", "date"),
    Input('btn-nclicks-1', 'n_clicks'),
    Input('btn-nclicks-2', 'n_clicks'),
    Input('btn-nclicks-3', 'n_clicks'),
    Input('btn-nclicks-4', 'n_clicks'),
    Input('btn-nclicks-5', 'n_clicks'),
    Input('btn-nclicks-6', 'n_clicks')
)


def update_graph(date,btn1, btn2, btn3, btn4, btn5, btn6):
    global weekly_hour
    usage_time =  pd.read_csv('./datas/usage_time.csv')
    
    date_value=datetime.strptime(date, '%Y-%m-%d')
    yesterday_index = date_value - timedelta(days = 1)
        
    date_value = date_value.strftime('%Y-%m-%d')    
    yesterday_index= yesterday_index.strftime('%Y-%m-%d')

    today_usage_time = usage_time.loc[usage_time['date']==date_value]
    yesterday = usage_time.loc[usage_time['date']==yesterday_index]
    
    others_value =today_usage_time["Others"].values
    total_value = today_usage_time["Total"].values
    yesterday_total =yesterday["Total"].values
    
    today_usage_time=today_usage_time.drop(columns='Total')
    today_usage_time=today_usage_time.drop(columns='Others')
    
    today_usage_time=today_usage_time.dropna(axis=1)
    today_usage_time = today_usage_time.iloc[:, 2:7]
    
    top_app = today_usage_time.iloc[0].sort_values(ascending=False).index.tolist()
    top_app=top_app+["Others"]
    today_usage_time = today_usage_time.reindex(columns=top_app)
    today_usage_time["Others"]=others_value
    # print(today_usage_time)  
    
    today_value = today_usage_time.values.tolist()[0]
    today_usage_time["date"]=date_value
    
    hour = total_value[0]//60
    min = total_value[0]%60

    total_time = html.Div(str(int(hour))+"h "+str(int(min)) +"m Used")

    k = [k for k, v in keys.items() if v == str(date)]
    
    tops = (top_apps[str(k[0])].values.tolist())+["Others"]    

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
        
   
        
    fig = px.bar(today_usage_time, y="date", x=[tops[0],tops[1],tops[2],tops[3],tops[4],tops[5]],orientation='h', color_discrete_sequence=GRAPH_COLOR, width=540, height=90)
    fig.update_xaxes(title=None, showticklabels=False)
    fig.update_yaxes(title=None, showticklabels=False,)
    fig.update_layout(showlegend=False, plot_bgcolor='white',paper_bgcolor="rgb(0,0,0,0)", margin=dict(b=0),hovermode= False)
    
    ######## usage time #############
    today_hour = weekly_hour[k[0]]
    
    today_hour=today_hour.iloc[:, 1:7].reindex(columns=["timestamp",tops[0],tops[1],tops[2],tops[3],tops[4]])    
    pd.to_datetime(today_hour['timestamp'], format = "%Y-%m-%d %H:%M:%S")
    total = pd.DataFrame(data=None, index=None, columns=["time","top1","top2","top3","top4","top5"], dtype=None, copy=False)

    top1=0
    top2=0
    top3=0
    top4=0
    top5=0

    for idx, row in today_hour.iterrows():
        today_time = row[0].split()[1]
        minute=int(today_time.split(":")[0])*60+int(today_time.split(":")[1])
        # print(minute)
        if(not math.isnan(row[1])):
            top1 = row[1]
            total = total.append({'time':minute, 'top1':top1, 'top2':top2, 'top3':top3, 'top4':top4, 'top5':top5},ignore_index=True)
        if(not math.isnan(row[2])):
            top2 = row[2]
            total = total.append({'time':minute, 'top1':top1, 'top2':top2, 'top3':top3, 'top4':top4, 'top5':top5},ignore_index=True)
        if(not math.isnan(row[3])):
            top3 = row[3]
            total = total.append({'time':minute, 'top1':top1, 'top2':top2, 'top3':top3, 'top4':top4, 'top5':top5},ignore_index=True)
        if(not math.isnan(row[4])):
            top4 = row[4]
            total = total.append({'time':minute, 'top1':top1, 'top2':top2, 'top3':top3, 'top4':top4, 'top5':top5},ignore_index=True)
        if(not math.isnan(row[5])):
            top5 = row[5]
            total = total.append({'time':minute, 'top1':top1, 'top2':top2, 'top3':top3, 'top4':top4, 'top5':top5},ignore_index=True)

    total['top1_datetime'] = pd.to_datetime(total['top1'], unit='m')
    total['top1_datetime_string'] = total['top1_datetime'].dt.strftime('%Hh %Mm')
    total['top2_datetime'] = pd.to_datetime(total['top2'], unit='m')
    total['top2_datetime_string'] = total['top2_datetime'].dt.strftime('%Hh %Mm')
    total['top3_datetime'] = pd.to_datetime(total['top3'], unit='m')
    total['top3_datetime_string'] = total['top3_datetime'].dt.strftime('%Hh %Mm')
    total['top4_datetime'] = pd.to_datetime(total['top4'], unit='m')
    total['top4_datetime_string'] = total['top4_datetime'].dt.strftime('%Hh %Mm')
    total['top5_datetime'] = pd.to_datetime(total['top5'], unit='m')
    total['top5_datetime_string'] = total['top5_datetime'].dt.strftime('%Hh %Mm')
    
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=total['time'], y=total['top1'], mode='lines', name=tops[0],line_color=GRAPH_COLOR[0], line=dict(dash=mode[0]),text=total['top1_datetime_string']))
    fig1.add_trace(go.Scatter(x=total['time'], y=total['top2'], mode='lines', name=tops[1],line_color=GRAPH_COLOR[1], line=dict(dash=mode[1]),text=total['top2_datetime_string']))
    fig1.add_trace(go.Scatter(x=total['time'], y=total['top3'], mode='lines', name=tops[2],line_color=GRAPH_COLOR[2], line=dict(dash=mode[2]),text=total['top3_datetime_string']))
    fig1.add_trace(go.Scatter(x=total['time'], y=total['top4'], mode='lines', name=tops[3],line_color=GRAPH_COLOR[3], line=dict(dash=mode[3]),text=total['top4_datetime_string']))
    fig1.add_trace(go.Scatter(x=total['time'], y=total['top5'], mode='lines', name=tops[4],line_color=GRAPH_COLOR[4], line=dict(dash=mode[4]),text=total['top5_datetime_string']))
    fig1.update_layout(
        xaxis = dict(
            title = "Time of Day",
            tickmode = 'array',
            tickvals = [0,240,480,720,960,1200,1440],
            ticktext = ['0', '4', '8', '12', '16', '20','24'],
            showline=True, linewidth=1, linecolor='#BEBEBE',
            
        ),
        yaxis = dict(
            title = "Usage Time (min)",
            tickmode = 'array',
            # tickvals = [0,120,240,360,480,600,720],
            # ticktext = ['0', '2', '4', '6', '8', '10','12'],
            linecolor="#BEBEBE",
            showgrid=True, linewidth=1,gridcolor='#E0E0E0'
        )
    )
    fig1.update_layout(
    hovermode="x unified",
    hoverlabel=dict(
        bordercolor="rgba(0, 0, 0, 0.6)",
        bgcolor="rgba(255, 255, 255,0.8)",
        font_size=14,
        ),
        hoverlabel_namelength=100
        )

    fig1.update_layout(showlegend=False, plot_bgcolor='white',paper_bgcolor="rgb(0,0,0,0)", font=dict(size=9),width=750, height=410)
    fig1.update_traces(hoverinfo = 'name+text')
    
    ###### access graph ######
    
    fig2 = go.Figure()
    today_access = top_access[top_access['Key'] == k[0]]      
    fig2.add_traces(go.Bar(x=today_access["name"], y=today_access['number_of_access'],  marker_color=GRAPH_COLOR, hovertemplate="%{x}: "+"%{y} times"+'<extra></extra>'))
    
    fig2.update_layout(showlegend=False, plot_bgcolor='white',paper_bgcolor="rgb(0,0,0,0)",width=720, height=270, margin=dict(t=0))
    fig2.update_layout(
        yaxis = dict(
            showgrid=True, gridcolor='#E0E0E0',
            zeroline=True, zerolinecolor='#A2A2A2'
        ),
        xaxis = dict(
            title=None, showticklabels=False,
        ),
        hoverlabel=dict(
            bordercolor="rgba(0, 0, 0, 0.6)",
            bgcolor="rgba(255, 255, 255,0.8)",
            font_size=14,
            ),
            hoverlabel_namelength=100
    )

    # print(today)
    
    # today_value=today.values.tolist()[0]
    
                
    children1 = html.Div([html.Div([html.Div("1",style={"text-align":"center","line-height":"20px","background-color":COLORS[0],"margin-top":"2px","height":'20px',"width":"30px","float":"left","border-radius":"5px"}),html.Div(tops[0],style={"float":"right","margin-left":"10px","font-weight":"bold", "color":TEXT_COLOR[0]})],style={"float":"left","margin-left":"10px"}),html.Div("{}{}{}{}".format(int(today_value[0])//60,"h ", int(today_value[0])%60,"m"),style={"float":"right","margin-right":"10px","font-weight":"bold", "color":TEXT_COLOR[0]})])
    children2 = html.Div([html.Div([html.Div("2",style={"text-align":"center","line-height":"20px","background-color":COLORS[1],"margin-top":"2px","height":'20px',"width":"30px","float":"left","border-radius":"5px"}),html.Div(tops[1],style={"float":"right","margin-left":"10px","font-weight":"bold", "color":TEXT_COLOR[1]})],style={"float":"left","margin-left":"10px"}),html.Div("{}{}{}{}".format(int(today_value[1])//60,"h ", int(today_value[1])%60,"m"),style={"float":"right","margin-right":"10px","font-weight":"bold", "color":TEXT_COLOR[1]})])
    children3 = html.Div([html.Div([html.Div("3",style={"text-align":"center","line-height":"20px","background-color":COLORS[2],"margin-top":"2px","height":'20px',"width":"30px","float":"left","border-radius":"5px"}),html.Div(tops[2],style={"float":"right","margin-left":"10px","font-weight":"bold", "color":TEXT_COLOR[2]})],style={"float":"left","margin-left":"10px"}),html.Div("{}{}{}{}".format(int(today_value[2])//60,"h ", int(today_value[2])%60,"m"),style={"float":"right","margin-right":"10px","font-weight":"bold", "color":TEXT_COLOR[2]})])
    children4 = html.Div([html.Div([html.Div("4",style={"text-align":"center","line-height":"20px","background-color":COLORS[3],"margin-top":"2px","height":'20px',"width":"30px","float":"left","border-radius":"5px"}),html.Div(tops[3],style={"float":"right","margin-left":"10px","font-weight":"bold", "color":TEXT_COLOR[3]})],style={"float":"left","margin-left":"10px"}),html.Div("{}{}{}{}".format(int(today_value[3])//60,"h ", int(today_value[3])%60,"m"),style={"float":"right","margin-right":"10px","font-weight":"bold", "color":TEXT_COLOR[3]})])
    children5 = html.Div([html.Div([html.Div("5",style={"text-align":"center","line-height":"20px","background-color":COLORS[4],"margin-top":"2px","height":'20px',"width":"30px","float":"left","border-radius":"5px"}),html.Div(tops[4],style={"float":"right","margin-left":"10px","font-weight":"bold", "color":TEXT_COLOR[4]})],style={"float":"left","margin-left":"10px"}),html.Div("{}{}{}{}".format(int(today_value[4])//60,"h ", int(today_value[4])%60,"m"),style={"float":"right","margin-right":"10px","font-weight":"bold", "color":TEXT_COLOR[4]})])
    children6 = html.Div([html.Div([html.Div("6",style={"text-align":"center","line-height":"20px","background-color":COLORS[5],"margin-top":"2px","height":'20px',"width":"30px","float":"left","border-radius":"5px"}),html.Div("Others",style={"float":"right","margin-left":"10px","font-weight":"bold", "color":TEXT_COLOR[5]})],style={"float":"left","margin-left":"10px"}),html.Div("{}{}{}{}".format(int(today_value[5])//60,"h ", int(today_value[5])%60,"m"),style={"float":"right","margin-right":"10px","font-weight":"bold", "color":TEXT_COLOR[5]})])
    
    ##### statistics #####
    
    children_usage = html.P(str(int(hour))+"h "+str(int(min))+"m", style={'font-weight':"bold",'font-size':'18px','margin':'-12px 0 0 20px',"float":"left"})

    differ=int(total_value[0])-int(yesterday_total[0])

    if (differ>0):
        differ_usage ="+ "+str(differ//60)+"h "+str(differ%60)+"m"
        usage_color="#BBA083"
    else:
        differ = -differ
        differ_usage = "- "+str(differ//60)+"h "+str(differ%60)+"m"
        usage_color="#AEBF9E"
    children_usage_diff = html.Div([html.P(differ_usage,style={"float":"left","margin-right":"10px",'font-size':'15px','color':usage_color}),html.P(" yesterday",style={"float":"right",'font-size':'14px'})],style={"float":"right",'margin':'-12px 15px 0 0'})
    
    access_differ = today_access['number_of_access'].sum() - top_access[top_access['Key'] == (k[0]-1)]['number_of_access'].sum()
    
    if(access_differ>0):
        access_differ = "+ "+ str(access_differ)
        access_color ="#BBA083"
    else:
        access_color="#AEBF9E"
    
    children7 = html.P(today_access['number_of_access'].sum(),style={'font-weight':"bold",'font-size':'18px','margin':'-12px 0 0 20px',"float":"left"})
    children8 = html.Div([html.P(access_differ,style={"float":"left","margin-right":"10px",'font-size':'15px','color':access_color}),html.P(" yesterday",style={"float":"right",'font-size':'14px'})],style={"float":"right",'margin':'-12px 15px 0 0'})
    
    today_unlock = unlocks["0"][k[0]]
    if (k[0]==0):
        differ_unlock=0
    else:
        differ_unlock = today_unlock - unlocks["0"][k[0]-1]
    
    if(differ_unlock>0):
        differ_unlock = "+" + str(differ_unlock)
        unlock_color ="#BBA083"
    else:
        unlock_color="#AEBF9E"
    
    children9 =  html.P(today_unlock,style={'font-weight':"bold",'font-size':'18px','margin':'-12px 0 0 20px',"float":"left"})
    children10 = html.Div([html.P(differ_unlock,style={"float":"left","margin-right":"10px",'font-size':'15px','color':unlock_color}),html.P(" yesterday",style={"float":"right",'font-size':'14px'})],style={"float":"right",'margin':'-12px 15px 0 0'})
    return total_time, fig, children1, {'background-color': color[0]},children2, {'background-color': color[1]}, children3,{'background-color': color[2]}, children4, {'background-color': color[3]}, children5, {'background-color': color[4]}, children6, {'background-color': color[5]}, fig1, fig2, children_usage, children_usage_diff, children7, children8, children9, children10


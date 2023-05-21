import pandas as pd
import datetime


COLORS = ['#F2CB80','#DCD76E','#A7C670','#999BB8','#BBA083','#B5B5B5']
click = [0,0,0,0,0,0]

keys = {0:'2019-04-30',1:'2019-05-01',2:'2019-05-02',3:'2019-05-03',4:'2019-05-04',5:'2019-05-05',6:'2019-05-06'}

top_apps = pd.read_csv('./datas/top_apps.csv')

top_access = pd.read_csv('./datas/access.csv')

app_usage_time = pd.read_csv('./datas/app_usage_time.csv')
weekly_usage =  pd.read_csv('./datas/app_usage_weekly.csv')

today = weekly_usage.loc[weekly_usage['date']=='2019-05-06']
yesterday = weekly_usage.loc[weekly_usage['date']=='2019-05-05']
hour = today['Total']//60
min = today['Total']%60

top=list(app_usage_time)

weekly_hour=[]
weekly_hour.append(pd.read_csv('./datas/usage_hour/app_usage_hour_2019_04_30.csv'))
weekly_hour.append(pd.read_csv('./datas/usage_hour/app_usage_hour_2019_05_01.csv'))
weekly_hour.append(pd.read_csv('./datas/usage_hour/app_usage_hour_2019_05_02.csv'))
weekly_hour.append(pd.read_csv('./datas/usage_hour/app_usage_hour_2019_05_03.csv'))
weekly_hour.append(pd.read_csv('./datas/usage_hour/app_usage_hour_2019_05_04.csv'))
weekly_hour.append(pd.read_csv('./datas/usage_hour/app_usage_hour_2019_05_05.csv'))
weekly_hour.append(pd.read_csv('./datas/usage_hour/app_usage_hour_2019_05_06.csv'))


today_hour = pd.read_csv('./datas/usage_hour/app_usage_hour_2019_05_06.csv')

unlocks = pd.read_csv('./datas/unlocks.csv')

date = list(keys.values())
    
for i in range(len(date)):
    date[i] = datetime.datetime.strptime(date[i], '%Y-%m-%d')
for i in range(len(date)):
    date[i] = date[i].strftime("%m/%d")
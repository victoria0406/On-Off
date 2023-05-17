import pandas as pd 


COLORS = ['#F2CB80','#DCD76E','#A7C670','#999BB8','#BBA083','#B5B5B5']
click = [0,0,0,0,0,0]

keys = {0:'2023-04-30',1:'2023-05-01',2:'2023-05-02',3:'2023-05-03',4:'2023-05-04',5:'2023-05-05',6:'2023-05-06'}

top_apps = pd.read_csv('./datas/top_apps.csv')
top_access = pd.read_csv('./datas/access.csv')

app_usage_time = pd.read_csv('./datas/app_usage_time.csv')
today = app_usage_time.loc[app_usage_time['date']=='2023-05-10']
yesterday = app_usage_time.loc[app_usage_time['date']=='2023-05-09']
top=list(app_usage_time)

hour = today['Total']//60
min = today['Total']%60

app_usage_hour = pd.read_csv('./datas/app_usage_hour.csv')


access = pd.read_csv('./datas/number_of_access.csv')

today_index = int(str(today['Total']).split()[0])

unlock = pd.read_csv('./datas/unlock.csv')

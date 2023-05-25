# Project URL
1. [Demo URL](https://peaceful-crag-15889.herokuapp.com/)
2. [Process Book](https://docs.google.com/presentation/d/16AtV0y9rWk-fDFNBUmKehER1nrsT19TNYdMwWu50WJ4/edit#slide=id.g2498668c554_1_349)
3. [Data processing](https://colab.research.google.com/drive/19UDCfamF_I6yBzntQ-LMky5Fkevur-H8#scrollTo=thMXKmUQK0Az)

# Installation
```console
pip install -r requirements.txt
```

Required libraries <br/>
```console
colorama==0.4.6
contourpy==1.0.7
cycler==0.11.0
dash==2.8.1
dash-bootstrap-components==1.4.1
dash-core-components==2.0.0
dash-html-components==2.0.0
dash-table==5.0.0
Flask==2.3.1
fonttools==4.39.3
idna==3.4
itsdangerous==2.1.2
Jinja2==3.1.2
kiwisolver==1.4.4
MarkupSafe==2.1.2
matplotlib==3.7.1
numpy==1.24.3
packaging==23.1
pandas==1.5.3
Pillow==9.5.0
plotly==5.13.1
pyparsing==3.0.9
python-dateutil==2.8.2
pytz==2023.3
requests==2.30.0
six==1.16.0
tenacity==8.2.2
tzdata==2023.3
urllib3==2.0.2
Werkzeug==2.3.0
gunicorn==20.1.0
```

# Directory
## 1. pages: Each page will have a router applied
   - root.py: Initial page
   - goal.py: Initially, you can set a goal, and after setting a goal, it shows the daily goal achievement rate
   - report.py: Shows the user's phone usage pattern for a specific date
   - weekly.py: Shows the user's weekly phone usage pattern
   - group.py: Assigns users to specific groups based on their usage patterns and compares the average within the group with the user's pattern

## 2. component: There are additional components <br/>
   Files in this folder
   - The code to create a component is too long
   - In case of creating reusable components

## 3. data: Contains data used for data visualization (except for the file for all users, values of 'P3016' user are used)
   - access.csv: Top 5 apps in terms of user access count over 7 days
   - app_usage_weekly.csv: Total usage of the top 5 apps used by the user for a week
   - goal_states.csv: Goal time and practice time
   - {goal name}_real: Actual usage time of the day
   - {goal name}_goal: Daily goal usage time
   - app_usage_app: Application used as a usage goal
       - Relevant data is treated as NA on days when there is no goal
   - screen_on.csv: Number of times the user turned on the screen over 7 days (irrelevant to unlocking)
   - top_apps.csv: Top 5 most used apps by the user (for 7 days)
   - total_user_usage.csv: Average total usage / session duration of all users over 7 days (used for checking 2d - distribution for groups)
   - total_user_usage_whole.csv: Total usage and session duration of all users over 7 days
   - unlock.csv: Number of times unlocked in a day (for 7 days)
   - usage_time.csv: Total daily usage by app over 7 days
   - weekly_access.csv: Daily access count by app over 7 days

## File Directory
1. pages: Each page will have a router applied
   - goal.py: Initially, you can set a goal, and after setting a goal, it shows the daily goal achievement rate
   - report.py: Shows the user's phone usage pattern for a specific date
   - weekly.py: Shows the user's weekly phone usage pattern
   - group.py: Assigns users to specific groups based on their usage patterns and compares the average within the group with the user's pattern

2. component: There are additional components <br/>
   Files in this folder
   - The code to create a component is too long
   - In case of creating reusable components

3. data: Contains data used for data visualization (except for the file for all users, values of 'P3016' user are used)
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

## Commands
1. pip install -r requirements.txt <br/>
   Install the packages used
2. git checkout -b dev/"name" <br/>
   Create and checkout a branch
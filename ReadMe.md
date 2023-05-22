## 파일 구조 설명
1. pages: router 적용될 페이지가 각각 존재
   - goal.py: 초기에는 목표를 설정할 수 있고, 목표 설정 이후에는 당일 목표 당성률을 보여줌
   - report.py: user의 해당 날짜의 핸드폰 사용 패턴을 보여줌
   - weekly.py: user의 한 주간 핸드폰 사용 패턴을 보여줌
   - group.py: user의 사용패턴에 따라 특정 그룹에 assign하고 해당 그룹 내에서의 평균과 user의 패턴을 비교

2. component: 부가적인 component가 존재 <br/>
   해당 폴더에 들어가는 파일
   - 하나의 component에 생성에 코드가 너무 김
   - 재사용되는 component를 만들 경우

3. data: data visulization에 사용한 data가 존재(모든 유저에 대한 파일 제외하고는 'P3016' 유저의 값 사용)
   - access.csv: 7일 간 유저의 사용량 top 5 앱들 접속 횟수
   - app_usage_weekly.csv: 유저가 1주일동안 총 사용한 top 5 앱 사용량
   - goal_states.csv: 목표 시간과 실천 시간 <br />
      - {목표명}_real: 당일 실제 사용 시간
      - {목표명}_goal: 당일 목표 사용 시간
      - app_usage_app: 사용 목표 어플리케이션 
      - 해당 목표가 없는 날은 관련 데이터 NA로 처리
   - screen_on.csv: 7일 간 유저가 화면을 킨 횟수(unlock과 무관)
   - top_apps.csv: 유저가 가장 많이 사용한 앱 5개 (7일치)
   - total_user_usage.csv: 모든 user의 7일 간 <b>평균</b> total usage / session duraion (group 을 확인하기 위한 2d distribution 에 사용)
   - total_user_usage_whole.csv: 모든 user의 7일 간 total usage와 session duration
   - unlock.csv: 하루동안 unlock한 횟수 (7일치)
   - usage_time.csv: 7일 간 앱 별 하루 총 사용량
   - weekly_access.csv: 7일 간 앱 별 하루 접속 횟수
   

## Commands
1. pip install -r requirements.txt <br/>
    사용된 패키지 설치
2. git checkout -b dev/이름 <br/>
   브랜치 생성 및 체크아웃
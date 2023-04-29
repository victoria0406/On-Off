## Commands
1. pip install -r requirements.txt <br/>
    사용된 패키지 설치
2. git checkout -b dev/이름 <br/>
   브랜치 생성 및 체크아웃

## 파일 구조 설명
1. pages: router 적용될 페이지가 각각 존재
2. component: 부가적인 component가 존재 <br/>
    해당 폴더에 들어가는 파일
    - 하나의 component에 생성에 코드가 너무 김
    - 재사용되는 component를 만들 경우
3. datas
   더미 데이터 파일들
   - app_usage_time.csv: 앱 별 하루 총 사용량 데이터 (9일치)
   - app_usage_hour.csv: 앱 별 시간 별 사용량 (NA 는 해당 어플리케이션을 그 시간에 사용하지 않았다는 의미)
   - unlock.csv: 하루 unlock 횟수 (9일치)
   - total_user_usage.csv: 모든 사람들의 total usage / session duraion (group 을 확인하기 위한 2d distribution 에 사용)
   - goal_status.csv: 목표 시간과 실천 시간 <br />
      - {목표명}_real: 당일 실제 사용 시간
      - {목표명}_goal: 당일 목표 사용 시간
      - app_usage_app: 사용 목표 어플리케이션 
      - 해당 목표가 없는 날은 관련 데이터 NA로 처리
   - weekly_average.csv: user와 group의 요일 별 평균 사용량

## 편의를 위해 sidebar에 group page 목록 추가
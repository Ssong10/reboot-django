# 전생 app

* `**` 님은 전생에 선생님이었습니다.

1. 

2. Form : 이름을 받아서

3. 직업 랜덤 추출

   ```python
   fake.job() 을 통해서
   >>> fake = Faker('ko_KR')
   
   fake.date_between(start_date="-30y", end_date="today")
   # datetime.date(2012, 1, 20)
   ```

   

4. 결과를 출력

   1. DB에 등록된 이름이 있으면, 해당하는 결과 출력
   2. 이름이 없으면 새롭게 DB에 추가하고, 결과 출력

uFyNcRYg7k8TZn0AIk6K6sifVlWpvQdc
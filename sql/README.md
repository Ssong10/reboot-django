# SQL과 django ORM

## 기본 준비 사항

* https://bit.do/djangoorm에서 csv 파일 다운로드

* django app

  * `django_extensions` 설치

  * `users` app 생성

  * csv 파일에 맞춰 `models.py` 작성 및 migrate

    아래의 명령어를 통해서 실제 쿼리문 확인

    ```bash
    $ python manage.py sqlmigrate users 0001	
    ```

* `db.sqlite3` 활용

  * `sqlite3`  실행

    ```bash
    $ ls
    db.sqlite3 manage.py ...
    $ sqlite3 db.sqlite3
    ```

  * csv 파일 data 로드

    ```sqlite
    sqlite > .tables
    auth_group                  django_admin_log
    auth_group_permissions      django_content_type
    auth_permission             django_migrations
    auth_user                   django_session
    auth_user_groups            auth_user_user_permissions  
    users_user
    sqlite > .mode csv
    sqlite > .import users.csv users_user
    sqlite > SELECT COUNT(*) FROM user_users;
    100
    ```

* 확인

  * sqlite3에서 스키마 확인

    ```sqlite
    sqlite > .schema users_user
    CREATE TABLE IF NOT EXISTS "users_user" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "first_name" varchar(10) NOT NULL, "last_name" varchar(10) NOT NULL, "age" integer NOT NULL, "country" varchar(10) NOT NULL, "phone" varchar(15) NOT NULL, "balance" integer NOT NULL);
    ```

    

## 문제

> 아래의 문제들을 sql문과 대응되는 orm을 작성 하세요.

### 기본 CRUD 로직

1. 모든 user 레코드 조회

   ```python
   # orm
   User.objects.all()
   ```

      ```sql
   -- sql
   SELECT * FROM users_user
      ```

2. user 레코드 생성

   ```python
   # orm
   User.objects.create(first_name='승열',last_name='이',age=27,
                       country='충청남도',phone='010-5533-9382',balance=10000)
   
   
   # 2.
   user = User()
   user.first_name = '길동'
   ...
   user.save()
   ```

   ```sql
   -- sql
   INSERT INTO users_user VALUES ('승열','이',27,'충청남도','010-5533-9382',10000)
   ```

   * 하나의 레코드를 빼고 작성 후 `NOT NULL` constraint 오류를 orm과 sql에서 모두 확인 해보세요.

3. 해당 user 레코드 조회

   ```python
   # orm
   User.objects.get(first_name='승열')
   ```

      ```sql
   -- sql
   SELECT * FROM users_user WHERE first_name='승열';
      ```

4. 해당 user 레코드 수정

   ```python
   # orm
   user = User.objects.get(first_name='승열')
   user.balance = 10000000
   user.save()
   ```

      ```sql
   -- sql
   UPDATE users_user SET balance= 1000000 WHERE first_name='승열'
      ```

5. 해당 user 레코드 삭제

   ```python
   # orm
   user = User.objects.get(first_name='승열')
user.delete()
   ```
   
      ```sql
   -- sql
   DELETE FROM users_user WHERE first_name='승열'
      ```

### 조건에 따른 쿼리문

1. 전체 인원 수 

   ```python
   # orm
   User.objects.count()
   ```

      ```sql
   -- sql
   SELECT COUNT(*) FROM users_user;
      ```

2. 나이가 30인 사람의 이름

   ```python
   # orm
   User.objects.filter(age=30).values('first_name')
   ```

      ```sql
   -- sql
   SELECT first_name FROM users_user WHERE age =30;
      ```

3. 나이가 30살 이상인 사람의 인원 수

   > gte : 이상
   >
   > gt : 초과
   >
   > lte : 이하
   >
   > lt : 미만

   ```python
   # orm
   User.objects.filter(age__gte=30).count()
   ```

   ```sql
   -- sql
   SELECT count(*) FROM users_user WHERE age >=30;
   ```

4. 나이가 30이면서 성이 김씨인 사람의 인원 수

   ```python
   # orm
   User.objects.filter(age=30,last_name='김').count()
   User.objects.filter(age=30).filter(last_name='김').count()
   ```

   ```sql
   -- sql
   SELECT count(*) FROM users_user WHERE age =30 and last_name='김';
   ```

5. 지역번호가 02인 사람의 인원 수

   > exact : 정확히 같을 때 (iexact)
   >
   > contains : 포함하는지 (icontains)
   >
   > startswith : 시작 값이 같을 때 (istartswith)
   >
   > endswith : 끝나는 값이 같을 때 (iendswith)
   >
   > i -> case insensitive(대소문자 무시)

   ```python
   # orm
   User.objects.filter(phone__startswith='02-').count()
   ```

      ```sql
   -- sql
   SELECT count(*) FROM users_user WHERE phone LIKE '02-%';
      ```

6. 거주 지역이 강원도이면서 성이 황씨인 사람의 이름

   ```python
   # orm
   User.objects.filter(country='강원도',last_name='황').values('first_name')
   ```
    ```sql
   -- sql
   SELECT first_name FROM users_user WHERE country='강원도' and last_name='황';
    ```



### 정렬 및 LIMIT, OFFSET

1. 나이가 많은 사람 10명

   ```python
   # orm
   User.objects.order_by('-age')[:10].values('age','first_name')
   ```

      ```sql
   -- sql
   SELECT age,first_name FROM users_user ORDER BY age DESC LIMIT 10;
      ```

2. 잔액이 적은 사람 10명

   ```python
   # orm
   User.objects.order_by('balance')[:10].values('first_name','balance')
   ```

      ```sql
   -- sql
   SELECT first_name, balance FROM users_user ORDER BY balance LIMIT 10;
      ```

3. 성, 이름 내림차순 순으로 5번째 있는 사람

      ```python
   # orm
   User.objects.order_by('-last_name','-first_name')[4:5].values('last_name','first_name')
   ```
    ```sql
   -- sql
   SELECT last_name, first_name FROM users_user
   ORDER BY last_name DESC, first_name DESC LIMIT 1 OFFSET 4;
    ```



### 표현식

1. 전체 평균 나이

   ```python
   # orm
   from django.db.models import Avg
   User.objects.aggregate(Avg('age'))
   > {'age__avg': 28.23}
   ```

      ```sql
   -- sql
   SELECT AVG(age) FROM users_user;
      ```

2. 김씨의 평균 나이

   ```python
   # orm
   from django.db.models import Avg
   User.objects.filter(last_name='김').aggregate(Avg('age'))
   > {'age__avg': 28.782608695652176}
   ```

      ```sql
   -- sql
   SELECT AVG(age) FROM users_user WHERE last_name='김'
      ```

3. 계좌 잔액 중 가장 높은 값

   ```python
   # orm
   User.objects.aggregate(Max('balance'))
   > {'balance__max': 1000000}
   ```

      ```sql
   -- sql
   SELECT MAX(balance) FROM users_user;
      ```

4. 계좌 잔액 총액

      ```python
   # orm
   User.objects.all().aggregate(Sum('balance'))
	{'balance__sum': 14425040}
	```

    ```sql
   -- sql
   SELECT SUM(balance) FROM users_user;
    ```
# Django

## Model 정의

* title : charfield
* content : textfield
* created_at : auto_now_add ,  datetimefield
* updated_at : auto_now , datetimefield

## CRUD

* C
  *  `/new` : 글 작성 form
  * `/create/` : 저장 후 index로 보내기(`redirect`) 

* R
  * `/1/` : detail 함수에서 처리

* D
  * `/1/delete/` : 삭제 후 index로 보내기
* U
  * `1/edit/` : 글 수정 form
  * `1/update/` : 저장 후 Read로 보내기



## 1:N 관계 설정하기

```python


6. 각 reporter의 article들 조회
## reporter1.article_set.all()
7. article1에 댓글 두개 추가
## comment1_2 = Comment.objects.create(content='댓글2번',article=article1)
8. 마지막 댓글의 기사를 작성한 기자
## comment1_2.article.reporter
9. 기사별 댓글 내용 출력
# articles = Article.objects.all()
# for article in articles:
#      for comment in article.comment_set.all():
#          print(comment.content)
10. 기자별 기사 내용 출력
# reporters = Reporter.objects.all()
# for reporter in reporters:
#      print(reporter.name)
#      for article in reporter.article_set.all():
#          print(article.title)
11. 기자별 기사 갯수, 댓글 갯수 출력
# reporter1.article_set.count()
# article1.comment_set.count()
```


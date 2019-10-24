from django.db import models

# Create your models here.
    
class User(models.Model):
    username = models.CharField(max_length=15)

class Article(models.Model):
    title = models.CharField(max_length=30)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class Comment(models.Model):
    content = models.CharField(max_length=40)
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

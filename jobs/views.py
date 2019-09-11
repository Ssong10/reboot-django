from django.shortcuts import render, redirect
from .models import Users
from faker import Faker
from decouple import config
import requests
import random

# Create your views here.

def index(request):
    return render(request,'jobs/index.html')

def result(request):
    if request.method =='POST':
        name = request.POST.get('name')
        user = Users.objects.filter(name=name).first()
        if not user:
            user = Users()
            fake = Faker('ko_KR')
            user.name = name
            user.address = fake.address()
            user.job = fake.job()
            user.birthday = fake.date_between(start_date="-50y", end_date="-20y")
            user.save()
        # 작업 결과에 따라, giphy 요청
        
        api_key = config('GIPHY_API_KEY')
        job = user.job.split()[0]
        print(job)
        # 1. url 설정
        url = f'http://api.giphy.com/v1/gifs/search?api_key={api_key}&q={job}&lang=ko'
        # 2. 요청 보내기
        response = requests.get(url).json()
        # 3. 응답결과에서 이미지 url 뽑기
        if response.get('data'):
            rnd = random.choice(range(len(response['data'])))
            image_url = response['data'][rnd].get('images').get('original').get('url')
        else:
            image_url = None
        context = {
            'user' : user,
            'image_url' : image_url,
        }
        return render(request,'jobs/result.html', context)
        
    else:
        return redirect('jobs:index')
def delete(request):
    Users.objects.all().delete()
    # for user in alluser:
    #     user.delete()
    return redirect('jobs:index')
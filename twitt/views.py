from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from . models import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os
import pandas as pd 


#import tensorflow as tf
import re

sid = SentimentIntensityAnalyzer()
# Create your views here.
max_fatures = 2000
data = pd.read_csv('train.csv')
data.dropna()
data = data[['text','sentiment']]
data = data[data.sentiment != "neutral"]
data['text'] = data['text'].apply(lambda x: x.lower())
data['text'] = data['text'].apply((lambda x: re.sub('[^a-zA-z0-9\s]','',x)))



#@login_required(login_url='login')
def home(request):
    return render(request,'index.html')

@login_required(login_url='login')
def chat(request):
    if request.method=="POST":
        feedback = request.POST['feedback']
        sid = SentimentIntensityAnalyzer()
        ss = sid.polarity_scores(feedback)
        print(ss)
        db = Chat(text=feedback,user=request.user,score=ss)
        db.save()
        return redirect('report')

    return render(request,'feedback.html')

def app_login(request):
    if request.method=="POST":
        score=0
        name = request.POST['username']
        password = request.POST['password']
    
        user = authenticate(username=name, password=password)
        login(request=request,user=user)
        return redirect('index')
    return render(request,'login.html')

def app_logout(request):
    logout(request)
    return redirect('index')

def report(request):
    db = Chat.objects.all()
    return render(request,'report.html',{'reports':db})


def app_signup(request):
    if request.method=="POST":
        name = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_user(username=name,password=password,email=email)
        user.save()
        return redirect('login')
    return render(request,'signup.html')

@login_required(login_url='login')
def add_comment(request):
    if request.method=='POST':
        comment = request.POST['feedback']
        ss = sid.polarity_scores(comment)
        db = Chat(user=request.user,text=comment,positive=ss['pos'],negative=ss['neg'],neutral=ss['neu'])
        db.save()
        ss = sid.polarity_scores(comment)
        pos = ss['pos']
        neg = ss['neg']
        neu = ss['neu']
        return render(request,"feedback.html",{'pos':pos,'neu':neu,'neg':neg})
    return render(request,"feedback.html",{})

def report(request):
    db = Chat.objects.all()
    return render(request,'report.html',{'db':db})

def chart(request):
    db = Chat.objects.all()
    return render(request,'chart.html',{'db':db})

from django.urls import path
from .views import *
urlpatterns = [
    path('',home,name="index" ),
    path('signup',app_signup,name="signup" ),
    path('login',app_login,name="login" ),
    path('logout',app_logout,name="logout" ),
    path('chat',add_comment,name="chat"),
    path('report',report,name="report"),
    path('chart',chart,name="chart"),

]

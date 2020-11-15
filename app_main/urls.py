from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.intro, name = "intro"),
    path('login',views.login, name = "login"),
    path('register', views.register, name = "register"),
    path('home', views.home, name = "home"),
    path('logout', views.logout, name = "logout"),
    path('speechsum', views.speechsum, name = 'speechsum'),
    path('textsum', views.textsum, name = 'textsum'),
    path('speechlist', views.speechlist, name = 'speechlist'),
    path('textlist', views.textlist, name = 'textlist'),
    path('maketextsummary', views.maketextsummary, name = 'maketextsummary'),
    path('maketextlist', views.maketextlist, name = 'maketextlist'),
    path('makespeechlist', views.makespeechlist, name = "makespeechlist"),
    path('makespeechsum', views.makespeechsum, name = "makespeechsum")
]

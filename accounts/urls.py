from django.conf.urls import url
from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('', views.login, name='login'),
    url(r'logout/$', views.pagelogout, name='logout'),
]

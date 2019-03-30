from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'info'

urlpatterns = [
    path('test', views.test, name='test'),
    path('all_history', views.request_all_history, name="request_all_history")
]
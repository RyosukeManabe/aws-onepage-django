from django.contrib import admin
from django.urls import path
from .views import formfunc

app_name = 'hpformapp'

urlpatterns = [
    path('form/', formfunc, name='form'),
]
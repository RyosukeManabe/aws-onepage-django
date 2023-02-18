from django.contrib import admin
from django.urls import path
from .views import formfunc,privacypolicyfunc,termsfunc,rootfunc

app_name = 'instaformapp'
urlpatterns = [
    path('form/', formfunc, name='form'),
    path('privacy-policy',privacypolicyfunc, name='privacy-policy'),
    path('terms',termsfunc, name='terms'),
    path('',rootfunc, name='root'),
]
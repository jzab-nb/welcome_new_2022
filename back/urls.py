from django.urls import path
from .views import index, login, check, check_in, report, show, lbt, notice, api

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('check/', check, name='check'),
    path('check_in/', check_in, name='check_in'),
    path('report/', report, name='report'),
    path('show/', show, name='show'),
    path('lbt/', lbt, name='lbt'),
    path('noticemanger/', notice, name='notice'),
    path('api/', api, name='api')
]

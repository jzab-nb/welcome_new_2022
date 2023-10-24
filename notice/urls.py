from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', notice),
    path('read', read),
    re_path(r'^lbt', lbt),
]
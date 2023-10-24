from django.urls import path
from .views import answer, is_pass


urlpatterns = [
    path('', answer),
    path('is_pass', is_pass)
]

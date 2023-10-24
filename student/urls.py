from rest_framework import routers
from .views import InfoViewSet, StudentViewSet, ReportInfoViewSet, image

from django.urls import include, re_path, path

router = routers.DefaultRouter()
router.register(r'info', InfoViewSet)
router.register(r'student', StudentViewSet)
router.register(r'report_info', ReportInfoViewSet)

urlpatterns = [
    path('image', image),
    re_path('^', include(router.urls)),
]

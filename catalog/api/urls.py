from django.urls import include, path
from rest_framework import routers
from . import viewsets


router = routers.DefaultRouter()
router.register(r'releases', viewsets.ReleaseViewSet, basename='release')
router.register(r'zones', viewsets.ZoneViewSet, basename='zone')

urlpatterns = router.urls

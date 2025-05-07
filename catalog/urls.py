from django.urls import path
from . import views


urlpatterns = [
    path('skins/', views.skin_list, name='skin_list'),
]

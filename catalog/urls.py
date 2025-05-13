from django.urls import path
from . import views


urlpatterns = [
    path('collections/', views.collection_list, name='collection_list'),
    path('skins/', views.skin_list, name='skin_list'),
]

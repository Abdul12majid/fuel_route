from . import views
from django.urls import path

urlpatterns = [
    path('', views.index),
    path('get_route', views.get_route),
]

from django.urls import path
from . import views

# create url link here

urlpatterns = [
    path('', views.home, name='home'),
    path('VolveFieldDataSet/', views.volveFieldDataSet, name='volveFieldDataSet')
]
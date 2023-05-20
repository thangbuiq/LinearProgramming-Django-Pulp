from django.urls import path
from . import views

urlpatterns = [
    path('', views.lp_solve, name='lp_solve'),
]

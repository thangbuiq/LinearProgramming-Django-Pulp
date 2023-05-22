from django.urls import path
from lp.views import lp_solve

urlpatterns = [
    path('', lp_solve),
]

from django.urls import path
from . import views
from .views.exit_parking import exit_parking

urlpatterns = [
    path('', views.enter_parking_view, name='enter_parking'),
    path("exit/", exit_parking, name="exit_parking"),
]
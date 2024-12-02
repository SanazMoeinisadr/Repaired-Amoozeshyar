from django.urls import path
from . import views

urlpatterns = [
    path("", views.homePage, name="Home"),
    path("contactUs", views.contactUS, name="contactUs"),
]
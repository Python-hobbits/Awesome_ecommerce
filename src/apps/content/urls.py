from django.shortcuts import render
from django.urls import path

from src.apps.content.views import IndexView


urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]

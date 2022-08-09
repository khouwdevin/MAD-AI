from django.conf.urls import url, include
from django.contrib import admin

from . import views
from about import views as aboutViews

urlpatterns = [
    url(r'^$', views.checking),
]
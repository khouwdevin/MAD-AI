from django.conf.urls import url, include
from django.contrib import admin

from . import views
from checking import views as checkingViews

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home),
    url(r'^chatbotpage/', include('checking.urls')),
    url(r'^aboutus/', include('about.urls')),
    url(r'^booking/', views.booking),
]

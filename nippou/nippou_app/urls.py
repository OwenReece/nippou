from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r"^list/", views.list_view, name="list_view"),
    url('^registration/login', views.login, name="login"),
    url('^registration/logout', views.logout, name="logout"),
]

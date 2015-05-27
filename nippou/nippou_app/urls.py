from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r"^document/(?P<nippou_id>[0-9]+)/edit", views.edit, name="edit"),
    url(r"^document/(?P<nippou_id>[0-9]+)/delete", views.delete, name="delete"),
    url(r"^document/(?P<nippou_id>[0-9]+)/", views.detail, name="detail"),
    url(r"^document/", views.view, name="view"),
    url('^registration/login', views.login, name="login"),
    url('^registration/logout', views.logout, name="logout"),
]

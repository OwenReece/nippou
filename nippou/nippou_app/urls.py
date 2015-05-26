from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r"^document/(?P<nippou_id>[0-9]+)/", views.editor, name="edit"),
    url(r"^document/", views.viewer, name="view"),
    url('^registration/login', views.login, name="login"),
    url('^registration/logout', views.logout, name="logout"),
]

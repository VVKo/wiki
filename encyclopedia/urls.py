from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<TITLE>", views.entry, name="entry"),
    path("wiki/edit/<TITLE>", views.edit, name="edit"),
    path("wiki/search/", views.search, name="search"),
    path("wiki/create/", views.create, name="create")
]

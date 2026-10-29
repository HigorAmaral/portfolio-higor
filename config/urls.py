from django.contrib import admin
from django.urls import path

from recados import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/recados/", views.recados, name="recados"),
    path("api/conteudo/", views.conteudo, name="conteudo"),
    path("", views.index, name="index"),
]

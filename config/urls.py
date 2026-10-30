import os
from django.contrib import admin
from django.urls import path

from recados import views

# Rota do painel de administração configurável por variável de ambiente para segurança avançada
admin_slug = os.environ.get("ADMIN_URL", "admin").strip("/") or "admin"

urlpatterns = [
    path(f"{admin_slug}/", admin.site.urls),
    path("healthz/", views.healthz, name="healthz"),
    path("api/docs/", views.api_docs, name="api_docs"),
    path("api/docs/schema.json", views.api_schema, name="api_schema"),
    path("api/visitas/", views.visitas, name="visitas"),
    path("api/recados/", views.recados, name="recados"),
    path("api/conteudo/", views.conteudo, name="conteudo"),
    path("", views.index, name="index"),
]

# Páginas de erro personalizadas (HTML no site, JSON na API)
handler400 = "recados.erros.erro_400"
handler403 = "recados.erros.erro_403"
handler404 = "recados.erros.erro_404"
handler500 = "recados.erros.erro_500"

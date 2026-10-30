from django.contrib import admin

from .models import Habilidade, Projeto, Recado

admin.site.site_header = "Painel do portfólio"
admin.site.site_title = "Painel do portfólio"


@admin.register(Recado)
class RecadoAdmin(admin.ModelAdmin):
    list_display = ("nome", "texto", "criado_em", "visivel")
    list_editable = ("visivel",)
    list_filter = ("visivel", "criado_em")
    search_fields = ("nome", "texto")


@admin.register(Habilidade)
class HabilidadeAdmin(admin.ModelAdmin):
    list_display = ("titulo", "tecnologias", "ordem", "visivel")
    list_editable = ("ordem", "visivel")


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ("nome", "status", "github", "demo", "ordem", "visivel")
    list_editable = ("status", "ordem", "visivel")
    list_filter = ("status", "visivel")
    search_fields = ("nome", "descricao")

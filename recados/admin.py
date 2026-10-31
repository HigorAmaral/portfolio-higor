import csv
from django.contrib import admin
from django.db.models import Sum
from django.http import HttpResponse

from .models import Habilidade, LinkContato, MetricaAcesso, Projeto, Recado

admin.site.site_header = "Painel do portfólio"
admin.site.site_title = "Painel do portfólio"


class RespondidoListFilter(admin.SimpleListFilter):
    """Filtro rápido para separar recados já respondidos daqueles pendentes de resposta."""

    title = "Status da resposta"
    parameter_name = "respondido"

    def lookups(self, request, model_admin):
        return (
            ("pendente", "Aguardando resposta"),
            ("respondido", "Já respondidos"),
        )

    def queryset(self, request, queryset):
        if self.value() == "pendente":
            return queryset.filter(resposta="")
        if self.value() == "respondido":
            return queryset.exclude(resposta="")
        return queryset


@admin.register(Recado)
class RecadoAdmin(admin.ModelAdmin):
    list_display = ("nome", "texto", "tem_resposta", "criado_em", "visivel")
    list_editable = ("visivel",)
    list_filter = ("visivel", RespondidoListFilter, "criado_em")
    search_fields = ("nome", "texto", "resposta")
    readonly_fields = ("criado_em", "respondido_em")
    actions = ["marcar_visivel", "marcar_oculto"]
    fieldsets = (
        ("Recado do Visitante", {"fields": ("nome", "texto", "criado_em", "visivel")}),
        (
            "Resposta do Higor (Pública)",
            {
                "fields": ("resposta", "respondido_em"),
                "description": "Preencha para responder ao visitante. A resposta e a data aparecerão no mural do portfólio.",
            },
        ),
    )

    @admin.display(boolean=True, description="Respondido?")
    def tem_resposta(self, obj):
        return bool(obj.resposta)

    @admin.action(description="Tornar recados selecionados visíveis no mural")
    def marcar_visivel(self, request, queryset):
        qtd = queryset.update(visivel=True)
        self.message_user(request, f"{qtd} recado(s) marcado(s) como visível.")

    @admin.action(description="Ocultar recados selecionados do mural")
    def marcar_oculto(self, request, queryset):
        qtd = queryset.update(visivel=False)
        self.message_user(request, f"{qtd} recado(s) ocultado(s).")


@admin.register(Habilidade)
class HabilidadeAdmin(admin.ModelAdmin):
    list_display = ("titulo", "tecnologias", "ordem", "visivel")
    list_editable = ("ordem", "visivel")


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ("nome", "status", "badge", "github", "demo", "ordem", "visivel")
    list_editable = ("status", "ordem", "visivel")
    list_filter = ("status", "visivel")
    search_fields = ("nome", "descricao", "estudo_titulo", "estudo_desafio")
    fieldsets = (
        (
            "Informações Básicas",
            {
                "fields": ("nome", "descricao", "tecnologias", "status", "ordem", "visivel"),
            },
        ),
        (
            "Links & Destaque",
            {
                "fields": ("badge", "github", "demo", "pdf"),
                "description": "Links externos, selo de destaque no card e link para PDF/monografia.",
            },
        ),
        (
            "Estudo de Caso (Modal no Portfólio)",
            {
                "fields": (
                    "estudo_titulo",
                    "estudo_desafio",
                    "estudo_solucao",
                    "estudo_aprendizados",
                ),
                "description": "Conteúdo exibido no modal 'Estudo de Caso' ao clicar no card do projeto.",
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(LinkContato)
class LinkContatoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "chave", "url", "ordem", "visivel")
    list_editable = ("ordem", "visivel")
    search_fields = ("titulo", "url", "chave")
    list_filter = ("visivel", "chave")


@admin.register(MetricaAcesso)
class MetricaAcessoAdmin(admin.ModelAdmin):
    list_display = ("data", "caminho", "visualizacoes", "downloads_curriculo")
    list_filter = ("caminho", "data")
    date_hierarchy = "data"
    search_fields = ("caminho",)
    readonly_fields = ("data", "caminho", "visualizacoes", "downloads_curriculo")
    actions = ["exportar_csv"]

    @admin.action(description="Exportar métricas selecionadas para CSV")
    def exportar_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="metricas_acesso.csv"'
        response.write("\ufeff")  # BOM UTF-8 para Excel abrir acentos perfeitamente
        writer = csv.writer(response)
        writer.writerow(["Data", "Caminho", "Visualizações", "Downloads de Currículo"])
        for m in queryset:
            writer.writerow([m.data.isoformat(), m.caminho, m.visualizacoes, m.downloads_curriculo])
        return response


# Injeção de KPIs no dashboard inicial do Django Admin
_original_index = admin.site.index


def _custom_admin_index(request, extra_context=None):
    extra = extra_context or {}
    agregado = MetricaAcesso.objects.aggregate(
        total_views=Sum("visualizacoes"),
        total_downloads=Sum("downloads_curriculo"),
    )
    extra["kpi_views"] = agregado.get("total_views") or 0
    extra["kpi_downloads"] = agregado.get("total_downloads") or 0
    extra["kpi_recados"] = Recado.objects.count()
    extra["kpi_respostas"] = Recado.objects.exclude(resposta="").count()
    extra["kpi_pendentes"] = Recado.objects.filter(resposta="").count()
    extra["kpi_projetos"] = Projeto.objects.filter(visivel=True).count()
    return _original_index(request, extra_context=extra)


admin.site.index = _custom_admin_index


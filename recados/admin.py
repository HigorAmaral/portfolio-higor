import csv
from django.contrib import admin
from django.db.models import Sum
from django.http import HttpResponse

from .models import (
    ConfiguracaoPerfil,
    Conquista,
    Experiencia,
    Habilidade,
    LinkContato,
    MetricaAcesso,
    Projeto,
    Recado,
)

admin.site.site_header = "Painel do portfólio · Higor Fritz"
admin.site.site_title = "Painel do portfólio"
admin.site.index_title = "Visão Geral, Métricas & Gestão de Conteúdo"


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
    search_fields = ("titulo", "descricao", "tecnologias")


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "categoria",
        "status",
        "badge",
        "tem_estudo_caso",
        "ordem",
        "visivel",
    )
    list_editable = ("categoria", "status", "ordem", "visivel")
    list_filter = ("categoria", "status", "visivel")
    search_fields = ("nome", "descricao", "tecnologias", "estudo_titulo", "estudo_desafio")
    actions = [
        "mover_para_backend",
        "mover_para_frontend",
        "mover_para_ia",
        "marcar_concluido",
        "duplicar_projeto",
    ]
    fieldsets = (
        (
            "Informações Básicas",
            {
                "fields": ("nome", "categoria", "status", "descricao", "tecnologias", "ordem", "visivel"),
                "description": "Escolha em 'Categoria' em qual aba do portfólio o projeto deve ficar (Back-end, Front-end ou IA & Inovação).",
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
            },
        ),
    )

    @admin.display(boolean=True, description="Estudo de Caso?")
    def tem_estudo_caso(self, obj):
        return bool(obj.estudo_titulo or obj.estudo_desafio or obj.estudo_solucao)

    @admin.action(description="Mover selecionados para a aba: Back-end")
    def mover_para_backend(self, request, queryset):
        qtd = queryset.update(categoria=Projeto.Categoria.BACKEND)
        self.message_user(request, f"{qtd} projeto(s) movido(s) para Back-end.")

    @admin.action(description="Mover selecionados para a aba: Front-end")
    def mover_para_frontend(self, request, queryset):
        qtd = queryset.update(categoria=Projeto.Categoria.FRONTEND)
        self.message_user(request, f"{qtd} projeto(s) movido(s) para Front-end.")

    @admin.action(description="Mover selecionados para a aba: IA & Inovação")
    def mover_para_ia(self, request, queryset):
        qtd = queryset.update(categoria=Projeto.Categoria.IA)
        self.message_user(request, f"{qtd} projeto(s) movido(s) para IA & Inovação.")

    @admin.action(description="Marcar projetos selecionados como Concluído")
    def marcar_concluido(self, request, queryset):
        qtd = queryset.update(status=Projeto.Status.CONCLUIDO)
        self.message_user(request, f"{qtd} projeto(s) marcado(s) como Concluído.")

    @admin.action(description="Duplicar projeto(s) selecionado(s) como rascunho oculto")
    def duplicar_projeto(self, request, queryset):
        criados = 0
        for p in queryset:
            p.pk = None
            p.id = None
            p.nome = f"{p.nome[:68]} (Cópia)"
            p.visivel = False
            p.ordem = p.ordem + 1
            p.save()
            criados += 1
        self.message_user(request, f"{criados} cópia(s) criada(s) como rascunho oculto.")


@admin.register(Experiencia)
class ExperienciaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "periodo", "ordem", "visivel")
    list_editable = ("ordem", "visivel")
    search_fields = ("titulo", "periodo", "descricao")
    list_filter = ("visivel",)


@admin.register(Conquista)
class ConquistaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "selo", "link_url", "ordem", "visivel")
    list_editable = ("ordem", "visivel")
    search_fields = ("titulo", "selo", "descricao")
    list_filter = ("visivel",)


@admin.register(ConfiguracaoPerfil)
class ConfiguracaoPerfilAdmin(admin.ModelAdmin):
    list_display = ("tag_disponibilidade", "localizacao", "atualizado_em")
    readonly_fields = ("atualizado_em",)


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


# Injeção de KPIs, Gráfico de Evolução e Resumo no dashboard inicial do Django Admin
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
    extra["kpi_cat_backend"] = Projeto.objects.filter(visivel=True, categoria="backend").count()
    extra["kpi_cat_frontend"] = Projeto.objects.filter(visivel=True, categoria="frontend").count()
    extra["kpi_cat_ia"] = Projeto.objects.filter(visivel=True, categoria="ia").count()

    # Histórico recente (últimos 7 registros diários) para o gráfico de barras no Admin
    recentes = list(MetricaAcesso.objects.order_by("-data")[:7])[::-1]
    max_val = max([m.visualizacoes for m in recentes] + [1])
    extra["kpi_chart_days"] = [
        {
            "data_curta": m.data.strftime("%d/%m"),
            "views": m.visualizacoes,
            "downloads": m.downloads_curriculo,
            "pct_views": max(8, int((m.visualizacoes / max_val) * 100)) if m.visualizacoes else 4,
            "pct_downloads": max(8, int((m.downloads_curriculo / max_val) * 100)) if m.downloads_curriculo else 0,
        }
        for m in recentes
    ]
    extra["ultimos_recados"] = list(Recado.objects.order_by("-criado_em")[:4])
    return _original_index(request, extra_context=extra)


admin.site.index = _custom_admin_index

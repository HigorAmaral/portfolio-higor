"""Handlers de erro personalizados.

- Rotas do site recebem páginas HTML estilizadas (templates/4xx.html e 500.html).
- Rotas da API (/api/...) e o /healthz/ recebem JSON, para não quebrar clientes que esperam JSON.
"""
import logging

from django.http import HttpResponse, JsonResponse
from django.template import loader

logger = logging.getLogger(__name__)

MENSAGENS = {
    400: "Requisição inválida.",
    403: "Acesso negado.",
    404: "Recurso não encontrado.",
    429: "Muitas requisições. Tente novamente mais tarde.",
    500: "Erro interno do servidor.",
}


def _eh_api(request):
    caminho = getattr(request, "path", "") or ""
    return caminho.startswith("/api/") or caminho.startswith("/healthz")


def _renderizar(request, status, contexto=None):
    if request is not None and _eh_api(request):
        return JsonResponse({"erro": MENSAGENS.get(status, "Erro."), "status": status}, status=status)
    try:
        # Sem passar "request": o template não depende de context processors (robusto até no erro 500)
        html = loader.get_template(f"{status}.html").render(contexto or {})
    except Exception:
        logger.exception("Falha ao renderizar página de erro %s", status)
        html = f"<h1>{status}</h1><p>{MENSAGENS.get(status, 'Erro.')}</p>"
    return HttpResponse(html, status=status, content_type="text/html; charset=utf-8")


def erro_400(request, exception=None):
    return _renderizar(request, 400)


def erro_403(request, exception=None):
    return _renderizar(request, 403)


def erro_404(request, exception=None):
    return _renderizar(request, 404, {"caminho": request.path})


def erro_500(request):
    return _renderizar(request, 500)


def erro_csrf(request, reason=""):
    """Falha de CSRF (ex.: sessão expirada no formulário do admin)."""
    return _renderizar(request, 403)


def resposta_429(request, mensagem=None):
    return _renderizar(request, 429, {"mensagem": mensagem} if mensagem else None)

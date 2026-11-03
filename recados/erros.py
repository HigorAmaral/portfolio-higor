"""Handlers de erro personalizados.

- Rotas do site recebem páginas HTML estilizadas (templates/4xx.html, 500.html e bloqueado.html).
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


def _renderizar(request, status, contexto=None, template_nome=None):
    if request is not None and _eh_api(request):
        msg = (contexto or {}).get("mensagem") or MENSAGENS.get(status, "Erro.")
        return JsonResponse({"erro": msg, "status": status}, status=status)
    arq_template = template_nome or f"{status}.html"
    try:
        # Sem passar "request": o template não depende de context processors (robusto até no erro 500)
        html = loader.get_template(arq_template).render(contexto or {})
    except Exception:
        logger.exception("Falha ao renderizar página de erro %s", arq_template)
        msg_fallback = (contexto or {}).get("mensagem") or MENSAGENS.get(status, "Erro.")
        html = f"<h1>{status}</h1><p>{msg_fallback}</p>"
    resp = HttpResponse(html, status=status, content_type="text/html; charset=utf-8")
    resp["Cache-Control"] = "no-store"
    return resp


def erro_400(request, exception=None):
    return _renderizar(request, 400)


def erro_403(request, exception=None):
    return _renderizar(request, 403)


def erro_404(request, exception=None):
    caminho = getattr(request, "path", "/") if request is not None else "/"
    return _renderizar(request, 404, {"caminho": caminho})


def erro_500(request):
    return _renderizar(request, 500)


def erro_csrf(request, reason=""):
    """Falha de CSRF (ex.: sessão expirada no formulário do admin)."""
    return _renderizar(request, 403)


def resposta_429(request, mensagem=None):
    return _renderizar(request, 429, {"mensagem": mensagem} if mensagem else None)


def resposta_bloqueado(request, mensagem=None):
    """Renderiza a página estilizada de 'Acesso temporariamente bloqueado' (HTTP 403)."""
    caminho = getattr(request, "path", "/") if request is not None else "/"
    contexto = {
        "caminho": caminho,
        "mensagem": mensagem
        or "Acesso temporariamente bloqueado. Por medida preventiva de segurança, aguarde alguns minutos antes de tentar novamente.",
    }
    return _renderizar(request, 403, contexto, template_nome="bloqueado.html")

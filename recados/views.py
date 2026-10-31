import json
import logging
import re
import time
from pathlib import Path

from config.seguranca import ip_cliente
from django.conf import settings
from django.core.cache import cache
from django.db import connection
from django.db.models import F
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.html import escape, strip_tags
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods

from .models import Habilidade, MetricaAcesso, Projeto, Recado
from .notificacoes import notificar_novo_recado
from .openapi import OPENAPI_SPEC

FRONTEND = Path(settings.BASE_DIR) / "frontend" / "index.html"
INTERVALO_SEGUNDOS = 30  # tempo mínimo entre dois recados do mesmo IP
MAX_BODY_SIZE = 10 * 1024  # 10 KB limite para evitar DoS por payload excessivo
JANELA_METRICA_SEGUNDOS = 30 * 60  # cada IP conta no máximo 1 visita/download a cada 30 min
CAMINHOS_METRICA = {"/"}  # whitelist: impede criação ilimitada de linhas com caminhos arbitrários

logger = logging.getLogger(__name__)

# Remove caracteres de controle ASCII que não sejam quebras de linha normais
REGEX_CONTROLE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def index(request):
    """Entrega o front-end (frontend/index.html)."""
    if not FRONTEND.exists():
        raise Http404("frontend/index.html não encontrado")
    return FileResponse(open(FRONTEND, "rb"), content_type="text/html; charset=utf-8")


@require_GET
def manifest(request):
    """Web App Manifest do PWA (servido na raiz para escopo '/')."""
    caminho = FRONTEND.parent / "manifest.webmanifest"
    resp = FileResponse(open(caminho, "rb"), content_type="application/manifest+json")
    resp["Cache-Control"] = "public, max-age=3600"
    return resp


@require_GET
def service_worker(request):
    """Service Worker do PWA. Precisa estar na raiz para controlar todo o site."""
    caminho = FRONTEND.parent / "sw.js"
    resp = FileResponse(open(caminho, "rb"), content_type="application/javascript; charset=utf-8")
    # Sem cache HTTP: o navegador sempre verifica se há versão nova do SW
    resp["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp["Service-Worker-Allowed"] = "/"
    return resp


def _ip(request):
    """Obtém o IP real do cliente de forma resistente a spoofing (ver config/seguranca.py)."""
    return ip_cliente(request)


def _limpar_texto(texto):
    """Sanitiza string contra XSS e injeções."""
    if not texto:
        return ""
    limpo = strip_tags(str(texto))
    limpo = REGEX_CONTROLE.sub("", limpo)
    return escape(limpo.strip())


@require_GET
def healthz(request):
    """Endpoint de Health Check para monitoramento e keep-alive."""
    inicio = time.monotonic()
    db_status = "connected"
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Exception:
        # Detalhes vão só para o log do servidor; nunca expor erros internos publicamente
        logger.exception("Health check: falha no banco de dados")
        db_status = "unhealthy"

    cache_status = "operational"
    try:
        cache.set("_healthz_ping", "ok", 10)
        if cache.get("_healthz_ping") != "ok":
            cache_status = "degraded"
    except Exception:
        logger.exception("Health check: falha no cache")
        cache_status = "unhealthy"

    duracao_ms = round((time.monotonic() - inicio) * 1000, 2)
    saudavel = db_status == "connected"

    return JsonResponse(
        {
            "status": "healthy" if saudavel else "unhealthy",
            "database": db_status,
            "cache": cache_status,
            "tempo_resposta_ms": duracao_ms,
            "timestamp": timezone.now().isoformat(),
            "versao": "1.0.0",
        },
        status=200 if saudavel else 503,
    )


@require_GET
def api_docs(request):
    """Página de documentação interativa Swagger UI."""
    return render(request, "docs.html")


@require_GET
def api_schema(request):
    """Especificação OpenAPI 3.0 em formato JSON."""
    return JsonResponse(OPENAPI_SPEC)


@csrf_exempt
@require_http_methods(["POST"])
def visitas(request):
    """Registra métricas anônimas e agregadas de visitas e downloads de currículo."""
    if len(request.body) > 2048:
        return JsonResponse({"erro": "Payload muito grande."}, status=413)

    try:
        dados = json.loads(request.body.decode("utf-8", errors="replace") or "{}")
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({"erro": "JSON inválido."}, status=400)
    if not isinstance(dados, dict):
        return JsonResponse({"erro": "Formato de dados inválido."}, status=400)

    tipo = str(dados.get("tipo") or "pagina").strip()
    caminho = str(dados.get("caminho") or "/").strip()[:100]

    if tipo not in ("pagina", "download_curriculo"):
        return JsonResponse({"erro": "Tipo de métrica inválido."}, status=400)

    # Caminhos fora da whitelist são agrupados em "/" (evita inchaço do banco por spam)
    if caminho not in CAMINHOS_METRICA:
        caminho = "/"

    # Anti-inflação: cada IP conta no máximo uma vez por janela (o IP NÃO é salvo, só usado em memória)
    chave = f"metrica-{tipo}-{ip_cliente(request)}"
    if not cache.add(chave, 1, JANELA_METRICA_SEGUNDOS):
        return JsonResponse({"ok": True})

    hoje = timezone.now().date()
    metrica, _ = MetricaAcesso.objects.get_or_create(data=hoje, caminho=caminho)

    if tipo == "download_curriculo":
        MetricaAcesso.objects.filter(id=metrica.id).update(downloads_curriculo=F("downloads_curriculo") + 1)
    else:
        MetricaAcesso.objects.filter(id=metrica.id).update(visualizacoes=F("visualizacoes") + 1)

    return JsonResponse({"ok": True})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def recados(request):
    if request.method == "GET":
        itens = Recado.objects.filter(visivel=True)[:30]
        return JsonResponse(
            [{"nome": r.nome, "texto": r.texto, "criado_em": r.criado_em.isoformat()} for r in itens],
            safe=False,
        )

    # Proteção contra DoS via payload gigante
    if len(request.body) > MAX_BODY_SIZE:
        return JsonResponse({"erro": "Requisição excede o tamanho permitido."}, status=413)

    try:
        dados = json.loads(request.body.decode("utf-8", errors="replace") or "{}")
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({"erro": "Dados inválidos."}, status=400)
    if not isinstance(dados, dict):
        return JsonResponse({"erro": "Formato de dados inválido."}, status=400)

    # Armadilha honeypot para robôs/spammers
    if dados.get("site"):
        return JsonResponse({"ok": True}, status=201)

    # Sanitização estrita contra XSS
    nome_bruto = str(dados.get("nome") or "").strip()[:40] or "Anônimo"
    texto_bruto = str(dados.get("texto") or "").strip()

    if not texto_bruto:
        return JsonResponse({"erro": "Escreva uma mensagem."}, status=400)
    if len(texto_bruto) > 280:
        return JsonResponse({"erro": "O recado pode ter no máximo 280 caracteres."}, status=400)

    nome = _limpar_texto(nome_bruto)[:40] or "Anônimo"
    texto = _limpar_texto(texto_bruto)[:280]

    # Rate limiting por IP
    chave = f"recado-ip-{_ip(request)}"
    if not cache.add(chave, 1, INTERVALO_SEGUNDOS):
        return JsonResponse({"erro": "Espere um pouco antes de enviar outro recado."}, status=429)

    Recado.objects.create(nome=nome, texto=texto)
    notificar_novo_recado(nome, texto)

    return JsonResponse({"ok": True}, status=201)


@require_GET
def conteudo(request):
    """Habilidades e projetos exibidos no site (editados em /admin)."""
    habilidades = [
        {"titulo": h.titulo, "descricao": h.descricao, "tecnologias": h.lista_tecnologias()}
        for h in Habilidade.objects.filter(visivel=True)
    ]
    projetos = [
        {
            "nome": p.nome,
            "descricao": p.descricao,
            "tecnologias": p.lista_tecnologias(),
            "github": p.github,
            "demo": getattr(p, "demo", ""),
            "status": p.status,
            "status_label": p.get_status_display(),
        }
        for p in Projeto.objects.filter(visivel=True)
    ]
    return JsonResponse({"habilidades": habilidades, "projetos": projetos})

import json
import re
from pathlib import Path

from django.conf import settings
from django.core.cache import cache
from django.http import FileResponse, Http404, JsonResponse
from django.utils.html import escape, strip_tags
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods

from .models import Habilidade, Projeto, Recado

FRONTEND = Path(settings.BASE_DIR) / "frontend" / "index.html"
INTERVALO_SEGUNDOS = 30  # tempo mínimo entre dois recados do mesmo IP
MAX_BODY_SIZE = 10 * 1024  # 10 KB limite para evitar DoS por payload excessivo

# Remove caracteres de controle ASCII que não sejam quebras de linha normais
REGEX_CONTROLE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def index(request):
    """Entrega o front-end (frontend/index.html)."""
    if not FRONTEND.exists():
        raise Http404("frontend/index.html não encontrado")
    return FileResponse(open(FRONTEND, "rb"), content_type="text/html; charset=utf-8")


def _ip(request):
    """Obtém o IP real do cliente com segurança através de proxy confiável."""
    if settings.BEHIND_PROXY:
        encaminhado = request.META.get("HTTP_X_FORWARDED_FOR", "")
        if encaminhado:
            # Pega apenas o primeiro IP da cadeia (cliente original)
            return encaminhado.split(",")[0].strip()[:45]
    ip = request.META.get("REMOTE_ADDR", "?")
    return ip.strip()[:45]


def _limpar_texto(texto):
    """Sanitiza string contra XSS e injeções."""
    if not texto:
        return ""
    # Remove tags HTML e caracteres de controle perigosos
    limpo = strip_tags(str(texto))
    limpo = REGEX_CONTROLE.sub("", limpo)
    return escape(limpo.strip())


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

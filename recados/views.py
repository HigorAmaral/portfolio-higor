import json
from pathlib import Path

from django.conf import settings
from django.core.cache import cache
from django.http import FileResponse, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods

from .models import Habilidade, Projeto, Recado

FRONTEND = Path(settings.BASE_DIR) / "frontend" / "index.html"
INTERVALO_SEGUNDOS = 30  # tempo minimo entre dois recados do mesmo IP


def index(request):
    """Entrega o front-end (frontend/index.html)."""
    if not FRONTEND.exists():
        raise Http404("frontend/index.html nao encontrado")
    return FileResponse(open(FRONTEND, "rb"), content_type="text/html; charset=utf-8")


def _ip(request):
    if settings.BEHIND_PROXY:
        encaminhado = request.META.get("HTTP_X_FORWARDED_FOR", "")
        if encaminhado:
            return encaminhado.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "?")


# csrf_exempt: API publica sem login, so recebe JSON; o limite por IP e o campo
# "site" (armadilha para robos) protegem contra abuso.
@csrf_exempt
@require_http_methods(["GET", "POST"])
def recados(request):
    if request.method == "GET":
        itens = Recado.objects.filter(visivel=True)[:30]
        return JsonResponse(
            [{"nome": r.nome, "texto": r.texto, "criado_em": r.criado_em.isoformat()} for r in itens],
            safe=False,
        )

    try:
        dados = json.loads(request.body or b"{}")
    except ValueError:
        return JsonResponse({"erro": "Dados inválidos."}, status=400)
    if not isinstance(dados, dict):
        return JsonResponse({"erro": "Dados inválidos."}, status=400)

    # Armadilha para robos: o campo "site" fica escondido e deve vir vazio.
    if dados.get("site"):
        return JsonResponse({"ok": True}, status=201)

    nome = str(dados.get("nome") or "").strip()[:40] or "Anônimo"
    texto = str(dados.get("texto") or "").strip()
    if not texto:
        return JsonResponse({"erro": "Escreva uma mensagem."}, status=400)
    if len(texto) > 280:
        return JsonResponse({"erro": "O recado pode ter no máximo 280 caracteres."}, status=400)

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
            "status": p.status,
            "status_label": p.get_status_display(),
        }
        for p in Projeto.objects.filter(visivel=True)
    ]
    return JsonResponse({"habilidades": habilidades, "projetos": projetos})

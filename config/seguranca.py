"""Utilitários de segurança compartilhados (IP real do cliente atrás de proxy)."""
import ipaddress

from django.conf import settings

# Cabeçalhos definidos pela borda do Render/Cloudflare. A Cloudflare SOBRESCREVE esses valores,
# então o cliente não consegue falsificá-los (diferente do primeiro item do X-Forwarded-For).
CABECALHOS_IP_CONFIAVEIS = ("HTTP_TRUE_CLIENT_IP", "HTTP_CF_CONNECTING_IP")


def _ip_valido(valor):
    try:
        return str(ipaddress.ip_address(valor.strip()))
    except (ValueError, AttributeError):
        return None


def ip_cliente(request):
    """Retorna o IP real do visitante de forma resistente a spoofing."""
    if getattr(settings, "BEHIND_PROXY", False):
        for cabecalho in CABECALHOS_IP_CONFIAVEIS:
            ip = _ip_valido(request.META.get(cabecalho, ""))
            if ip:
                return ip
    return _ip_valido(request.META.get("REMOTE_ADDR", "")) or "desconhecido"

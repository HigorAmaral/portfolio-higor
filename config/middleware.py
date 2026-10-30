from django.core.cache import cache
from django.http import HttpResponse

from .seguranca import ip_cliente


class SecurityHeadersMiddleware:
    """Adiciona cabeçalhos de segurança HTTP modernos a todas as respostas."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Content-Security-Policy (CSP)
        # Permite scripts e estilos locais seguros e bloqueia injeções de terceiros e iframes não autorizados
        if "Content-Security-Policy" not in response:
            response["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self' data:; "
                "connect-src 'self'; "
                "object-src 'none'; "
                "frame-ancestors 'none'; "
                "form-action 'self'; "
                "base-uri 'self';"
            )

        # Permissions-Policy: bloqueia acesso a recursos sensíveis do dispositivo
        if "Permissions-Policy" not in response:
            response["Permissions-Policy"] = (
                "accelerometer=(), camera=(), geolocation=(), "
                "gyroscope=(), magnetometer=(), microphone=(), "
                "payment=(), usb=(), interest-cohort=()"
            )

        # Previne MIME-type sniffing e clickjacking
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "DENY"
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response["Cross-Origin-Opener-Policy"] = "same-origin"
        response["Cross-Origin-Resource-Policy"] = "same-origin"

        # Respostas do painel admin e da API nunca devem ser cacheadas por proxies
        caminho = request.path
        if caminho.startswith("/api/recados") or getattr(request, "_eh_admin", False):
            response["Cache-Control"] = "no-store"

        return response


class AdminBruteForceMiddleware:
    """Bloqueia tentativas de força bruta no login do Django Admin.

    Após MAX_TENTATIVAS logins falhos do mesmo IP, bloqueia novas tentativas por JANELA_SEGUNDOS.
    """

    MAX_TENTATIVAS = 5
    JANELA_SEGUNDOS = 15 * 60

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from django.urls import reverse

        try:
            url_login = reverse("admin:login")
        except Exception:
            url_login = None

        admin_raiz = url_login.rsplit("login/", 1)[0] if url_login else None
        if admin_raiz and request.path.startswith(admin_raiz):
            request._eh_admin = True

        if not url_login or request.path != url_login or request.method != "POST":
            return self.get_response(request)

        chave = f"admin-login-falhas-{ip_cliente(request)}"
        if (cache.get(chave) or 0) >= self.MAX_TENTATIVAS:
            return HttpResponse(
                "Muitas tentativas de login. Tente novamente em 15 minutos.",
                status=429,
                content_type="text/plain; charset=utf-8",
            )

        response = self.get_response(request)

        if response.status_code == 302:
            # Login bem-sucedido: zera o contador
            cache.delete(chave)
        else:
            # Login falhou (o Django re-renderiza o formulário com 200)
            if not cache.add(chave, 1, self.JANELA_SEGUNDOS):
                try:
                    cache.incr(chave)
                except ValueError:
                    cache.set(chave, 1, self.JANELA_SEGUNDOS)

        return response

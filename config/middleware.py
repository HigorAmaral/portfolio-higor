import logging
import os
import re

from django.core.cache import cache
from django.http import HttpResponse

from .seguranca import ip_cliente

logger = logging.getLogger("django.security")


class SecurityHeadersMiddleware:
    """Adiciona cabeçalhos de segurança HTTP modernos a todas as respostas."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Content-Security-Policy (CSP)
        # Sem 'unsafe-inline' em script-src: mesmo que alguém consiga injetar HTML, o navegador
        # se recusa a executar qualquer <script> ou JavaScript que não venha de arquivo do próprio site.
        if "Content-Security-Policy" not in response:
            response["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self'; "
                "script-src-attr 'none'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https://github.com https://avatars.githubusercontent.com; "
                "font-src 'self' data:; "
                "connect-src 'self'; "
                "worker-src 'self'; "
                "manifest-src 'self'; "
                "object-src 'none'; "
                "frame-src 'none'; "
                "frame-ancestors 'none'; "
                "form-action 'self'; "
                "base-uri 'self'; "
                "upgrade-insecure-requests;"
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
            from recados.erros import resposta_429

            return resposta_429(
                request,
                "Foram feitas muitas tentativas de login. Por segurança, aguarde 15 minutos antes de tentar novamente.",
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


class BloqueioScannerMiddleware:
    """Bloqueia robôs que varrem o site procurando falhas (/.env, /wp-admin, /phpmyadmin...).

    - Rotas típicas de exploração e ferramentas de ataque conhecidas recebem 404 seco (sem
      renderizar template nem tocar no banco) e somam "strikes" para o IP.
    - Ao atingir MAX_STRIKES, o IP fica banido temporariamente e recebe 403 em tudo.
    - O IP é usado só em memória (cache) e nunca é gravado no banco (LGPD).
    """

    MAX_STRIKES = 3
    JANELA_STRIKES = 10 * 60
    TEMPO_BANIMENTO = 60 * 60
    MAX_TAMANHO_URL = 2048

    ROTAS_SUSPEITAS = re.compile(
        r"(^|/)(\.env|\.git|\.svn|\.hg|\.aws|\.ssh|\.docker|\.vscode|\.idea|\.htaccess|\.htpasswd|\.ds_store)"
        r"|wp-(admin|login|content|includes|config|json)|xmlrpc\.php|phpmyadmin|pma/|myadmin|adminer"
        r"|\.(php\d?|asp|aspx|jsp|cgi|pl|sh|bak|old|orig|swp|sql|sqlite3?|db|ini|log|conf|yml|yaml|tar|gz|zip|rar|7z)$"
        r"|cgi-bin|/etc/passwd|/proc/self|boaform|hnap1|/actuator|server-status|/console|/vendor/phpunit"
        r"|/telescope|/_ignition|/solr/|/jenkins|/manager/html|/owa/|/remote/login|/autodiscover"
        r"|\.\./|\.\.\\|%2e%2e|%252e|%00",
        re.IGNORECASE,
    )

    AGENTES_ATAQUE = re.compile(
        r"sqlmap|nikto|nmap|masscan|zgrab|nuclei|wpscan|dirbuster|gobuster|dirb/|ffuf|feroxbuster"
        r"|acunetix|nessus|openvas|netsparker|qualys|w3af|arachni|hydra|jaeles|whatweb|commix|xsstrike",
        re.IGNORECASE,
    )

    METODOS_PERMITIDOS = {"GET", "HEAD", "POST", "OPTIONS"}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = ip_cliente(request)
        chave_ban = f"scanner-ban-{ip}"

        if cache.get(chave_ban):
            return self._resposta(403, "Acesso temporariamente bloqueado.")

        if request.method not in self.METODOS_PERMITIDOS:
            return self._resposta(405, "Método não permitido.")

        caminho_completo = request.get_full_path()
        if len(caminho_completo) > self.MAX_TAMANHO_URL:
            return self._resposta(414, "URL muito longa.")

        agente = request.META.get("HTTP_USER_AGENT", "")
        caminho = request.path

        if self.AGENTES_ATAQUE.search(agente) or self._rota_suspeita(caminho, caminho_completo):
            self._registrar_strike(ip, chave_ban)
            return self._resposta(404, "Não encontrado.")

        return self.get_response(request)

    def _rota_suspeita(self, caminho, caminho_completo):
        # Arquivos estáticos legítimos (ex.: .gz pré-comprimidos do WhiteNoise) nunca são suspeitos
        if caminho.startswith("/static/") and ".." not in caminho_completo and "%2e" not in caminho_completo.lower():
            return False
        if self.ROTAS_SUSPEITAS.search(caminho_completo):
            return True
        # Tentativa de achar o painel na URL padrão quando ele foi movido para uma URL secreta
        admin_slug = os.environ.get("ADMIN_URL", "admin").strip("/") or "admin"
        return admin_slug != "admin" and (caminho == "/admin" or caminho.startswith("/admin/"))

    def _registrar_strike(self, ip, chave_ban):
        chave = f"scanner-strikes-{ip}"
        if cache.add(chave, 1, self.JANELA_STRIKES):
            total = 1
        else:
            try:
                total = cache.incr(chave)
            except ValueError:
                cache.set(chave, 1, self.JANELA_STRIKES)
                total = 1
        if total >= self.MAX_STRIKES:
            cache.set(chave_ban, 1, self.TEMPO_BANIMENTO)
            logger.warning("Scanner bloqueado temporariamente após %s tentativas suspeitas", total)

    @staticmethod
    def _resposta(status, mensagem):
        resp = HttpResponse(mensagem, status=status, content_type="text/plain; charset=utf-8")
        resp["Cache-Control"] = "no-store"
        return resp

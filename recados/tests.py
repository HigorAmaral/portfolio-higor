import json
import os
from unittest.mock import patch

from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from .models import MetricaAcesso, Recado
from .notificacoes import notificar_novo_recado


class SecurityAndRecadosTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        cache.clear()

    def test_security_headers_present(self):
        """Verifica se os cabeçalhos de segurança essenciais estão presentes nas respostas."""
        response = self.client.get(reverse("index"), secure=True)
        self.assertEqual(response.status_code, 200)

        # CSP, Clickjacking, Sniffing e Permissions
        self.assertIn("Content-Security-Policy", response.headers)
        self.assertIn("default-src 'self'", response.headers["Content-Security-Policy"])
        self.assertEqual(response.headers.get("X-Frame-Options"), "DENY")
        self.assertEqual(response.headers.get("X-Content-Type-Options"), "nosniff")
        self.assertIn("Permissions-Policy", response.headers)
        self.assertEqual(response.headers.get("Referrer-Policy"), "strict-origin-when-cross-origin")

    def test_xss_sanitization(self):
        """Verifica se injeções de script HTML (XSS) são limpas e escapadas antes de salvar."""
        payload = {
            "nome": "<script>alert('hacker')</script>Higor",
            "texto": "<img src=x onerror=alert(1)>Olá mundo seguro!",
            "site": "",
        }
        response = self.client.post(
            reverse("recados"),
            data=json.dumps(payload),
            content_type="application/json",
            secure=True,
        )
        self.assertEqual(response.status_code, 201)

        recado = Recado.objects.first()
        self.assertIsNotNone(recado)
        self.assertNotIn("<script>", recado.nome)
        self.assertNotIn("<img", recado.texto)
        self.assertIn("Olá mundo seguro!", recado.texto)

    def test_dos_large_payload_blocked(self):
        """Verifica se payloads gigantes com tentativa de DoS são bloqueados."""
        payload = {"nome": "Teste", "texto": "A" * 15000}
        response = self.client.post(
            reverse("recados"),
            data=json.dumps(payload),
            content_type="application/json",
            secure=True,
        )
        self.assertEqual(response.status_code, 413)
        self.assertEqual(Recado.objects.count(), 0)

    def test_honeypot_bot_defense(self):
        """Verifica se bots que preenchem o campo 'site' são descartados silenciosamente."""
        payload = {"nome": "Bot", "texto": "Spam link", "site": "http://spam.com"}
        response = self.client.post(
            reverse("recados"),
            data=json.dumps(payload),
            content_type="application/json",
            secure=True,
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Recado.objects.count(), 0)

    def test_conteudo_endpoint_safe(self):
        """Verifica se a rota de conteúdo retorna estrutura esperada."""
        response = self.client.get(reverse("conteudo"), secure=True)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("habilidades", data)
        self.assertIn("projetos", data)

    def test_healthz_endpoint_healthy(self):
        """Verifica se o health check reporta status saudável com banco e cache operacionais."""
        response = self.client.get(reverse("healthz"), secure=True)
        self.assertEqual(response.status_code, 200)
        dados = response.json()
        self.assertEqual(dados.get("status"), "healthy")
        self.assertEqual(dados.get("database"), "connected")
        self.assertEqual(dados.get("cache"), "operational")
        self.assertIn("tempo_resposta_ms", dados)
        self.assertIn("timestamp", dados)

    def test_api_docs_and_schema_endpoints(self):
        """Verifica se a documentação Swagger UI e o schema OpenAPI 3.0 estão operacionais."""
        # Swagger UI HTML
        res_docs = self.client.get(reverse("api_docs"), secure=True)
        self.assertEqual(res_docs.status_code, 200)
        self.assertIn("vendor/swagger-ui/swagger-ui-bundle.js", res_docs.content.decode("utf-8"))

        # OpenAPI 3.0 JSON
        res_schema = self.client.get(reverse("api_schema"), secure=True)
        self.assertEqual(res_schema.status_code, 200)
        schema = res_schema.json()
        self.assertEqual(schema.get("openapi"), "3.0.3")
        self.assertIn("/healthz/", schema.get("paths", {}))
        self.assertIn("/api/recados/", schema.get("paths", {}))
        self.assertIn("/api/visitas/", schema.get("paths", {}))

    def test_metrica_visitas_e_download_curriculo(self):
        """Verifica se métricas agregadas sem cookies (LGPD) são computadas corretamente."""
        # Visualização de página
        res1 = self.client.post(
            reverse("visitas"),
            data=json.dumps({"tipo": "pagina", "caminho": "/"}),
            content_type="application/json",
            secure=True,
        )
        self.assertEqual(res1.status_code, 200)

        # Download do currículo
        res2 = self.client.post(
            reverse("visitas"),
            data=json.dumps({"tipo": "download_curriculo", "caminho": "/"}),
            content_type="application/json",
            secure=True,
        )
        self.assertEqual(res2.status_code, 200)

        # Checa no banco de dados
        metrica = MetricaAcesso.objects.first()
        self.assertIsNotNone(metrica)
        self.assertEqual(metrica.caminho, "/")
        self.assertEqual(metrica.visualizacoes, 1)
        self.assertEqual(metrica.downloads_curriculo, 1)

    def test_visitas_validation_errors(self):
        """Verifica validações do endpoint de métricas contra tipos inválidos e payload gigante."""
        # Tipo inválido
        res = self.client.post(
            reverse("visitas"),
            data=json.dumps({"tipo": "tipo_inexistente"}),
            content_type="application/json",
            secure=True,
        )
        self.assertEqual(res.status_code, 400)

        # Payload gigante (> 2KB)
        res_grande = self.client.post(
            reverse("visitas"),
            data=json.dumps({"tipo": "pagina", "caminho": "x" * 3000}),
            content_type="application/json",
            secure=True,
        )
        self.assertEqual(res_grande.status_code, 413)

    @patch("recados.notificacoes.urllib.request.urlopen")
    def test_webhook_notifier_execution(self, mock_urlopen):
        """Testa o disparo de webhook para Discord e Telegram sem travar execução."""
        mock_resp = mock_urlopen.return_value.__enter__.return_value
        mock_resp.status = 204
        with patch.dict(os.environ, {"DISCORD_WEBHOOK_URL": "https://discord.com/api/webhooks/mock"}):
            notificar_novo_recado("Testador", "Mensagem de teste")
            self.assertTrue(mock_urlopen.called)

    def test_webhook_silent_failure_on_network_error(self):
        """Testa que falhas de rede em webhooks não causam erro na requisição do usuário."""
        with patch.dict(os.environ, {"DISCORD_WEBHOOK_URL": "http://127.0.0.1:1/invalid"}):
            payload = {"nome": "Visitante", "texto": "Recado com webhook falhando"}
            res = self.client.post(
                reverse("recados"),
                data=json.dumps(payload),
                content_type="application/json",
                secure=True,
            )
            # Usuário recebe 201 com sucesso mesmo com webhook inacessível
            self.assertEqual(res.status_code, 201)
            self.assertEqual(Recado.objects.filter(nome="Visitante").count(), 1)


class HardeningTestCase(TestCase):
    """Testes das proteções adicionais (spoofing de IP, força bruta, vazamento de erros, spam de métricas)."""

    def setUp(self):
        self.client = Client()
        cache.clear()

    def _post_recado(self, **extra):
        return self.client.post(
            reverse("recados"),
            data=json.dumps({"nome": "A", "texto": "Oi"}),
            content_type="application/json",
            secure=True,
            **extra,
        )

    def test_rate_limit_nao_burlavel_com_x_forwarded_for(self):
        """Trocar o X-Forwarded-For (falsificável) não pode burlar o limite de recados."""
        r1 = self._post_recado(HTTP_X_FORWARDED_FOR="1.1.1.1")
        r2 = self._post_recado(HTTP_X_FORWARDED_FOR="2.2.2.2")
        self.assertEqual(r1.status_code, 201)
        self.assertEqual(r2.status_code, 429)

    def test_rate_limit_usa_true_client_ip(self):
        """IPs reais diferentes (definidos pela borda Cloudflare/Render) têm limites independentes."""
        r1 = self._post_recado(HTTP_TRUE_CLIENT_IP="1.1.1.1")
        r2 = self._post_recado(HTTP_TRUE_CLIENT_IP="2.2.2.2")
        self.assertEqual(r1.status_code, 201)
        self.assertEqual(r2.status_code, 201)

    def test_admin_login_bloqueia_forca_bruta(self):
        """Após 5 logins falhos, o IP é bloqueado com 429."""
        url = reverse("admin:login")
        for _ in range(5):
            r = self.client.post(url, {"username": "admin", "password": "errada"}, secure=True)
            self.assertEqual(r.status_code, 200)
        r = self.client.post(url, {"username": "admin", "password": "errada"}, secure=True)
        self.assertEqual(r.status_code, 429)

    def test_metricas_nao_inflaveis_e_caminho_whitelist(self):
        """Mesmo IP não infla contadores e caminhos arbitrários não criam novas linhas no banco."""
        for caminho in ["/", "/x1", "/x2", "/x3"]:
            self.client.post(
                reverse("visitas"),
                data=json.dumps({"tipo": "pagina", "caminho": caminho}),
                content_type="application/json",
                secure=True,
            )
        self.assertEqual(MetricaAcesso.objects.count(), 1)
        self.assertEqual(MetricaAcesso.objects.first().visualizacoes, 1)

    def test_visitas_rejeita_json_nao_objeto(self):
        r = self.client.post(reverse("visitas"), data="[1,2]", content_type="application/json", secure=True)
        self.assertEqual(r.status_code, 400)

    def test_healthz_nao_vaza_erro_interno(self):
        """Falhas no banco não podem expor mensagens internas publicamente."""
        with patch("recados.views.connection.cursor", side_effect=Exception("senha=segredo host=db")):
            r = self.client.get(reverse("healthz"), secure=True)
        self.assertEqual(r.status_code, 503)
        self.assertNotIn("segredo", r.content.decode())

    def test_docs_sem_cdn_externo(self):
        """A documentação deve usar apenas assets locais (CSP 'self')."""
        r = self.client.get(reverse("api_docs"), secure=True)
        conteudo = r.content.decode()
        self.assertNotIn("cdn.jsdelivr.net", conteudo)
        self.assertNotIn("cdn.jsdelivr.net", r.headers["Content-Security-Policy"])

    @patch("recados.notificacoes.urllib.request.urlopen")
    def test_discord_bloqueia_mencoes(self, mock_urlopen):
        """Visitantes não podem usar @everyone para spammar o Discord."""
        mock_urlopen.return_value.__enter__.return_value.status = 204
        with patch.dict(os.environ, {"DISCORD_WEBHOOK_URL": "https://discord.com/api/webhooks/mock"}):
            notificar_novo_recado("x", "@everyone spam")
        corpo = json.loads(mock_urlopen.call_args[0][0].data)
        self.assertEqual(corpo["allowed_mentions"], {"parse": []})

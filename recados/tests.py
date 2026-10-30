import json
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from .models import Recado


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

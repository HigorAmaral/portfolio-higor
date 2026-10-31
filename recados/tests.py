import json
import os
from unittest.mock import patch

from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from .models import LinkContato, MetricaAcesso, Projeto, Recado
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


    def test_custom_error_404_html_and_json(self):
        """Verifica se páginas 404 retornam HTML personalizado para o site e JSON para a API."""
        # 404 no site
        r_site = self.client.get("/rota-inexistente-12345", secure=True)
        self.assertEqual(r_site.status_code, 404)
        self.assertIn("Essa página se perdeu no código", r_site.content.decode("utf-8"))
        self.assertIn("404", r_site.content.decode("utf-8"))

        # 404 na API
        r_api = self.client.get("/api/rota-inexistente-xyz", secure=True)
        self.assertEqual(r_api.status_code, 404)
        dados = r_api.json()
        self.assertEqual(dados.get("status"), 404)
        self.assertIn("erro", dados)

    def test_custom_error_handlers_render(self):
        """Testa a renderização direta dos handlers 500, 403, 400 e 429."""
        from recados.erros import erro_400, erro_403, erro_500, resposta_429
        from django.test import RequestFactory

        rf = RequestFactory()

        # 500
        req500 = rf.get("/erro500")
        res500 = erro_500(req500)
        self.assertEqual(res500.status_code, 500)
        self.assertIn("Ops! Algo quebrou por aqui", res500.content.decode("utf-8"))

        # 403
        req403 = rf.get("/erro403")
        res403 = erro_403(req403)
        self.assertEqual(res403.status_code, 403)
        self.assertIn("Área restrita", res403.content.decode("utf-8"))

        # 400
        req400 = rf.get("/erro400")
        res400 = erro_400(req400)
        self.assertEqual(res400.status_code, 400)
        self.assertIn("Não consegui entender o pedido", res400.content.decode("utf-8"))

        # 429
        req429 = rf.get("/erro429")
        res429 = resposta_429(req429)
        self.assertEqual(res429.status_code, 429)
        self.assertIn("Calma, respira um pouco", res429.content.decode("utf-8"))


class PWATestCase(TestCase):
    def test_manifest_valido(self):
        """O manifest é servido na raiz, com tipo correto e ícones obrigatórios."""
        resp = self.client.get("/manifest.webmanifest", secure=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("application/manifest+json", resp["Content-Type"])
        dados = json.loads(b"".join(resp.streaming_content))
        self.assertEqual(dados["display"], "standalone")
        self.assertEqual(dados["scope"], "/")
        tamanhos = {i["sizes"] for i in dados["icons"]}
        self.assertTrue({"192x192", "512x512"} <= tamanhos)

    def test_service_worker_servido_na_raiz(self):
        """O SW fica em /sw.js, sem cache HTTP e com escopo liberado para '/'."""
        resp = self.client.get("/sw.js", secure=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("javascript", resp["Content-Type"])
        self.assertEqual(resp["Service-Worker-Allowed"], "/")
        self.assertIn("no-cache", resp["Cache-Control"])
        self.assertIn("worker-src 'self'", resp["Content-Security-Policy"])

    def test_service_worker_nao_aceita_post(self):
        self.assertEqual(self.client.post("/sw.js", secure=True).status_code, 405)


class MelhoriasPortfolioTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        cache.clear()

    def test_recado_resposta_auto_timestamp_and_api(self):
        """Verifica se resposta do autor no Recado preenche timestamp e é retornada na API."""
        r = Recado.objects.create(nome="Recrutador", texto="Gostei muito do seu portfólio!")
        self.assertEqual(r.resposta, "")
        self.assertIsNone(r.respondido_em)

        # Higor responde pelo painel
        r.resposta = "Muito obrigado pelo feedback! Fico à disposição."
        r.save()
        r.refresh_from_db()
        self.assertIsNotNone(r.respondido_em)

        # GET /api/recados/ deve serializar resposta e data de resposta
        resp = self.client.get(reverse("recados"), secure=True)
        self.assertEqual(resp.status_code, 200)
        dados = resp.json()
        item = next((x for x in dados if x["nome"] == "Recrutador"), None)
        self.assertIsNotNone(item)
        self.assertEqual(item["resposta"], "Muito obrigado pelo feedback! Fico à disposição.")
        self.assertIsNotNone(item["respondido_em"])

    def test_projeto_estudo_caso_and_conteudo_api(self):
        """Verifica se badge, pdf e estudo de caso estruturado são retornados na API de conteúdo."""
        p = Projeto.objects.create(
            nome="Projeto Teste",
            descricao="Descrição de teste",
            tecnologias="Python, Django",
            badge="🏆 Teste Destaque",
            pdf="/static/teste.pdf",
            estudo_titulo="Estudo de Caso Teste",
            estudo_desafio="Desafio de alta escala",
            estudo_solucao="Arquitetura em microsserviços",
            estudo_aprendizados="Alta disponibilidade",
            visivel=True,
        )
        dados_ec = p.dados_estudo_caso()
        self.assertIsNotNone(dados_ec)
        self.assertEqual(dados_ec["titulo"], "Estudo de Caso Teste")
        self.assertEqual(dados_ec["badge"], "🏆 Teste Destaque")
        self.assertEqual(dados_ec["desafio"], "Desafio de alta escala")

        resp = self.client.get(reverse("conteudo"), secure=True)
        self.assertEqual(resp.status_code, 200)
        projetos = resp.json().get("projetos", [])
        proj = next((x for x in projetos if x["nome"] == "Projeto Teste"), None)
        self.assertIsNotNone(proj)
        self.assertEqual(proj["badge"], "🏆 Teste Destaque")
        self.assertEqual(proj["pdf"], "/static/teste.pdf")
        self.assertEqual(proj["estudo_caso"]["solucao"], "Arquitetura em microsserviços")

    def test_admin_kpi_dashboard_context(self):
        """Verifica se os KPIs de métricas e conteúdo são injetados no contexto do Django Admin."""
        from django.contrib.admin import site
        from django.test import RequestFactory
        from django.contrib.auth.models import User

        rf = RequestFactory()
        req = rf.get("/admin/")
        req.user = User.objects.create_superuser("admin_test", "admin@test.com", "senha123")

        extra = {}
        # Chama a função customizada do admin
        resp = site.index(req, extra_context=extra)
        # O context_data do template response contém os KPIs
        ctx = resp.context_data
        self.assertIn("kpi_views", ctx)
        self.assertIn("kpi_downloads", ctx)
        self.assertIn("kpi_recados", ctx)
        self.assertIn("kpi_respostas", ctx)
        self.assertIn("kpi_projetos", ctx)

    def test_link_contato_in_conteudo_api(self):
        """Verifica se links de contato cadastrados são expostos na rota de conteúdo."""
        LinkContato.objects.create(
            chave="outro",
            titulo="Blog Técnico",
            url="https://medium.com/@higor",
            ordem=10,
            visivel=True,
        )
        resp = self.client.get(reverse("conteudo"), secure=True)
        self.assertEqual(resp.status_code, 200)
        dados = resp.json()
        self.assertIn("links", dados)
        item = next((x for x in dados["links"] if x["chave"] == "outro"), None)
        self.assertIsNotNone(item)
        self.assertEqual(item["titulo"], "Blog Técnico")
        self.assertEqual(item["url"], "https://medium.com/@higor")

    def test_admin_recado_filter_and_actions(self):
        """Verifica o filtro de recados pendentes/respondidos e as ações de visibilidade."""
        from django.contrib.admin import site
        from .admin import RecadoAdmin, RespondidoListFilter

        r1 = Recado.objects.create(nome="Visitante 1", texto="Olá", resposta="", visivel=True)
        r2 = Recado.objects.create(nome="Visitante 2", texto="Oi", resposta="Tudo bem!", visivel=True)

        admin_instance = RecadoAdmin(Recado, site)

        # Ação marcar oculto
        from django.test import RequestFactory
        from django.contrib.auth.models import User
        from unittest.mock import MagicMock
        rf = RequestFactory()
        req = rf.get("/admin/recados/recado/")
        req.user = User.objects.create_superuser("admin_act", "adm@test.com", "pass123")
        setattr(req, "_messages", MagicMock())

        admin_instance.marcar_oculto(req, Recado.objects.filter(id=r1.id))
        r1.refresh_from_db()
        self.assertFalse(r1.visivel)

        admin_instance.marcar_visivel(req, Recado.objects.filter(id=r1.id))
        r1.refresh_from_db()
        self.assertTrue(r1.visivel)

    def test_admin_metricas_exportar_csv(self):
        """Verifica a exportação de métricas agregadas para CSV."""
        from django.contrib.admin import site
        from .admin import MetricaAcessoAdmin
        from django.test import RequestFactory
        from django.contrib.auth.models import User

        MetricaAcesso.objects.create(caminho="/", visualizacoes=15, downloads_curriculo=3)

        admin_instance = MetricaAcessoAdmin(MetricaAcesso, site)
        rf = RequestFactory()
        req = rf.get("/admin/recados/metricaacesso/")
        req.user = User.objects.create_superuser("admin_csv", "csv@test.com", "pass123")

        resp = admin_instance.exportar_csv(req, MetricaAcesso.objects.all())
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp["Content-Type"], "text/csv; charset=utf-8")
        self.assertIn("attachment; filename=", resp["Content-Disposition"])
        content_text = resp.content.decode("utf-8")
        self.assertIn("Data,Caminho,Visualizações,Downloads de Currículo", content_text)
        self.assertIn("/", content_text)


class ProtecoesAvancadasTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        cache.clear()

    def test_bloqueio_scanner_rotas_sensiveis(self):
        """Varreduras em rotas como /.env, /wp-login.php recebem 404 seco e acumulam strikes."""
        for rota in ["/.env", "/wp-login.php", "/.git/config", "/phpmyadmin", "/wp-admin/"]:
            cache.clear()
            resp = self.client.get(rota, secure=True)
            self.assertEqual(resp.status_code, 404)
            self.assertEqual(resp["Content-Type"], "text/plain; charset=utf-8")

    def test_bloqueio_scanner_ferramentas_ataque(self):
        """User-Agents de scanners como sqlmap e nikto recebem 404 seco imediatamente."""
        resp = self.client.get("/", HTTP_USER_AGENT="sqlmap/1.5#stable", secure=True)
        self.assertEqual(resp.status_code, 404)

    def test_bloqueio_scanner_banimento_apos_strikes(self):
        """Após 3 strikes de varredura maliciosa do mesmo IP, o IP é banido com 403."""
        ip = "198.51.100.42"
        # 3 requisições suspeitas
        for _ in range(3):
            self.client.get("/.env", HTTP_TRUE_CLIENT_IP=ip, secure=True)

        # 4ª requisição (mesmo para rota legítima "/") é banida
        resp = self.client.get("/", HTTP_TRUE_CLIENT_IP=ip, secure=True)
        self.assertEqual(resp.status_code, 403)
        self.assertIn("Acesso temporariamente bloqueado", resp.content.decode("utf-8"))

    def test_metodos_http_nao_permitidos_bloqueados(self):
        """Métodos HTTP não autorizados (ex: DELETE na raiz) recebem 405 imediato."""
        resp = self.client.delete("/", secure=True)
        self.assertEqual(resp.status_code, 405)

    def test_recado_rejeita_links_phishing(self):
        """Tentativas de injetar links no mural são bloqueadas com 400."""
        payload = {"nome": "Spammer", "texto": "Visite meu site https://spam-malicioso.com e ganhe dinheiro"}
        resp = self.client.post(
            reverse("recados"),
            data=json.dumps(payload),
            content_type="application/json",
            secure=True,
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("links não são permitidos", resp.json().get("erro", ""))

    def test_recado_rejeita_sql_injection_residual(self):
        """Tentativas de injeção SQL no texto são rejeitadas."""
        payload = {"nome": "Atacante", "texto": "Meu recado ' OR 1=1 --"}
        resp = self.client.post(
            reverse("recados"),
            data=json.dumps(payload),
            content_type="application/json",
            secure=True,
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("comandos ou expressões", resp.json().get("erro", ""))

    def test_recado_rejeita_nome_reservado(self):
        """Impedir que visitantes se passem pelo administrador/autor do site."""
        payload = {"nome": "Higor Amaral", "texto": "Mensagem fingindo ser o autor"}
        resp = self.client.post(
            reverse("recados"),
            data=json.dumps(payload),
            content_type="application/json",
            secure=True,
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("nome é reservado", resp.json().get("erro", ""))

    def test_recado_rejeita_duplicata_mesmo_ip(self):
        """O mesmo IP não pode reenviar o mesmo recado repetido em curto intervalo."""
        payload = {"nome": "Visitante", "texto": "Mensagem bacana e original!"}
        r1 = self.client.post(
            reverse("recados"),
            data=json.dumps(payload),
            content_type="application/json",
            HTTP_TRUE_CLIENT_IP="203.0.113.10",
            secure=True,
        )
        self.assertEqual(r1.status_code, 201)

        # Imediatamente o mesmo IP tenta mandar a mesma mensagem
        # (limpa apenas o rate limit de 30s para testar a camada de duplicata)
        cache.delete("recado-ip-203.0.113.10")
        r2 = self.client.post(
            reverse("recados"),
            data=json.dumps(payload),
            content_type="application/json",
            HTTP_TRUE_CLIENT_IP="203.0.113.10",
            secure=True,
        )
        self.assertEqual(r2.status_code, 409)
        self.assertIn("já foi enviado recentemente", r2.json().get("erro", ""))

    def test_csp_sem_unsafe_inline_em_scripts(self):
        """O CSP estrito não deve conter 'unsafe-inline' em script-src."""
        resp = self.client.get(reverse("index"), secure=True)
        csp = resp.headers.get("Content-Security-Policy", "")
        self.assertIn("script-src 'self'", csp)
        self.assertNotIn("script-src 'self' 'unsafe-inline'", csp)
        self.assertIn("script-src-attr 'none'", csp)
        self.assertIn("object-src 'none'", csp)

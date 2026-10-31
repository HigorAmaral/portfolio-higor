from django.db import migrations


def popular_estudos(apps, schema_editor):
    Projeto = apps.get_model("recados", "Projeto")

    dados = {
        "Hackathon": {
            "badge": "🏆 Hackathon 24H · IA Aplicada",
            "pdf": "",
            "estudo_titulo": "Hackathon Fábrica 2k26 (Maratona 24H)",
            "estudo_desafio": (
                "Criar uma solução tecnológica completa em apenas 24 horas contínuas para apoiar professores "
                "da rede pública a adaptar atividades e avaliações para crianças neuroatípicas de 6 a 9 anos "
                "(com TEA e TDAH), além de estruturar relatórios de observação em sala de aula."
            ),
            "estudo_solucao": (
                "Desenvolvemos em equipe uma aplicação web em Python e Django integrada com modelos de "
                "Inteligência Artificial. A ferramenta analisa o plano de aula do professor e gera versões "
                "adaptadas com linguagem direta, suporte imagético, redução de sobrecarga sensorial e "
                "roteiros lúdicos diferenciados. Deploy efetuado no ambiente da Fábrica de Software do IFC."
            ),
            "estudo_aprendizados": (
                "Trabalho ágil sob altíssima pressão de tempo, prototipagem relâmpago, integração de IA "
                "no backend Django e entrega de um produto funcional pronto para uso em sala de aula em 24 horas."
            ),
        },
        "Portfólio": {
            "badge": "⚡ Django 6 · PostgreSQL · Swagger",
            "pdf": "",
            "estudo_titulo": "Portfólio & Backend Production-Ready",
            "estudo_desafio": (
                "Construir uma aplicação web rápida, moderna e de custo zero de infraestrutura (Render Free Tier), "
                "porém com arquitetura, testes e padrões de segurança de nível sênior."
            ),
            "estudo_solucao": (
                "Estruturação de backend Django com PostgreSQL na nuvem, esteira de CI/CD no GitHub Actions "
                "com 24 testes unitários automatizados, documentação interativa Swagger (/api/docs/), "
                "rate limiting por IP confiável (True-Client-IP), proteção estrita de headers (CSP, HSTS, COOP), "
                "auditoria de CVEs com pip-audit e bot keep-alive para zero downtime."
            ),
            "estudo_aprendizados": (
                "Implementação prática de esteira de integração contínua (CI/CD), arquitetura resiliente na nuvem, "
                "hardening contra ataques cibernéticos e documentação padronizada OpenAPI 3.0."
            ),
        },
        "Santory": {
            "badge": "🍕 Vue 3 · Django REST · Vercel · Render · Projeto Integrador",
            "pdf": "",
            "estudo_titulo": "Sistema Integrado de Gestão & PDV (Pizzaria Santory)",
            "estudo_desafio": (
                "A Pizzaria Santory operava com fluxos semi-manuais e anotações em papel para pedidos de balcão e telefone, "
                "causando lentidão no atendimento, erros na transmissão dos pedidos à cozinha, falta de controle de "
                "estoque de ingredientes e ausência de rastreamento de entregas ou pagamentos online."
            ),
            "estudo_solucao": (
                "Desenvolvimento de um ecossistema web integrado com arquitetura desacoplada: interface SPA reativa em "
                "Vue 3 (Vite) na Vercel e backend RESTful com Django no Render. Modelagem relacional completa (DER), "
                "controle automático de estoque com baixa por insumo, PDV em tempo real para salão/cozinha, perfis de "
                "acesso (Administrador, Atendente, Pizzaiolo, Entregador e Cliente) e catálogo interativo com personalização de pedidos."
            ),
            "estudo_aprendizados": (
                "Arquitetura cliente-servidor desacoplada (Vue 3 + Django API), engenharia de requisitos com 37 RFs e 20 regras "
                "de negócio, modelagem de banco de dados relacional (DER), trabalho em equipe com Git/GitHub e deploy em "
                "múltiplos provedores em nuvem (Vercel e Render)."
            ),
        },
        "BSI": {
            "badge": "🔬 BPMN · Modelo PEMM · 5W2H · Engenharia de Requisitos · LaTeX",
            "pdf": "/static/projeto-bsi-microprocessos.pdf",
            "estudo_titulo": "Mapeamento & Análise de Microprocessos (BSI IFC)",
            "estudo_desafio": (
                "A dispersão de plataformas (SIGAA, SEI, Google Forms) e o trâmite manual nos registros discentes do IFC "
                "geravam retrabalho na secretaria acadêmica, falta de rastreabilidade de solicitações para os alunos e "
                "diagnóstico de maturidade inicial (P0 em indicadores e infraestrutura de TI)."
            ),
            "estudo_solucao": (
                "Estruturação qualitativa da trajetória discente em 4 fases (Entrada, Rotina, Pedidos Especiais e Conclusão), "
                "modelagem formal de 4 fluxos em BPMN (matrículas, TCC, dispensas, regime disciplinar), aplicação do "
                "modelo de maturidade PEMM de Michael Hammer, plano de ação 5W2H e levantamento rigoroso de 8 Requisitos "
                "Funcionais (RF01-RF08) e 4 Não-Funcionais (RNF01-RNF04) com proteção de dados e acessibilidade."
            ),
            "estudo_aprendizados": (
                "Domínio prático de Gestão de Processos de Negócio (BPM/BPMN), Engenharia de Requisitos aplicada ao "
                "contexto educacional público federal, diagnóstico organizacional e redação científica técnica avançada com diagramação em LaTeX."
            ),
        },
    }

    for chave, valores in dados.items():
        projeto = Projeto.objects.filter(nome__icontains=chave).first()
        if projeto:
            for campo, val in valores.items():
                setattr(projeto, campo, val)
            projeto.save()


class Migration(migrations.Migration):

    dependencies = [
        ("recados", "0010_projeto_badge_projeto_estudo_aprendizados_and_more"),
    ]

    operations = [
        migrations.RunPython(popular_estudos, migrations.RunPython.noop),
    ]

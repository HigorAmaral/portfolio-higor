from django.db import migrations


NOVOS_PROJETOS = [
    {
        "nome": "AURA Assistant — Assistente Pessoal de IA",
        "categoria": "ia",
        "badge": "IA & Automação · Em Desenvolvimento",
        "descricao": (
            "Assistente pessoal de IA em Python com painel web, HUD flutuante, "
            "automação de sistema, acesso remoto e atualização automática via GitHub."
        ),
        "tecnologias": "Python, IA / LLMs, Automação, HTML5, CSS3, JavaScript",
        "github": "https://github.com/HigorAmaral/aura-assistant",
        "demo": "",
        "status": "em_andamento",
        "ordem": 9,
    },
    {
        "nome": "Gestão Empresa — Sistema ERP",
        "categoria": "backend",
        "badge": "Full Stack · ERP Empresarial",
        "descricao": (
            "Sistema completo de gerenciamento empresarial (ERP) com Next.js, Prisma "
            "e SQLite, reunindo Ordens de Serviço, módulo financeiro, controle de "
            "estoque e trilha de auditoria."
        ),
        "tecnologias": "TypeScript, Next.js, Prisma, SQLite, Vercel",
        "github": "https://github.com/HigorAmaral/gestao-empresa",
        "demo": "https://gestao-empresa-one.vercel.app",
        "status": "concluido",
        "ordem": 10,
    },
    {
        "nome": "SWOT Kahoot — Dinâmica Interativa",
        "categoria": "frontend",
        "badge": "Gamificação · Análise SWOT",
        "descricao": (
            "Sistema estilo Kahoot desenvolvido em TypeScript para dinâmicas de sala "
            "de aula sobre Análise SWOT e Funções Administrativas em TI."
        ),
        "tecnologias": "TypeScript, React, Next.js, Gamificação, Vercel",
        "github": "https://github.com/HigorAmaral/swot-kahoot",
        "demo": "https://swot-kahoot.vercel.app",
        "status": "concluido",
        "ordem": 11,
    },
]


def adicionar_projetos(apps, schema_editor):
    Projeto = apps.get_model("recados", "Projeto")
    for dados in NOVOS_PROJETOS:
        Projeto.objects.get_or_create(
            github=dados["github"],
            defaults={**dados, "visivel": True},
        )


def remover_projetos(apps, schema_editor):
    Projeto = apps.get_model("recados", "Projeto")
    Projeto.objects.filter(github__in=[p["github"] for p in NOVOS_PROJETOS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("recados", "0018_experiencia_conquista_configuracaoperfil"),
    ]

    operations = [
        migrations.RunPython(adicionar_projetos, remover_projetos),
    ]

from django.db import migrations


def atualizar_projetos(apps, schema_editor):
    Projeto = apps.get_model("recados", "Projeto")

    # Atualiza o Hackathon Fábrica 2k26 com o link de demonstração real e destaque de 24h
    Projeto.objects.filter(nome__icontains="Hackathon").update(
        nome="Hackathon Fábrica 2k26",
        descricao="Plataforma com Inteligência Artificial desenvolvida em uma maratona intensiva de 24 horas para auxiliar professores na adaptação personalizada de atividades pedagógicas e percepção precoce de sinais em alunos neuroatípicos (TEA e TDAH).",
        tecnologias="Python, Django, IA, Educação Inclusiva, Hackathon 24h",
        demo="https://delta.fabricadesoftware.ifc.edu.br/login?redirect=/turmas",
        github="https://github.com/Hackathon-Fabrica-2k26",
        status="concluido",
        ordem=0,
    )

    # Garante que o projeto do próprio Portfólio exista no banco de dados para ser servido pela API
    portfolio, _ = Projeto.objects.get_or_create(
        nome="Portfólio Pessoal & API REST",
        defaults={
            "descricao": "Arquitetura web completa com mural interativo, documentação OpenAPI 3.0 (Swagger UI), endpoint de health check, segurança robusta contra XSS/DoS, esteira de CI/CD no GitHub Actions e banco PostgreSQL no Render.",
            "tecnologias": "Python, Django, PostgreSQL, Swagger UI, CI/CD, Render",
            "github": "https://github.com/HigorAmaral/portfolio-higor",
            "demo": "https://portfolio-higor.onrender.com",
            "status": "concluido",
            "ordem": 1,
            "visivel": True,
        },
    )
    portfolio.demo = "https://portfolio-higor.onrender.com"
    portfolio.github = "https://github.com/HigorAmaral/portfolio-higor"
    portfolio.save()


def reverter(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [("recados", "0005_metricaacesso")]
    operations = [migrations.RunPython(atualizar_projetos, reverter)]

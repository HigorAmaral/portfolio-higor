from django.db import migrations, models


def popular_categorias_iniciais(apps, schema_editor):
    Projeto = apps.get_model("recados", "Projeto")
    mapa_categorias = {
        "Hackathon Fábrica 2k26": "ia",
        "Projeto BSI: Microprocessos Acadêmicos": "ia",
        "Portfólio Pessoal & API REST": "backend",
        "API RESTful Livraria & Gestão de Acervo": "backend",
        "Santory Pizzaria": "frontend",
        "EcoApack — Catálogo Industrial & Orçamentos B2B": "frontend",
        "Primeiro Lar Imobiliária": "frontend",
        "AgroNovo-Mundo — E-commerce Agro & Pet": "frontend",
    }
    for proj in Projeto.objects.all():
        cat = mapa_categorias.get(proj.nome)
        if not cat:
            nome_low = (proj.nome or "").lower()
            if "hackathon" in nome_low or "bsi" in nome_low or "microprocessos" in nome_low:
                cat = "ia"
            elif "portf" in nome_low or "livraria" in nome_low or "api" in nome_low:
                cat = "backend"
            else:
                cat = "frontend"
        proj.categoria = cat
        proj.save(update_fields=["categoria"])


class Migration(migrations.Migration):

    dependencies = [
        ("recados", "0015_adicionar_novos_projetos"),
    ]

    operations = [
        migrations.AddField(
            model_name="projeto",
            name="categoria",
            field=models.CharField(
                choices=[
                    ("backend", "Back-end"),
                    ("frontend", "Front-end"),
                    ("ia", "IA & Inovação"),
                ],
                default="backend",
                help_text="Define em qual aba de filtro o projeto fica no portfólio (Back-end, Front-end ou IA & Inovação).",
                max_length=20,
                verbose_name="Categoria (aba no site)",
            ),
        ),
        migrations.RunPython(popular_categorias_iniciais, migrations.RunPython.noop),
    ]

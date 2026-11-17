from django.db import migrations


NOMES_OCULTAR = [
    "Santory Pizzaria",
    "EcoApack — Catálogo Industrial & Orçamentos B2B",
    "Primeiro Lar Imobiliária",
]


def ocultar_projetos(apps, schema_editor):
    Projeto = apps.get_model("recados", "Projeto")
    Projeto.objects.filter(nome__in=NOMES_OCULTAR).update(visivel=False)


def reexibir_projetos(apps, schema_editor):
    Projeto = apps.get_model("recados", "Projeto")
    Projeto.objects.filter(nome__in=NOMES_OCULTAR).update(visivel=True)


class Migration(migrations.Migration):

    dependencies = [
        ("recados", "0019_adicionar_novos_projetos_2026"),
    ]

    operations = [
        migrations.RunPython(ocultar_projetos, reexibir_projetos),
    ]

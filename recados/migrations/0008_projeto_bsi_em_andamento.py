from django.db import migrations


def definir_em_andamento(apps, schema_editor):
    Projeto = apps.get_model("recados", "Projeto")
    Projeto.objects.filter(nome__icontains="BSI").update(status="em_andamento")


def reverter(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [("recados", "0007_atualizar_projeto_bsi")]
    operations = [migrations.RunPython(definir_em_andamento, reverter)]

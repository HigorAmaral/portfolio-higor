from django.db import migrations


def atualizar_projeto_bsi(apps, schema_editor):
    Projeto = apps.get_model("recados", "Projeto")
    Projeto.objects.filter(nome__icontains="BSI").update(
        nome="Projeto BSI: Microprocessos Acadêmicos",
        descricao="Mapeamento e análise aprofundada dos microprocessos acadêmicos do Bacharelado em Sistemas de Informação no IFC Câmpus Araquari com modelagem BPMN, diagnóstico de maturidade PEMM, plano 5W2H e engenharia de requisitos com conformidade LGPD.",
        tecnologias="BPMN / BPM, Engenharia de Requisitos, Modelo PEMM, Matriz 5W2H, LGPD, LaTeX",
        demo="/static/projeto-bsi-microprocessos.pdf",
        status="concluido",
    )


def reverter(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [("recados", "0006_atualizar_projetos_links")]
    operations = [migrations.RunPython(atualizar_projeto_bsi, reverter)]

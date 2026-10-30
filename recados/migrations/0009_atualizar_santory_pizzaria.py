from django.db import migrations


def atualizar_santory(apps, schema_editor):
    Projeto = apps.get_model("recados", "Projeto")
    Projeto.objects.filter(nome__icontains="Santory").update(
        descricao="Sistema integrado de gestão, PDV e delivery para pizzaria: SPA em Vue 3 (Vercel) e API Django REST (Render) com controle automático de estoque e rastreamento em tempo real.",
        tecnologias="Vue 3, Vite, Python, Django REST, Vercel, Render",
        demo="https://santoryfrontend-1.vercel.app/login",
        github="https://github.com/Santory-Pizzaria",
        status="concluido",
    )


def reverter(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [("recados", "0008_projeto_bsi_em_andamento")]
    operations = [migrations.RunPython(atualizar_santory, reverter)]

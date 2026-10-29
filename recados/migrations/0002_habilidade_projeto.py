from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("recados", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Habilidade",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("titulo", models.CharField(max_length=60)),
                ("descricao", models.CharField(blank=True, max_length=200)),
                ("tecnologias", models.CharField(blank=True, help_text="Separe por vírgula. Ex.: Python, Django", max_length=200)),
                ("ordem", models.PositiveSmallIntegerField(default=0, help_text="Menor número aparece primeiro.")),
                ("visivel", models.BooleanField(default=True)),
            ],
            options={"verbose_name": "habilidade", "verbose_name_plural": "habilidades", "ordering": ["ordem", "id"]},
        ),
        migrations.CreateModel(
            name="Projeto",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=80)),
                ("descricao", models.TextField(blank=True)),
                ("tecnologias", models.CharField(blank=True, help_text="Separe por vírgula. Ex.: React, Django", max_length=200)),
                ("github", models.URLField(blank=True, max_length=300)),
                ("status", models.CharField(choices=[("em_andamento", "Em andamento"), ("concluido", "Concluído")], default="em_andamento", max_length=20)),
                ("ordem", models.PositiveSmallIntegerField(default=0, help_text="Menor número aparece primeiro.")),
                ("visivel", models.BooleanField(default=True)),
            ],
            options={"verbose_name": "projeto", "verbose_name_plural": "projetos", "ordering": ["ordem", "id"]},
        ),
    ]

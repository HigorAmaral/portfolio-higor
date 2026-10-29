from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Recado",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=40)),
                ("texto", models.CharField(max_length=280)),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
                ("visivel", models.BooleanField(default=True)),
            ],
            options={"ordering": ["-criado_em"]},
        ),
    ]

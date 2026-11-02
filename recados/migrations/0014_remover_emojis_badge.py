import re
from django.db import migrations


def remover_emojis_badges(apps, schema_editor):
    Projeto = apps.get_model("recados", "Projeto")
    for p in Projeto.objects.all():
        if p.badge:
            p.badge = re.sub(
                r"[\U00010000-\U0010ffff\u2600-\u26ff\u2700-\u27bf]\s*",
                "",
                p.badge,
            ).strip()
            p.save(update_fields=["badge"])


class Migration(migrations.Migration):

    dependencies = [
        ("recados", "0013_popular_links_contato"),
    ]

    operations = [
        migrations.RunPython(remover_emojis_badges, migrations.RunPython.noop),
    ]

from django.db import migrations


def popular_links(apps, schema_editor):
    LinkContato = apps.get_model("recados", "LinkContato")

    links = [
        {
            "chave": "whatsapp",
            "titulo": "WhatsApp",
            "url": "https://wa.me/5547996565013?text=Ol%C3%A1%20Higor!%20Vi%20seu%20portf%C3%B3lio%20e%20gostaria%20de%20conversar%20sobre%20uma%20oportunidade.",
            "ordem": 1,
            "visivel": True,
        },
        {
            "chave": "linkedin",
            "titulo": "LinkedIn",
            "url": "https://www.linkedin.com/in/higor-do-amaral-fritz/",
            "ordem": 2,
            "visivel": True,
        },
        {
            "chave": "github",
            "titulo": "GitHub",
            "url": "https://github.com/HigorAmaral",
            "ordem": 3,
            "visivel": True,
        },
        {
            "chave": "email",
            "titulo": "E-mail",
            "url": "mailto:higordoamaralfritz@gmail.com",
            "ordem": 4,
            "visivel": True,
        },
        {
            "chave": "curriculo",
            "titulo": "Currículo (PDF)",
            "url": "/static/curriculo-higor.pdf",
            "ordem": 5,
            "visivel": True,
        },
    ]

    for item in links:
        LinkContato.objects.update_or_create(
            chave=item["chave"],
            defaults={
                "titulo": item["titulo"],
                "url": item["url"],
                "ordem": item["ordem"],
                "visivel": item["visivel"],
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ("recados", "0012_linkcontato"),
    ]

    operations = [
        migrations.RunPython(popular_links, migrations.RunPython.noop),
    ]

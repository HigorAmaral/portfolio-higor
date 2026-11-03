from django.db import migrations


def atualizar_dados(apps, schema_editor):
    LinkContato = apps.get_model("recados", "LinkContato")
    Habilidade = apps.get_model("recados", "Habilidade")

    # 1. Padronizar e-mail amarahigor@gmail.com e LinkedIn nos links de contato
    LinkContato.objects.update_or_create(
        chave="email",
        defaults={
            "titulo": "amarahigor@gmail.com",
            "url": "mailto:amarahigor@gmail.com",
            "ordem": 4,
            "visivel": True,
        },
    )
    LinkContato.objects.update_or_create(
        chave="linkedin",
        defaults={
            "titulo": "LinkedIn",
            "url": "https://www.linkedin.com/in/higor-do-amaral-fritz-727869298/",
            "ordem": 2,
            "visivel": True,
        },
    )

    # 2. Enriquecer as habilidades cadastradas no banco
    habilidades_atualizadas = [
        (
            "Front-end",
            "Front-end & Web",
            "Interfaces rápidas, responsivas, acessíveis e organizadas em componentes.",
            "JavaScript, React, Vue 3, Vite, Pinia, HTML5, CSS3",
            1,
        ),
        (
            "Back-end",
            "Back-end & APIs REST",
            "APIs RESTful documentadas, autenticação JWT, segurança e painéis administrativos.",
            "Python, Django, Django REST, Swagger / OpenAPI, JWT, Gunicorn",
            2,
        ),
        (
            "Dados",
            "Dados & DevOps",
            "Modelagem relacional, versionamento com Git/GitHub, testes e deploy em nuvem.",
            "PostgreSQL, MySQL, Git, GitHub Actions, Vercel, Render",
            3,
        ),
        (
            "Design",
            "Design & UI/UX",
            "Protótipos navegáveis no Figma, arquitetura da informação e design systems.",
            "Figma, UI/UX, Prototipagem, Design Systems, Responsividade",
            4,
        ),
        (
            "Idiomas",
            "Idiomas & Soft Skills",
            "Inglês intermediário (4 anos KNN) para documentação técnica e comunicação em equipe.",
            "Inglês (4 anos KNN), Trabalho em Equipe, BPMN, Metodologias Ágeis",
            5,
        ),
    ]

    for prefixo, novo_titulo, descricao, tecnologias, ordem in habilidades_atualizadas:
        hab = Habilidade.objects.filter(titulo__istartswith=prefixo).first()
        if hab:
            hab.titulo = novo_titulo
            hab.descricao = descricao
            hab.tecnologias = tecnologias
            hab.ordem = ordem
            hab.visivel = True
            hab.save()
        else:
            Habilidade.objects.create(
                titulo=novo_titulo,
                descricao=descricao,
                tecnologias=tecnologias,
                ordem=ordem,
                visivel=True,
            )


class Migration(migrations.Migration):

    dependencies = [
        ("recados", "0016_projeto_categoria"),
    ]

    operations = [
        migrations.RunPython(atualizar_dados, migrations.RunPython.noop),
    ]

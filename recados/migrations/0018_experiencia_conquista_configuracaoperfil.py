from django.db import migrations, models


def popular_dados_admin(apps, schema_editor):
    Experiencia = apps.get_model("recados", "Experiencia")
    Conquista = apps.get_model("recados", "Conquista")
    ConfiguracaoPerfil = apps.get_model("recados", "ConfiguracaoPerfil")

    if not ConfiguracaoPerfil.objects.exists():
        ConfiguracaoPerfil.objects.create(
            tag_disponibilidade="Disponível para estágio e novos projetos",
            localizacao="Araquari / Joinville · SC",
            subtitulo_hero=(
                "Graduando em Sistemas de Informação pelo Instituto Federal Catarinense (IFC) e Técnico em Informática. "
                "Desenvolvo aplicações web completas, APIs RESTful seguras com Python e Django, interfaces em Vue e React e soluções com IA."
            ),
        )

    experiencias_iniciais = [
        (
            "Graduação (2026 – 2029 / Em andamento)",
            "Bacharelado em Sistemas de Informação",
            "Instituto Federal Catarinense — Câmpus Araquari · Período Matutino (08:20 às 12:00)",
            1,
        ),
        (
            "Técnico Integrado (Concluído)",
            "Técnico em Informática para Internet",
            "Instituto Federal Catarinense — Câmpus Araquari",
            2,
        ),
        (
            "Experiência Prática (2022 – 2023)",
            "Jovem Aprendiz (Almoxarifado) · TAF Indústria de Plásticos Ltda.",
            "Controle, organização e conferência de insumos e matérias-primas no setor de estoque/almoxarifado. Apoio a processos logísticos internos, rotinas de registro e cumprimento de normas operacionais.",
            3,
        ),
    ]
    if not Experiencia.objects.exists():
        for periodo, titulo, descricao, ordem in experiencias_iniciais:
            Experiencia.objects.create(
                periodo=periodo,
                titulo=titulo,
                descricao=descricao,
                ordem=ordem,
                visivel=True,
            )

    conquistas_iniciais = [
        (
            "Maratona 24 Horas · Destaque",
            "Hackathon Fábrica de Software 2k26",
            "Desenvolvimento em equipe de uma plataforma com IA construída em uma maratona intensiva de 24 horas ininterruptas para auxiliar professores na adaptação personalizada de atividades e detecção precoce de sinais de autismo, TEA e TDAH em crianças de 6 a 9 anos no IFC Câmpus Araquari.",
            "https://delta.fabricadesoftware.ifc.edu.br/login?redirect=/turmas",
            "Acessar Sistema ao Vivo ↗",
            1,
        ),
        (
            "4 Anos de Formação",
            "Inglês Intermediário · KNN Idiomas",
            "Formação de 4 anos de curso com domínio para leitura técnica de documentações em inglês, escrita de código e comunicação em equipe.",
            "",
            "",
            2,
        ),
        (
            "Curso Técnico Integrado",
            "Técnico em Informática para Internet · IFC",
            "Formação técnica presencial integrada ao ensino médio com base em algoritmos, lógica de programação, HTML5/CSS3, JavaScript e bancos de dados.",
            "",
            "",
            3,
        ),
        (
            "Pesquisa Científica & BPMN",
            "Microprocessos Acadêmicos BSI",
            "Monografia e mapeamento dos microprocessos discentes do IFC com modelagem formal em BPMN, avaliação pelo modelo PEMM (Michael Hammer), diretrizes 5W2H e engenharia de requisitos com conformidade LGPD.",
            "/static/projeto-bsi-microprocessos.pdf",
            "Ver Monografia (PDF) ↗",
            4,
        ),
    ]
    if not Conquista.objects.exists():
        for selo, titulo, descricao, link_url, link_texto, ordem in conquistas_iniciais:
            Conquista.objects.create(
                selo=selo,
                titulo=titulo,
                descricao=descricao,
                link_url=link_url,
                link_texto=link_texto,
                ordem=ordem,
                visivel=True,
            )


class Migration(migrations.Migration):

    dependencies = [
        ("recados", "0017_atualizar_email_e_habilidades"),
    ]

    operations = [
        migrations.CreateModel(
            name="ConfiguracaoPerfil",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tag_disponibilidade", models.CharField(default="Disponível para estágio e novos projetos", max_length=100, verbose_name="Selo de disponibilidade (Hero)")),
                ("localizacao", models.CharField(default="Araquari / Joinville · SC", max_length=100, verbose_name="Selo de localização (Hero)")),
                ("subtitulo_hero", models.TextField(default="Graduando em Sistemas de Informação pelo Instituto Federal Catarinense (IFC) e Técnico em Informática. Desenvolvo aplicações web completas, APIs RESTful seguras com Python e Django, interfaces em Vue e React e soluções com IA.", verbose_name="Texto de apresentação (Hero)")),
                ("atualizado_em", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "configuração do perfil (Hero)",
                "verbose_name_plural": "configurações do perfil (Hero)",
            },
        ),
        migrations.CreateModel(
            name="Conquista",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("selo", models.CharField(help_text="Ex.: Maratona 24 Horas · Destaque", max_length=80, verbose_name="Selo superior")),
                ("titulo", models.CharField(help_text="Ex.: Hackathon Fábrica de Software 2k26", max_length=120, verbose_name="Título da conquista")),
                ("descricao", models.TextField(verbose_name="Descrição detalhada")),
                ("link_url", models.CharField(blank=True, help_text="Ex.: https://... ou /static/arquivo.pdf", max_length=300, verbose_name="Link externo ou PDF (opcional)")),
                ("link_texto", models.CharField(blank=True, default="Acessar Credencial ↗", max_length=80, verbose_name="Texto do botão de link")),
                ("ordem", models.PositiveSmallIntegerField(default=0, help_text="Menor número aparece primeiro.")),
                ("visivel", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "conquista / certificado",
                "verbose_name_plural": "conquistas & certificados",
                "ordering": ["ordem", "id"],
            },
        ),
        migrations.CreateModel(
            name="Experiencia",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("periodo", models.CharField(help_text="Ex.: Graduação (2026 – 2029 / Em andamento)", max_length=80, verbose_name="Período / Tipo")),
                ("titulo", models.CharField(help_text="Ex.: Bacharelado em Sistemas de Informação", max_length=120, verbose_name="Curso ou Cargo")),
                ("descricao", models.TextField(help_text="Ex.: Instituto Federal Catarinense — Câmpus Araquari", verbose_name="Instituição / Descrição")),
                ("ordem", models.PositiveSmallIntegerField(default=0, help_text="Menor número aparece primeiro.")),
                ("visivel", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "formação / experiência",
                "verbose_name_plural": "formações & experiências",
                "ordering": ["ordem", "id"],
            },
        ),
        migrations.RunPython(popular_dados_admin, migrations.RunPython.noop),
    ]

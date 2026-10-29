from django.db import migrations

HABILIDADES = [('Front-end', 'Interfaces rápidas e organizadas em componentes.', 'JavaScript, React, Vue'), ('Back-end', 'APIs, regras de negócio e painéis administrativos.', 'Python, Django'), ('Dados', 'Modelagem e consultas em banco relacional.', 'MySQL'), ('Design', 'Protótipos e telas pensadas para quem usa.', 'Figma'), ('Idiomas', 'Inglês com 4 anos de curso na KNN, para ler documentação e trabalhar com times internacionais.', 'Inglês')]
PROJETOS = [('Projeto BSI', 'Mapeamento dos microprocessos acadêmicos do IFC Câmpus Araquari, feito como trabalho do curso de Sistemas de Informação.', 'Pesquisa, Processos, LaTeX', '', 'em_andamento'), ('Hackathon Fábrica 2k26', 'Site com IA que ajuda professores a adaptar atividades e a perceber sinais em alunos de 6 a 9 anos, como autismo, TEA e TDAH. Feito no hackathon da Fábrica de Software do IFC Câmpus Araquari.', 'IA, Educação, Hackathon 2026', 'https://github.com/Hackathon-Fabrica-2k26', 'concluido'), ('Santory Pizzaria', 'Projeto desenvolvido durante o curso técnico em Informática, no Instituto Federal.', 'Curso técnico', 'https://github.com/Santory-Pizzaria', 'concluido')]


def criar(apps, schema_editor):
    Habilidade = apps.get_model("recados", "Habilidade")
    Projeto = apps.get_model("recados", "Projeto")
    if not Habilidade.objects.exists():
        for i, (titulo, descricao, tecnologias) in enumerate(HABILIDADES):
            Habilidade.objects.create(titulo=titulo, descricao=descricao, tecnologias=tecnologias, ordem=i)
    if not Projeto.objects.exists():
        for i, (nome, descricao, tecnologias, github, status) in enumerate(PROJETOS):
            Projeto.objects.create(nome=nome, descricao=descricao, tecnologias=tecnologias, github=github, status=status, ordem=i)


def desfazer(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [("recados", "0002_habilidade_projeto")]
    operations = [migrations.RunPython(criar, desfazer)]

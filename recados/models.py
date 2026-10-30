from django.db import models


class Recado(models.Model):
    nome = models.CharField(max_length=40)
    texto = models.CharField(max_length=280)
    criado_em = models.DateTimeField(auto_now_add=True)
    visivel = models.BooleanField(default=True)

    class Meta:
        ordering = ["-criado_em"]

    def __str__(self):
        return f"{self.nome}: {self.texto[:40]}"


class Habilidade(models.Model):
    titulo = models.CharField(max_length=60)
    descricao = models.CharField(max_length=200, blank=True)
    tecnologias = models.CharField(max_length=200, blank=True, help_text="Separe por vírgula. Ex.: Python, Django")
    ordem = models.PositiveSmallIntegerField(default=0, help_text="Menor número aparece primeiro.")
    visivel = models.BooleanField(default=True)

    class Meta:
        ordering = ["ordem", "id"]
        verbose_name = "habilidade"
        verbose_name_plural = "habilidades"

    def __str__(self):
        return self.titulo

    def lista_tecnologias(self):
        return [t.strip() for t in self.tecnologias.split(",") if t.strip()]


class Projeto(models.Model):
    class Status(models.TextChoices):
        EM_ANDAMENTO = "em_andamento", "Em andamento"
        CONCLUIDO = "concluido", "Concluído"

    nome = models.CharField(max_length=80)
    descricao = models.TextField(blank=True)
    tecnologias = models.CharField(max_length=200, blank=True, help_text="Separe por vírgula. Ex.: React, Django")
    github = models.URLField(max_length=300, blank=True)
    demo = models.URLField(max_length=300, blank=True, help_text="Link para o projeto rodando ao vivo (opcional).")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.EM_ANDAMENTO)
    ordem = models.PositiveSmallIntegerField(default=0, help_text="Menor número aparece primeiro.")
    visivel = models.BooleanField(default=True)

    class Meta:
        ordering = ["ordem", "id"]
        verbose_name = "projeto"
        verbose_name_plural = "projetos"

    def __str__(self):
        return self.nome

    def lista_tecnologias(self):
        return [t.strip() for t in self.tecnologias.split(",") if t.strip()]

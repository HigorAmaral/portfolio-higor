from django.db import models
from django.utils import timezone


class Recado(models.Model):
    nome = models.CharField(max_length=40)
    texto = models.CharField(max_length=280)
    criado_em = models.DateTimeField(auto_now_add=True)
    visivel = models.BooleanField(default=True)
    resposta = models.CharField(
        max_length=280,
        blank=True,
        verbose_name="Resposta do autor",
        help_text="Sua resposta pública a este recado.",
    )
    respondido_em = models.DateTimeField(null=True, blank=True, verbose_name="Respondido em")

    class Meta:
        ordering = ["-criado_em"]

    def __str__(self):
        return f"{self.nome}: {self.texto[:40]}"

    def save(self, *args, **kwargs):
        if self.resposta and not self.respondido_em:
            self.respondido_em = timezone.now()
        elif not self.resposta:
            self.respondido_em = None
        super().save(*args, **kwargs)


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
    badge = models.CharField(
        max_length=80,
        blank=True,
        verbose_name="Selo de destaque",
        help_text="Ex.: 🏆 Hackathon 24h, ⚡ API REST ao vivo",
    )
    pdf = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="Link de PDF/Monografia",
        help_text="Ex.: /static/projeto-bsi-microprocessos.pdf",
    )
    estudo_titulo = models.CharField(
        max_length=120,
        blank=True,
        verbose_name="Título do estudo de caso",
    )
    estudo_desafio = models.TextField(
        blank=True,
        verbose_name="Desafio técnico",
    )
    estudo_solucao = models.TextField(
        blank=True,
        verbose_name="Solução desenvolvida",
    )
    estudo_aprendizados = models.TextField(
        blank=True,
        verbose_name="Aprendizados e resultados",
    )
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

    def dados_estudo_caso(self):
        if not (self.estudo_titulo or self.estudo_desafio or self.estudo_solucao):
            return None
        return {
            "titulo": self.estudo_titulo or self.nome,
            "badge": self.badge or "Estudo de Caso",
            "desafio": self.estudo_desafio,
            "solucao": self.estudo_solucao,
            "aprendizados": self.estudo_aprendizados,
        }


class MetricaAcesso(models.Model):
    """Métricas anônimas e agregadas por dia e rota para respeitar a LGPD."""

    data = models.DateField(default=timezone.now, db_index=True)
    caminho = models.CharField(max_length=100, default="/", db_index=True)
    visualizacoes = models.PositiveIntegerField(default=0)
    downloads_curriculo = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "métrica de acesso"
        verbose_name_plural = "métricas de acesso"
        ordering = ["-data", "caminho"]
        unique_together = ("data", "caminho")

    def __str__(self):
        return f"{self.data} ({self.caminho}): {self.visualizacoes} views, {self.downloads_curriculo} cv downloads"


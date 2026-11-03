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

    class Categoria(models.TextChoices):
        BACKEND = "backend", "Back-end"
        FRONTEND = "frontend", "Front-end"
        IA = "ia", "IA & Inovação"

    nome = models.CharField(max_length=80)
    categoria = models.CharField(
        max_length=20,
        choices=Categoria.choices,
        default=Categoria.BACKEND,
        verbose_name="Categoria (aba no site)",
        help_text="Define em qual aba de filtro o projeto fica no portfólio (Back-end, Front-end ou IA & Inovação).",
    )
    descricao = models.TextField(blank=True)
    tecnologias = models.CharField(max_length=200, blank=True, help_text="Separe por vírgula. Ex.: React, Django")
    github = models.URLField(max_length=300, blank=True)
    demo = models.URLField(max_length=300, blank=True, help_text="Link para o projeto rodando ao vivo (opcional).")
    badge = models.CharField(
        max_length=80,
        blank=True,
        verbose_name="Selo de destaque",
        help_text="Ex.: Hackathon 24h, API REST ao vivo",
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


class LinkContato(models.Model):
    """Canais de contato e links externos gerenciáveis no admin."""

    CHAVES = (
        ("whatsapp", "WhatsApp"),
        ("linkedin", "LinkedIn"),
        ("github", "GitHub"),
        ("email", "E-mail"),
        ("curriculo", "Currículo (PDF)"),
        ("outro", "Outro Link"),
    )

    chave = models.CharField(max_length=30, choices=CHAVES, unique=True, help_text="Identificador único do canal.")
    titulo = models.CharField(max_length=60, help_text="Texto exibido (Ex.: WhatsApp, LinkedIn, GitHub)")
    url = models.CharField(max_length=300, help_text="URL completa ou mailto:")
    ordem = models.PositiveSmallIntegerField(default=0, help_text="Menor número aparece primeiro.")
    visivel = models.BooleanField(default=True)

    class Meta:
        ordering = ["ordem", "id"]
        verbose_name = "link de contato / rede social"
        verbose_name_plural = "links de contato / redes sociais"

    def __str__(self):
        return f"{self.titulo} ({self.chave})"


class Experiencia(models.Model):
    """Itens da linha do tempo de Formação & Trajetória gerenciáveis pelo Admin."""

    periodo = models.CharField(
        max_length=80,
        verbose_name="Período / Tipo",
        help_text="Ex.: Graduação (2026 – 2029 / Em andamento)",
    )
    titulo = models.CharField(
        max_length=120,
        verbose_name="Curso ou Cargo",
        help_text="Ex.: Bacharelado em Sistemas de Informação",
    )
    descricao = models.TextField(
        verbose_name="Instituição / Descrição",
        help_text="Ex.: Instituto Federal Catarinense — Câmpus Araquari",
    )
    ordem = models.PositiveSmallIntegerField(default=0, help_text="Menor número aparece primeiro.")
    visivel = models.BooleanField(default=True)

    class Meta:
        ordering = ["ordem", "id"]
        verbose_name = "formação / experiência"
        verbose_name_plural = "formações & experiências"

    def __str__(self):
        return f"{self.titulo} ({self.periodo})"


class Conquista(models.Model):
    """Cards da seção Conquistas & Reconhecimentos gerenciáveis pelo Admin."""

    selo = models.CharField(
        max_length=80,
        verbose_name="Selo superior",
        help_text="Ex.: Maratona 24 Horas · Destaque",
    )
    titulo = models.CharField(
        max_length=120,
        verbose_name="Título da conquista",
        help_text="Ex.: Hackathon Fábrica de Software 2k26",
    )
    descricao = models.TextField(verbose_name="Descrição detalhada")
    link_url = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="Link externo ou PDF (opcional)",
        help_text="Ex.: https://... ou /static/arquivo.pdf",
    )
    link_texto = models.CharField(
        max_length=80,
        blank=True,
        default="Acessar Credencial ↗",
        verbose_name="Texto do botão de link",
    )
    ordem = models.PositiveSmallIntegerField(default=0, help_text="Menor número aparece primeiro.")
    visivel = models.BooleanField(default=True)

    class Meta:
        ordering = ["ordem", "id"]
        verbose_name = "conquista / certificado"
        verbose_name_plural = "conquistas & certificados"

    def __str__(self):
        return self.titulo


class ConfiguracaoPerfil(models.Model):
    """Configurações rápidas de disponibilidade e textos de destaque do Hero."""

    tag_disponibilidade = models.CharField(
        max_length=100,
        default="Disponível para estágio e novos projetos",
        verbose_name="Selo de disponibilidade (Hero)",
    )
    localizacao = models.CharField(
        max_length=100,
        default="Araquari / Joinville · SC",
        verbose_name="Selo de localização (Hero)",
    )
    subtitulo_hero = models.TextField(
        default=(
            "Graduando em Sistemas de Informação pelo Instituto Federal Catarinense (IFC) e Técnico em Informática. "
            "Desenvolvo aplicações web completas, APIs RESTful seguras com Python e Django, interfaces em Vue e React e soluções com IA."
        ),
        verbose_name="Texto de apresentação (Hero)",
    )
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "configuração do perfil (Hero)"
        verbose_name_plural = "configurações do perfil (Hero)"

    def __str__(self):
        return f"Perfil Hero ({self.tag_disponibilidade})"

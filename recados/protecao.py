"""Validação de conteúdo enviado por visitantes ao mural de recados.

Camadas (defesa em profundidade):
1. Normalização: remove caracteres invisíveis e de controle de direção (ataque "Trojan Source").
2. Bloqueio de payloads de código: HTML/JS, template injection, SQL injection, path traversal.
3. Anti-spam/phishing: links, repetição excessiva e nomes que se passam pelo dono do site.

A saída no navegador continua sendo feita com textContent (nunca innerHTML), então mesmo que
algo passe por aqui, o navegador nunca executa o conteúdo.
"""
import re
import unicodedata

from django.utils.html import strip_tags

# Caracteres de controle ASCII (exceto \t \n \r)
_REGEX_CONTROLE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
# Zero-width, marcas de direção bidi (U+202A-202E, U+2066-2069), BOM e afins
_REGEX_INVISIVEIS = re.compile(r"[\u200b-\u200f\u202a-\u202e\u2060-\u2064\u2066-\u2069\ufeff\u00ad]")

_PADROES_CODIGO = [
    r"<\s*/?\s*[a-z!?]",  # qualquer tag HTML/XML
    r"javascript\s*:",
    r"vbscript\s*:",
    r"data\s*:\s*text/html",
    r"\bon[a-z]{3,}\s*=",  # onerror=, onload=...
    r"\{\{.*\}\}|\{%.*%\}|\$\{.*\}",  # template injection
    r"\b(union\s+(all\s+)?select|drop\s+(table|database)|insert\s+into|delete\s+from|truncate\s+table)\b",
    r"'\s*(--|#|/\*)|'\s*or\s+'?\w+'?\s*=\s*'?\w+",  # ' OR 1=1 --  /  admin'--
    r"\.\./|\.\.\\|%2e%2e|/etc/passwd|cmd\.exe|powershell",
    r"\b(eval|exec|system|document\.cookie|window\.location)\s*\(",
]
_REGEX_CODIGO = re.compile("|".join(_PADROES_CODIGO), re.IGNORECASE | re.DOTALL)

_REGEX_PROTOCOLO = re.compile(r"(https?://|ftp://|www\.)", re.IGNORECASE)
# TLD em minúsculas de propósito: evita bloquear frases como "Gostei do projeto.Com certeza"
_REGEX_DOMINIO = re.compile(
    r"\b[\w-]+\.(com|net|org|io|xyz|ru|top|info|biz|click|link|site|online|shop|br|me|ly|gg)\b(/|\s|$)"
)


def _tem_link(valor):
    return bool(_REGEX_PROTOCOLO.search(valor) or _REGEX_DOMINIO.search(valor))
_REGEX_REPETICAO = re.compile(r"(.)\1{14,}")  # mesmo caractere 15+ vezes seguidas

_NOMES_RESERVADOS = (
    "admin",
    "administrador",
    "moderador",
    "suporte",
    "higor do amaral",
    "higor amaral",
    "higor fritz",
    "resposta do higor",
)


class ConteudoInvalido(ValueError):
    """Erro com mensagem segura para devolver ao visitante."""


def normalizar(texto):
    """Remove tags, caracteres de controle e invisíveis; normaliza Unicode (NFKC)."""
    if not texto:
        return ""
    limpo = unicodedata.normalize("NFKC", str(texto))
    limpo = _REGEX_INVISIVEIS.sub("", limpo)
    limpo = _REGEX_CONTROLE.sub("", limpo)
    limpo = strip_tags(limpo)
    # Colapsa excesso de quebras de linha/espaços usados para "empurrar" o layout
    limpo = re.sub(r"\n{3,}", "\n\n", limpo)
    limpo = re.sub(r"[ \t]{3,}", "  ", limpo)
    return limpo.strip()


def validar_recado(nome_bruto, texto_bruto):
    """Valida e sanitiza o recado. Retorna (nome, texto) limpos ou lança ConteudoInvalido."""
    nome = normalizar(nome_bruto)[:40] or "Anônimo"
    texto = normalizar(texto_bruto)

    if len(texto) < 2:
        raise ConteudoInvalido("Escreva uma mensagem.")
    if len(texto) > 280:
        raise ConteudoInvalido("O recado pode ter no máximo 280 caracteres.")

    # Verifica código residual malicioso no texto limpo (ex.: SQLi, template tags, path traversal)
    if _REGEX_CODIGO.search(texto) or _REGEX_CODIGO.search(nome):
        raise ConteudoInvalido("Seu recado contém comandos ou expressões não permitidas.")

    if _tem_link(texto) or _tem_link(nome):
        raise ConteudoInvalido("Por segurança, links não são permitidos no mural.")
    if _REGEX_REPETICAO.search(texto):
        raise ConteudoInvalido("Seu recado parece spam. Tente escrever de outra forma.")

    nome_cmp = nome.casefold()
    if any(reservado in nome_cmp for reservado in _NOMES_RESERVADOS):
        raise ConteudoInvalido("Esse nome é reservado. Por favor, use outro.")

    return nome, texto

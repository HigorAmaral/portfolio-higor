import json
import logging
import os
import urllib.parse
import urllib.request

logger = logging.getLogger(__name__)


def notificar_novo_recado(nome: str, texto: str) -> None:
    """Envia notificações instantâneas para Discord ou Telegram quando um novo recado é postado.
    
    A execução é segura com timeout curto para nunca travar a resposta do usuário caso o webhook falhe.
    """
    _notificar_discord(nome, texto)
    _notificar_telegram(nome, texto)


def _notificar_discord(nome: str, texto: str) -> bool:
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL", "").strip()
    if not webhook_url:
        return False

    dados = {
        "username": "Portfólio Higor (Mural)",
        "embeds": [
            {
                "title": "🎉 Novo recado recebido no Portfólio!",
                "color": 3719160,  # #38BDF8 (Sky Blue)
                "fields": [
                    {"name": "Autor", "value": nome or "Anônimo", "inline": True},
                    {"name": "Mensagem", "value": texto, "inline": False},
                ],
                "footer": {"text": "Django Backend Notifier"},
            }
        ],
    }

    try:
        requisicao = urllib.request.Request(
            webhook_url,
            data=json.dumps(dados).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": "Portfolio-Higor/1.0"},
            method="POST",
        )
        with urllib.request.urlopen(requisicao, timeout=3) as resposta:
            return 200 <= resposta.status < 300
    except Exception as erro:
        logger.warning("Falha ao enviar webhook do Discord: %s", erro)
        return False


def _notificar_telegram(nome: str, texto: str) -> bool:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat_id:
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    mensagem = f"🎉 *Novo recado no Portfólio!*\n\n*De:* {nome or 'Anônimo'}\n*Mensagem:*\n{texto}"

    dados = {
        "chat_id": chat_id,
        "text": mensagem,
        "parse_mode": "Markdown",
    }

    try:
        requisicao = urllib.request.Request(
            url,
            data=json.dumps(dados).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": "Portfolio-Higor/1.0"},
            method="POST",
        )
        with urllib.request.urlopen(requisicao, timeout=3) as resposta:
            return 200 <= resposta.status < 300
    except Exception as erro:
        logger.warning("Falha ao enviar mensagem para Telegram: %s", erro)
        return False

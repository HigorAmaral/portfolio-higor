"""Gera a versão estática do portfólio para o GitHub Pages (modo híbrido).

O site (HTML, CSS, JS, PDFs e imagens) é publicado no GitHub Pages, que abre instantaneamente.
A API Django (mural de recados, conteúdo dinâmico, métricas e Swagger) continua no Render.

Uso:
    API_BASE=https://portfolio-higor.onrender.com SITE_BASE=/portfolio-higor python scripts/build_pages.py

Variáveis:
    API_BASE   URL pública do backend Django (sem barra no final).
    SITE_BASE  Subpasta onde o Pages publica o site ("/nome-do-repo"), ou vazio se usar domínio próprio.
    OUT_DIR    Pasta de saída (padrão: _site).
"""

import json
import os
import re
import shutil
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
API_BASE = os.environ.get("API_BASE", "https://portfolio-higor.onrender.com").rstrip("/")
# Raiz ("") por padrão para Cloudflare Pages / Netlify; no GitHub Pages o workflow passa "/portfolio-higor"
SITE_BASE = os.environ.get("SITE_BASE", "").rstrip("/")
SAIDA = RAIZ / os.environ.get("OUT_DIR", "_site")


def gerar_index():
    html = (RAIZ / "frontend" / "index.html").read_text(encoding="utf-8")

    # Aponta o JS para a API no Render e informa a subpasta do site
    html, n = re.subn(
        r'<meta name="api-base" content="[^"]*">',
        f'<meta name="api-base" content="{API_BASE}">\n<meta name="site-base" content="{SITE_BASE}">',
        html,
    )
    assert n == 1, "meta api-base não encontrada no index.html"

    # Caminhos absolutos do Django -> caminhos do Pages / da API
    html = html.replace('"/static/', f'"{SITE_BASE}/static/')
    html = html.replace('"/manifest.webmanifest"', f'"{SITE_BASE}/manifest.webmanifest"')
    html = html.replace('"/api/', f'"{API_BASE}/api/')
    return html


def gerar_manifest():
    dados = json.loads((RAIZ / "frontend" / "manifest.webmanifest").read_text(encoding="utf-8"))
    texto = json.dumps(dados, ensure_ascii=False, indent=2)
    texto = texto.replace('"/static/', f'"{SITE_BASE}/static/').replace('"/?', f'"{SITE_BASE}/?')
    dados = json.loads(texto)
    dados["id"] = dados["scope"] = f"{SITE_BASE}/"
    return json.dumps(dados, ensure_ascii=False, indent=2)


def main():
    if SAIDA.exists():
        shutil.rmtree(SAIDA)
    SAIDA.mkdir(parents=True)

    (SAIDA / "index.html").write_text(gerar_index(), encoding="utf-8")
    (SAIDA / "404.html").write_text(gerar_index(), encoding="utf-8")
    (SAIDA / "manifest.webmanifest").write_text(gerar_manifest(), encoding="utf-8")
    # O Swagger UI fica só no Render; o resto dos arquivos estáticos vai para o Pages
    shutil.copytree(RAIZ / "static", SAIDA / "static", ignore=shutil.ignore_patterns("vendor"))
    (SAIDA / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Site estático gerado em {SAIDA} (API: {API_BASE}, base: {SITE_BASE or '/'})")


if __name__ == "__main__":
    main()

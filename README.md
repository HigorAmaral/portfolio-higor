# Portfólio Pessoal & API REST — Higor do Amaral Fritz

Aplicação web full-stack desenvolvida com **Django** no back-end e interface minimalista, responsiva e acessível no front-end. O projeto reúne projetos de software, estudos de caso com métricas e arquitetura, monografia acadêmica (BSI/IFC), formação e documentação interativa de API REST.

[![Deploy no Render](https://img.shields.io/badge/Deploy-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://portfolio-higor.onrender.com)
[![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![OpenAPI](https://img.shields.io/badge/Swagger-OpenAPI_3.0-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)](https://portfolio-higor.onrender.com/api/docs/)

---

## Demonstração ao Vivo

* **Portfólio (Render):** [portfolio-higor.onrender.com](https://portfolio-higor.onrender.com)
* **Documentação da API (Swagger UI):** [portfolio-higor.onrender.com/api/docs/](https://portfolio-higor.onrender.com/api/docs/)
* **Health Check:** [portfolio-higor.onrender.com/healthz/](https://portfolio-higor.onrender.com/healthz/)

---

## Arquitetura & Tecnologias

O projeto funciona tanto servido integralmente pelo Django (Render) quanto em **modo híbrido**, com o front-end estático publicado em hospedagem de borda (**Cloudflare Pages**, **Netlify** ou **GitHub Pages**) consumindo a API Django hospedada no Render.

### Front-end
* **Design minimalista e responsivo:** HTML5 semântico, CSS modular com design tokens e JavaScript Vanilla (sem frameworks pesados), adaptado para desktop, tablet e celular.
* **Tema claro e escuro:** alternância manual com persistência em `localStorage` e respeito à preferência do sistema (`prefers-color-scheme`).
* **Projetos e estudos de caso:** filtro por categoria (`Back-end`, `Front-end`, `IA & Inovação`), busca por tecnologia/nome e modal com desafio, solução técnica, métricas de impacto e fluxo de arquitetura.
* **PWA:** manifesto web (`manifest.webmanifest`) e Service Worker (`sw.js`) quando servido pelo Django.

### Back-end & Infraestrutura
* **Linguagem & Framework:** Python 3.12+ com Django 6.
* **Banco de Dados:** PostgreSQL (produção) e SQLite (desenvolvimento local).
* **Servidor & Estáticos:** Gunicorn + WhiteNoise (compressão gzip/brotli).
* **API & Documentação:** Endpoints REST (`/api/conteudo/`, `/api/visitas/`, `/api/recados/`) documentados em OpenAPI 3.0 (Swagger UI) e protegidos por CORS configurável (`CORS_ORIGINS`).

---

## Segurança & Boas Práticas

* **Headers HTTP:** `Content-Security-Policy` (sem `unsafe-inline` em scripts), `HSTS`, `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Cross-Origin-Opener-Policy` e `Cross-Origin-Resource-Policy`.
* **Proteção contra abuso:** rate limiting por IP com suporte a proxy reverso, proteção contra força bruta no painel administrativo e sanitização de entradas.
* **Prevenção a injeções:** uso exclusivo do ORM parametrizado do Django e manipulação segura do DOM (`textContent`).
* **Privacidade (LGPD):** métricas anônimas de acesso sem armazenamento de IPs ou identificadores pessoais.

---

## Estrutura do Repositório

```text
portfolio-higor/
├── config/                  # Configurações globais, middleware de segurança, CORS e URLs
├── recados/                 # App Django: models, views REST, proteção, OpenAPI e testes
├── frontend/                # Front-end (index.html, manifest.webmanifest, sw.js)
├── static/                  # JavaScript (app.js), PDFs (currículos e monografia) e ícones PWA
├── scripts/
│   └── build_pages.py       # Gera a versão estática (_site/) para Cloudflare Pages / Netlify / GH Pages
├── .github/workflows/       # Pipelines de CI, keep-alive e deploy no GitHub Pages
├── netlify.toml             # Configuração de build para deploy no Netlify
├── render.yaml              # Infraestrutura para deploy do back-end no Render
├── manage.py
└── requirements.txt
```

---

## Como Rodar Localmente

### 1. Clonar e preparar o ambiente
```bash
git clone https://github.com/HigorAmaral/portfolio-higor.git
cd portfolio-higor

python3 -m venv venv
source venv/bin/activate        # Linux/macOS
# .\venv\Scripts\Activate.ps1   # Windows (PowerShell)

pip install -r requirements.txt
cp .env.example .env
```
*(Sem configurar `DATABASE_URL` no `.env`, o Django usa SQLite automaticamente).*

### 2. Migrações e servidor
```bash
python manage.py migrate
python manage.py runserver
```
Acesse `http://127.0.0.1:8000/`.

### 3. Build estático (modo híbrido)
Para gerar apenas o front-end estático em `_site/` apontando para a API do Render:
```bash
python3 scripts/build_pages.py
```
Variáveis opcionais: `API_BASE` (padrão `https://portfolio-higor.onrender.com`) e `SITE_BASE` (padrão `""` para raiz do domínio, ou `/portfolio-higor` para GitHub Pages). Em produção, adicione o domínio do front-end na variável `CORS_ORIGINS` do Render.

---

## Testes Automatizados

```bash
python manage.py test
```

---

## Autor

**Higor do Amaral Fritz**  
*Graduando em Bacharelado em Sistemas de Informação — IFC Câmpus Araquari*  
*Técnico em Informática para Internet — IFC Câmpus Araquari*

* **Portfólio:** [portfolio-higor.onrender.com](https://portfolio-higor.onrender.com)
* **GitHub:** [@HigorAmaral](https://github.com/HigorAmaral)
* **E-mail:** [amarahigor@gmail.com](mailto:amarahigor@gmail.com)
* **Currículo (PT-BR):** [curriculo-higor.pdf](static/curriculo-higor.pdf)
* **Resume (EN):** [curriculo-higor-en.pdf](static/curriculo-higor-en.pdf)
* **Padrão de Repositórios:** [docs/GUIA_PADRAO_REPOSITORIOS.md](docs/GUIA_PADRAO_REPOSITORIOS.md)

---

## Licença

Projeto desenvolvido para fins acadêmicos e profissionais de exibição de portfólio.

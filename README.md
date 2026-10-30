# 🚀 Portfólio Pessoal & API REST — Higor do Amaral Fritz

Aplicação web full-stack desenvolvida com **Django** no backend e interface moderna, responsiva e acessível no frontend. O projeto atua como o portfólio oficial de Higor do Amaral Fritz, reunindo projetos de software, artigos científicos (BSI/IFC), mural de recados interativo e documentação de API REST padronizada.

[![Deploy no Render](https://img.shields.io/badge/Deploy-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://portfolio-higor.onrender.com)
[![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![CI/CD](https://img.shields.io/badge/GitHub_Actions-CI_Passed-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/HigorAmaral/portfolio-higor/actions)
[![OpenAPI](https://img.shields.io/badge/Swagger-OpenAPI_3.0-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)](https://portfolio-higor.onrender.com/api/docs/)

---

## 🌐 Demonstração ao Vivo

* **Portfólio Oficial:** [portfolio-higor.onrender.com](https://portfolio-higor.onrender.com)
* **Documentação Interativa da API (Swagger UI):** [portfolio-higor.onrender.com/api/docs/](https://portfolio-higor.onrender.com/api/docs/)
* **Health Check & Integridade Operacional:** [portfolio-higor.onrender.com/healthz/](https://portfolio-higor.onrender.com/healthz/)

---

## 🛠️ Tecnologias & Arquitetura

### Back-end & Infraestrutura
* **Linguagem & Framework:** Python 3.12+ com Django 6.
* **Banco de Dados:** PostgreSQL (produção na nuvem) e SQLite (desenvolvimento local ágil).
* **Servidor de Produção:** Gunicorn gerenciado por container Linux no Render.
* **Arquivos Estáticos:** WhiteNoise com compressão gzip/brotli e cache agressivo de ativos.
* **Documentação de API:** Especificação OpenAPI 3.0 com interface Swagger UI interativa nativa.
* **CI/CD:** Pipeline automatizado no GitHub Actions executando 21 testes unitários em cada push.

### Front-end & Interface
* **Arquitetura:** HTML5 semântico, CSS3 com design tokens e JavaScript Vanilla (zero frameworks pesados para carregamento ultra-rápido).
* **Acessibilidade & Design:** Paleta dinâmica adaptada para modo escuro e claro (Dark/Light mode) com cálculo de contraste harmonioso (`color-mix`), tipografia fluida e suporte a leitores de tela.
* **Estudos de Caso:** Modais interativos detalhando desafios técnicos, decisões de engenharia e resultados de projetos.

---

## 🔒 Segurança & Boas Práticas (OWASP Compliance)

A aplicação foi projetada seguindo diretrizes estritas de *Security by Design*:

* **Proteção de Headers HTTP:**
  * **Content Security Policy (CSP):** Políticas estritas de execução de scripts, conexões e estilização.
  * **HTTP Strict Transport Security (HSTS):** Forçamento de criptografia de ponta a ponta (`max-age=31536000; includeSubDomains; preload`).
  * **Isolamento de Origem:** `Cross-Origin-Opener-Policy: same-origin` e `Cross-Origin-Resource-Policy: same-origin`.
  * **Prevenção de Clickjacking & MIME Sniffing:** `X-Frame-Options: DENY` e `X-Content-Type-Options: nosniff`.
* **Rate Limiting & Anti-Abuso:**
  * Limitador de requisições por IP confiável com suporte a cabeçalhos de proxy reverso (*Cloudflare / Render*).
  * Mecanismo de *honeypot* e sanitização automática de caracteres maliciosos contra bots de spam.
* **Prevenção de Injeções (XSS & SQLi):**
  * Uso integral do ORM parametrizado do Django para proteção contra SQL Injection.
  * Renderização de dados como texto seguro, sem parsing perigoso de HTML não sanitizado.
* **Privacidade & Conformidade LGPD (Lei nº 13.709/2018):**
  * Métricas anônimas de telemetria sem armazenamento de endereços IP ou identificadores pessoais rastreáveis.
* **Gestão de Dependências:**
  * Auditoria contínua de vulnerabilidades de pacotes com Dependabot e `pip-audit`.

---

## 📁 Estrutura do Repositório

```text
portfolio-higor/
├── config/              # Configurações globais, segurança, middleware e URLs do Django
│   ├── middleware.py    # Headers HTTP de segurança, rate limit e validação de proxies
│   ├── seguranca.py     # Auditoria de ambiente e boas práticas em tempo de execução
│   └── settings.py      # Configuração desacoplada de ambientes (produção / dev)
├── recados/             # Aplicação core: models, views REST, testes e openapi.py
│   ├── models.py        # Modelagem de dados (Recados, Projetos, Habilidades, Métricas)
│   ├── openapi.py       # Especificação técnica do Swagger UI (OpenAPI 3.0)
│   ├── tests.py         # Suíte com 21 testes unitários automatizados
│   └── views.py         # Endpoints da API, mural de recados e health check
├── frontend/            # Frontend do site (HTML5, CSS modular e JavaScript)
│   └── index.html       # Single Page com tema dinâmico, animações e integração REST
├── static/              # Ativos públicos (PDFs de artigos, ícones, temas)
├── .github/             # Pipelines de automação CI/CD do GitHub Actions
├── manage.py            # Utilitário de gerenciamento do projeto
├── render.yaml          # Infraestrutura como código (IaC) para deploy no Render
└── requirements.txt     # Dependências de produção
```

---

## 💻 Como Rodar o Projeto Localmente

### Pré-requisitos
* Python 3.12 ou superior instalado.
* Git instalado.

### 1. Clonar o repositório
```bash
git clone https://github.com/HigorAmaral/portfolio-higor.git
cd portfolio-higor
```

### 2. Criar e ativar o ambiente virtual
```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto baseado no `.env.example`:
```bash
cp .env.example .env
```
*(Em ambiente de desenvolvimento, sem configurar banco de dados externo, o Django utilizará automaticamente o SQLite integrado).*

### 5. Executar as migrações e iniciar o servidor
```bash
python manage.py migrate
python manage.py runserver
```

Acesse a aplicação no navegador em: `http://127.0.0.1:8000/`

---

## 🧪 Executando os Testes Automatizados

O projeto conta com testes unitários cobrindo endpoints de API, validações de integridade, rate limiting, regras de negócio e proteção de dados:

```bash
python manage.py test
```

---

## 👨‍💻 Autor

**Higor do Amaral Fritz**  
*Graduando em Bacharelado em Sistemas de Informação — IFC Câmpus Araquari*  
*Técnico em Informática para Internet — IFC Câmpus Araquari*

* **Portfólio:** [portfolio-higor.onrender.com](https://portfolio-higor.onrender.com)
* **GitHub:** [@HigorAmaral](https://github.com/HigorAmaral)
* **E-mail:** [amarahigor@gmail.com](mailto:amarahigor@gmail.com)

---

## 📄 Licença

Este projeto é desenvolvido para fins acadêmicos e profissionais de exibição de portfólio.

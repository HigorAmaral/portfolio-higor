# Portfólio — Higor do Amaral Fritz

Site com **front-end** (HTML/CSS/JS puro) e **backend** em Django com banco **MySQL**.
O backend guarda o mural de recados e entrega o site.

```
portfolio-higor/
├── frontend/index.html     ← o site (pode ser hospedado separado)
├── config/                 ← configurações do Django
├── recados/                ← API do mural + painel de moderação
├── manage.py
├── requirements.txt
└── .env.example
```

## 1. Rodar no seu computador (Ubuntu)

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip

cd portfolio-higor
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
DEBUG=1 python manage.py runserver
```

No Ubuntu o comando é `python3` fora do ambiente virtual; depois do `source venv/bin/activate`, `python` também funciona.
Abra http://127.0.0.1:8000. Sem `DB_NAME` no `.env`, ele usa SQLite (bom para testar).

Problemas comuns:
- `ensurepip is not available`: instale `python3-venv` (comando acima).
- `command not found: python`: use `python3`, ou ative o ambiente virtual.
- Erro de porta ocupada: use `python manage.py runserver 8080`.

## 2. Usar o MySQL

Crie o banco e o usuário:

```sql
CREATE DATABASE portfolio CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'portfolio'@'localhost' IDENTIFIED BY 'sua-senha';
GRANT ALL PRIVILEGES ON portfolio.* TO 'portfolio'@'localhost';
```

Instale as dependências do MySQL no Ubuntu e o driver Python:

```bash
sudo apt install -y build-essential pkg-config default-libmysqlclient-dev python3-dev
pip install -r requirements-mysql.txt
```

Copie `.env.example` para `.env`, preencha `DB_NAME`, `DB_USER`, `DB_PASSWORD` e rode `python manage.py migrate`.

## 3. Colocar no ar (servidor/VPS)

1. Envie a pasta para o servidor e crie o `.env` (com `DEBUG=0`, `SECRET_KEY` nova, seu domínio em `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS`).
2. `pip install -r requirements.txt -r requirements-mysql.txt`, `python manage.py migrate`, `python manage.py collectstatic --noinput`, `python manage.py createsuperuser`.
3. Rode com Gunicorn: `gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 2`.
4. Use Nginx (ou Caddy) na frente, com HTTPS (Let's Encrypt), enviando o tráfego para a porta 8000.
   Mantenha `HTTPS=1` e `BEHIND_PROXY=1` no `.env`.

Serviços como Render, Railway ou PythonAnywhere também servem: o comando de start é o do Gunicorn acima e as variáveis do `.env` vão no painel deles.

### Publicar no Render

Este projeto já inclui `render.yaml`. Para publicar:

1. Abra o repositório no GitHub e, no Render, escolha **New > Blueprint**.
2. Selecione o repositório `HigorAmaral/portfolio-higor`.
3. Confirme a criação do serviço web e do banco PostgreSQL.
4. O Render instalará as dependências, executará as migrações e iniciará o Gunicorn automaticamente.
5. Depois do primeiro deploy, crie o administrador no Shell do serviço:

   ```bash
   python manage.py createsuperuser
   ```

O front-end e a API serão servidos pelo mesmo endereço do serviço. O painel ficará em `/admin/`.
Para usar domínio próprio, atualize `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS` nas variáveis do serviço.

## 4. Moderar os recados

Entre em `/admin`, abra **Recados** e desmarque **Visível** (ou apague) o que for indevido.

## 5. Editar habilidades e projetos (painel admin)

Entre em `/admin` e use:
- **Habilidades:** adicione, edite, esconda (desmarque *Visível*) ou apague. Em *Tecnologias*, separe por vírgula. O número de *Ordem* define a posição (menor aparece primeiro).
- **Projetos:** mesmos campos, mais o **Status** (*Em andamento* ou *Concluído*) e o link do GitHub. Sem link, o botão não aparece.
- **Recados:** moderação do mural.

As mudanças aparecem no site ao recarregar a página. Se atualizar o projeto, rode `python manage.py migrate` de novo
(ele cria as tabelas e já cadastra as habilidades e projetos atuais; confira o status de cada projeto no painel).

**Visual do painel:** o tema fica em `static/tema/admin.css` e `templates/admin/base_site.html` (mesma paleta do site, com modo claro e escuro).
Se o painel aparecer sem estilo, rode `python manage.py collectstatic --noinput` e recarregue com Ctrl+Shift+R.

## 6. Front-end em outro lugar (opcional)

Para hospedar só o `frontend/index.html` em Netlify, Vercel, GitHub Pages etc.:

1. No `index.html`, troque `<meta name="api-base" content="">` por `<meta name="api-base" content="https://api.seudominio.com">`.
2. No `.env` do backend, coloque `CORS_ORIGINS=https://seusite.com`.

## Segurança já incluída

- Limite de 1 recado a cada 30 segundos por IP e campo escondido contra robôs.
- Textos exibidos como texto puro (sem executar HTML) e limites de tamanho.
- Cookies e HTTPS reforçados quando `HTTPS=1`.
- O limite por IP usa a memória do processo. Para mais robustez com vários workers, configure um cache compartilhado (Redis, por exemplo).

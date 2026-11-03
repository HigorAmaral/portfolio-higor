from django.db import migrations


def adicionar_novos_projetos(apps, schema_editor):
    Projeto = apps.get_model("recados", "Projeto")

    novos_projetos = [
        {
            "nome": "EcoApack — Catálogo Industrial & Orçamentos B2B",
            "badge": "React 19 · B2B & Catálogo Interativo",
            "descricao": (
                "Plataforma web corporativa B2B desenvolvida em React 19 para indústria de embalagens plásticas "
                "sustentáveis. Conta com catálogo interativo de baldes industriais, configurador dinâmico de cores "
                "(corpo e tampa), lupa de zoom em alta resolução e automação de orçamentos via EmailJS."
            ),
            "tecnologias": "React 19, JavaScript, Bootstrap 5, EmailJS, PWA, Vercel",
            "github": "https://github.com/HigorAmaral/eco-park-application",
            "demo": "https://eco-park-application.vercel.app",
            "status": "concluido",
            "ordem": 5,
            "visivel": True,
            "estudo_titulo": "EcoApack — Catálogo Industrial & Orçamentos B2B",
            "estudo_desafio": (
                "Digitalizar a vitrine comercial de uma indústria de embalagens plásticas sustentáveis "
                "(baldes industriais de 1kg e 1,2kg), permitindo que compradores B2B inspecionem detalhes técnicos "
                "das peças, simulem combinações de cores e solicitem cotações rápidas sem depender de atendimento manual lento."
            ),
            "estudo_solucao": (
                "Desenvolvimento de uma Single Page Application (SPA) em React 19 hospedada na Vercel, com seletor "
                "interativo de cores para tampa e corpo do produto, efeito de lupa dinâmica (zoom in-place por coordenadas "
                "do cursor), animações de revelação com IntersectionObserver e envio automatizado de propostas comerciais "
                "e contatos diretamente por EmailJS."
            ),
            "estudo_aprendizados": (
                "Componentização avançada e hooks no React 19, manipulação de eventos de ponteiro para zoom óptico "
                "de produto, integração de mensageria serverless (EmailJS) e otimização de performance e SEO para páginas corporativas."
            ),
        },
        {
            "nome": "Primeiro Lar Imobiliária",
            "badge": "Vue 3 & Pinia · Integração API IBGE",
            "descricao": (
                "Aplicação imobiliária para compra, venda, anúncio e favoritismo de imóveis construída com Vue 3, "
                "Vite e Pinia. Integra a API oficial de localidades do IBGE em tempo real para filtragem dinâmica "
                "por estados (UF) e municípios brasileiros, além de consumo de API REST via Axios."
            ),
            "tecnologias": "Vue 3, Vite, Pinia, Vue Router, Axios, API IBGE, PWA",
            "github": "https://github.com/HigorAmaral/front-primeiro.lar-25",
            "demo": "https://front-primeirolar-25.vercel.app",
            "status": "concluido",
            "ordem": 6,
            "visivel": True,
            "estudo_titulo": "Primeiro Lar Imobiliária — Portal de Imóveis",
            "estudo_desafio": (
                "Construir uma plataforma imobiliária moderna e responsiva onde usuários possam buscar imóveis "
                "com filtros precisos de localização em todo o território nacional, cadastrar anúncios de venda "
                "e gerenciar sua lista de imóveis favoritos com estado sincronizado."
            ),
            "estudo_solucao": (
                "Arquitetura front-end modular em Vue 3 (Vite) com gerenciamento de estado global via Pinia e "
                "roteamento protegido no Vue Router. Consumo em tempo real da API de Localidades do IBGE para "
                "carregamento dinâmico de UFs e cidades por estado selecionado, integração com backend RESTful via "
                "Axios e suporte a instalação como Progressive Web App (PWA)."
            ),
            "estudo_aprendizados": (
                "Gerenciamento de estado global escalável com Pinia, consumo combinado de APIs públicas governamentais "
                "(IBGE) e APIs próprias com Axios, navegação SPA avançada e configuração de PWA com Vite."
            ),
        },
        {
            "nome": "API RESTful Livraria & Gestão de Acervo",
            "badge": "Django REST · JWT Auth & OpenAPI 3",
            "descricao": (
                "Backend RESTful completo construído com Django e Django REST Framework (DRF) para gestão de acervo "
                "literário, editoras, autores e fluxo transacional de compras. Possui autenticação JWT (SimpleJWT), "
                "upload de capas na nuvem via Cloudinary, filtros avançados e documentação OpenAPI 3 (Swagger e Redoc)."
            ),
            "tecnologias": "Python, Django REST Framework, PostgreSQL, JWT Auth, Swagger / Redoc, Cloudinary",
            "github": "https://github.com/HigorAmaral/livraria_3info1_2025-1",
            "demo": "",
            "status": "concluido",
            "ordem": 7,
            "visivel": True,
            "estudo_titulo": "API RESTful de Livraria & Fluxo de Compras (DRF)",
            "estudo_desafio": (
                "Projetar um backend desacoplado e escalável capaz de gerenciar todo o ciclo de catálogo de uma "
                "livraria (livros, autores, categorias e editoras), perfis de usuários customizados, upload de mídias "
                "e processamento transacional de carrinhos e itens de compra."
            ),
            "estudo_solucao": (
                "Implementação de API RESTful com Django REST Framework gerenciada via PDM, autenticação stateless "
                "com JSON Web Tokens (djangorestframework-simplejwt), armazenamento de imagens em nuvem com Cloudinary, "
                "filtragem avançada com django-filter, suporte a CORS e geração automática de documentação interativa "
                "Swagger UI e Redoc com drf-spectacular."
            ),
            "estudo_aprendizados": (
                "Arquitetura de APIs RESTful corporativas com DRF, serializadores aninhados para pedidos e itens de "
                "compra, autenticação JWT segura, integração de storage em nuvem e documentação padronizada OpenAPI 3.0."
            ),
        },
        {
            "nome": "AgroNovo-Mundo — E-commerce Agro & Pet",
            "badge": "Mostra SEPE · IFC Araquari",
            "descricao": (
                "E-commerce departamental agropecuário e pet shop desenvolvido em Vue 3 para a Semana de Ensino, "
                "Pesquisa e Extensão (SEPE — IFC). Conta com carrinho de compras reativo, lista de favoritos, busca "
                "global em tempo real entre componentes, autenticação Google OAuth e integração com WhatsApp."
            ),
            "tecnologias": "Vue 3, Vite, Vue Router, Google OAuth, Carrinho Reativo, PWA",
            "github": "https://github.com/HigorAmaral/Eco-Park",
            "demo": "",
            "status": "concluido",
            "ordem": 8,
            "visivel": True,
            "estudo_titulo": "AgroNovo-Mundo — E-commerce Agropecuário & Pet (SEPE IFC)",
            "estudo_desafio": (
                "Desenvolver uma loja virtual segmentada em múltiplos departamentos técnicos (Rações, Medicamentos, "
                "Ferragens, Pets, Dedetização e Hormônios) com busca instantânea, carrinho unificado e cálculo dinâmico "
                "de subtotais para apresentação na Semana de Ensino, Pesquisa e Extensão (SEPE) do IFC."
            ),
            "estudo_solucao": (
                "Construção de uma SPA em Vue 3 e Vue Router utilizando a API de Composition (provide/inject e "
                "watchers reativos) para compartilhar o estado do carrinho, favoritos e barra de pesquisa global entre "
                "todas as rotas departamentais, além de autenticação social via Google OAuth (vue3-google-login) e "
                "geolocalização via Google Maps."
            ),
            "estudo_aprendizados": (
                "Comunicação reativa entre múltiplos componentes com Provide/Inject no Vue 3, implementação de fluxos "
                "completos de carrinho de e-commerce, autenticação OAuth2 com Google e apresentação técnica em evento acadêmico."
            ),
        },
    ]

    for item in novos_projetos:
        Projeto.objects.update_or_create(
            nome=item["nome"],
            defaults={
                "badge": item["badge"],
                "descricao": item["descricao"],
                "tecnologias": item["tecnologias"],
                "github": item["github"],
                "demo": item["demo"],
                "status": item["status"],
                "ordem": item["ordem"],
                "visivel": item["visivel"],
                "estudo_titulo": item["estudo_titulo"],
                "estudo_desafio": item["estudo_desafio"],
                "estudo_solucao": item["estudo_solucao"],
                "estudo_aprendizados": item["estudo_aprendizados"],
            },
        )


def remover_novos_projetos(apps, schema_editor):
    Projeto = apps.get_model("recados", "Projeto")
    nomes = [
        "EcoApack — Catálogo Industrial & Orçamentos B2B",
        "Primeiro Lar Imobiliária",
        "API RESTful Livraria & Gestão de Acervo",
        "AgroNovo-Mundo — E-commerce Agro & Pet",
    ]
    Projeto.objects.filter(nome__in=nomes).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("recados", "0014_remover_emojis_badge"),
    ]

    operations = [
        migrations.RunPython(adicionar_novos_projetos, remover_novos_projetos),
    ]

OPENAPI_SPEC = {
    "openapi": "3.0.3",
    "info": {
        "title": "API Portfólio Higor Amaral",
        "version": "1.0.0",
        "description": "API RESTful em Django para o portfólio profissional de Higor do Amaral Fritz (Desenvolvedor Full Stack Python/Django).",
        "contact": {
            "name": "Higor do Amaral Fritz",
            "url": "https://portfolio-higor.onrender.com",
            "email": "higoramaralfritz@gmail.com",
        },
    },
    "servers": [
        {"url": "/", "description": "Servidor Atual"},
    ],
    "paths": {
        "/healthz/": {
            "get": {
                "summary": "Health Check do Sistema",
                "description": "Verifica conectividade com banco de dados, cache em memória e tempo de resposta.",
                "responses": {
                    "200": {
                        "description": "Sistema saudável e operacional.",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "healthy",
                                    "database": "connected",
                                    "cache": "operational",
                                    "tempo_resposta_ms": 1.25,
                                    "timestamp": "2026-10-30T12:00:00Z",
                                }
                            }
                        },
                    },
                    "503": {
                        "description": "Falha na integridade do banco ou cache.",
                    },
                },
            }
        },
        "/api/recados/": {
            "get": {
                "summary": "Listar Recados do Mural",
                "description": "Retorna os 30 recados mais recentes marcados como visíveis.",
                "responses": {
                    "200": {
                        "description": "Lista de recados.",
                        "content": {
                            "application/json": {
                                "example": [
                                    {
                                        "nome": "Recrutador Tech",
                                        "texto": "Parabéns pelo projeto! Excelente portfólio.",
                                        "criado_em": "2026-10-30T10:15:00.000000",
                                    }
                                ]
                            }
                        },
                    }
                },
            },
            "post": {
                "summary": "Publicar Novo Recado",
                "description": "Envia um recado com sanitização HTML (anti-XSS), rate limiting (30s) e armadilha honeypot.",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "nome": {"type": "string", "maxLength": 40, "example": "Carlos Silva"},
                                    "texto": {"type": "string", "maxLength": 280, "example": "Excelente trabalho!"},
                                    "site": {"type": "string", "description": "Armadilha honeypot para robôs (deve vir vazia).", "example": ""},
                                },
                                "required": ["texto"],
                            }
                        }
                    },
                },
                "responses": {
                    "201": {"description": "Recado publicado com sucesso."},
                    "400": {"description": "Texto vazio, tamanho acima de 280 caracteres ou JSON inválido."},
                    "413": {"description": "Payload excede o tamanho máximo de 10 KB."},
                    "429": {"description": "Rate limit atingido (espere 30 segundos entre recados)."},
                },
            },
        },
        "/api/conteudo/": {
            "get": {
                "summary": "Obter Habilidades e Projetos",
                "description": "Retorna os projetos e habilidades públicas cadastradas via Django Admin.",
                "responses": {
                    "200": {
                        "description": "Conteúdo dinâmico.",
                        "content": {
                            "application/json": {
                                "example": {
                                    "habilidades": [
                                        {"titulo": "Backend Python", "descricao": "APIs REST com Django", "tecnologias": ["Python", "Django", "PostgreSQL"]}
                                    ],
                                    "projetos": [
                                        {
                                            "nome": "Portfólio Pessoal",
                                            "descricao": "Sistema completo com Django",
                                            "tecnologias": ["Django", "Python", "PostgreSQL"],
                                            "github": "https://github.com/HigorAmaral/portfolio-higor",
                                            "demo": "https://portfolio-higor.onrender.com",
                                            "status": "concluido",
                                            "status_label": "Concluído",
                                        }
                                    ],
                                }
                            }
                        },
                    }
                },
            }
        },
        "/api/visitas/": {
            "post": {
                "summary": "Registrar Métrica Anônima de Acesso (LGPD)",
                "description": "Contabiliza visualizações de página ou downloads de currículo sem cookies nem identificação individual.",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "tipo": {"type": "string", "enum": ["pagina", "download_curriculo"], "example": "pagina"},
                                    "caminho": {"type": "string", "maxLength": 100, "example": "/"},
                                },
                            }
                        }
                    },
                },
                "responses": {
                    "200": {"description": "Métrica computada com sucesso."},
                    "400": {"description": "Tipo de métrica inválido."},
                },
            }
        },
    },
}

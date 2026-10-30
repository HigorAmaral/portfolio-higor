import os
import secrets
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

try:
    import pymysql

    pymysql.install_as_MySQLdb()
    pymysql.version_info = (1, 4, 3, "final", 0)
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def env_list(nome, padrao=""):
    return [x.strip() for x in os.environ.get(nome, padrao).split(",") if x.strip()]


DEBUG = os.environ.get("DEBUG", "0") == "1"

# Chave secreta segura: se estiver em produção e não houver SECRET_KEY, gera uma chave criptográfica forte
_secret_env = os.environ.get("SECRET_KEY")
if _secret_env:
    SECRET_KEY = _secret_env
elif DEBUG:
    SECRET_KEY = "apenas-para-desenvolvimento-local-inseguro-apenas-teste"
else:
    # Gera fallback seguro aleatório para evitar rodar chave padrão em produção
    SECRET_KEY = secrets.token_urlsafe(64)

# Proteção contra Host Header Poisoning
if not DEBUG:
    ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", ".onrender.com,localhost,127.0.0.1")
else:
    ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", "*")

CSRF_TRUSTED_ORIGINS = env_list(
    "CSRF_TRUSTED_ORIGINS",
    "https://*.onrender.com,https://portfolio-higor.onrender.com",
)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "recados",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "config.middleware.SecurityHeadersMiddleware",
    "config.middleware.AdminBruteForceMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
CSRF_FAILURE_VIEW = "recados.erros.erro_csrf"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

if os.environ.get("DATABASE_URL"):
    DATABASES = {
        "default": dj_database_url.config(
            default=os.environ.get("DATABASE_URL"),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
elif os.environ.get("DB_NAME"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.environ["DB_NAME"],
            "USER": os.environ.get("DB_USER", ""),
            "PASSWORD": os.environ.get("DB_PASSWORD", ""),
            "HOST": os.environ.get("DB_HOST", "localhost"),
            "PORT": os.environ.get("DB_PORT", "3306"),
            "OPTIONS": {"charset": "utf8mb4"},
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Senhas fortes obrigatórias para usuários do painel admin
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 10}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Limites globais de requisição (proteção contra DoS por payload/quantidade de campos)
DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024  # 1 MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 500
FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024

# Sessão do admin expira em 8 horas e ao fechar o navegador
SESSION_COOKIE_AGE = 8 * 60 * 60
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Logs no console (visíveis no painel do Render), sem dados sensíveis
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "WARNING"},
    "loggers": {
        "django.security": {"handlers": ["console"], "level": "WARNING", "propagate": False},
    },
}
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = DEBUG
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
}

# CORS: desabilitado por padrão para domínios arbitrários
CORS_ALLOWED_ORIGINS = env_list("CORS_ORIGINS")
CORS_URLS_REGEX = r"^/api/.*$"

# Configurações de Segurança e Cookies
BEHIND_PROXY = os.environ.get("BEHIND_PROXY", "1") == "1"
if BEHIND_PROXY:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

if not DEBUG:
    # Produção HTTPS e Headers Estritos
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    CSRF_COOKIE_SAMESITE = "Lax"

    SECURE_SSL_REDIRECT = BEHIND_PROXY or os.environ.get("HTTPS", "1") == "1"
    SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", 31536000))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
else:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False
    SECURE_HSTS_SECONDS = 0

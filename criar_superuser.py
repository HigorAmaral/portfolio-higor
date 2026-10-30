import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model  # noqa: E402

User = get_user_model()
username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

if password:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"Superuser '{username}' criado com sucesso!")
    else:
        user = User.objects.get(username=username)
        user.set_password(password)
        if email:
            user.email = email
        user.save()
        print(f"Superuser '{username}' atualizado com sucesso!")
else:
    print("DJANGO_SUPERUSER_PASSWORD não configurado; pulando criação de superuser.")

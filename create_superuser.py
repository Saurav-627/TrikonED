import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

User = get_user_model()
username = 'admin'
email = 'admin@gmail.com'
password = 'trikoned'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' created successfully.")
else:
    user = User.objects.get(username=username)
    user.email = email
    user.set_password(password)
    user.save()
    print(f"Superuser '{username}' updated successfully with new email/password.")

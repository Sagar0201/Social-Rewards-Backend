# create_admin.py

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_rewards.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', '12345')
    print("Superuser 'admin' created.")
else:
    print("Superuser 'admin' already exists.")

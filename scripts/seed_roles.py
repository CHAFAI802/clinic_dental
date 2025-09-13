# scripts/seed_roles.py
import os
import django

# --- Initialisation Django ---
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dental_clinic.settings")
django.setup()

from accounts.models import CustomUser

def run():
    users_data = [
        {
            "email": "admin@cabinet.com",
            "password": "Admin123!",
            "role": "admin",
            "is_staff": True,
            "is_superuser": True,
        },
        {
            "email": "medecin@cabinet.com",
            "password": "Medecin123!",
            "role": "medecin",
            "is_staff": True,
            "is_superuser": False,
        },
        {
            "email": "secretaire@cabinet.com",
            "password": "Secretaire123!",
            "role": "secretaire",
            "is_staff": True,
            "is_superuser": False,
        },
    ]

    for user_data in users_data:
        if not CustomUser.objects.filter(email=user_data["email"]).exists():
            user = CustomUser.objects.create_user(
                email=user_data["email"],
                password=user_data["password"],
                role=user_data["role"],
            )
            user.is_staff = user_data["is_staff"]
            user.is_superuser = user_data["is_superuser"]
            user.save()
            print(f"✅ Créé : {user.email} ({user.role})")
        else:
            print(f"⚠️ Existe déjà : {user_data['email']}")

if __name__ == "__main__":
    run()

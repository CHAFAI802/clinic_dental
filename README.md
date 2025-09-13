# Clinic Dental

Projet Django complet de gestion d’un cabinet dentaire  
(Gestion des patients, rendez-vous, facturation, prescriptions, stock…).

## Prérequis

- Python 3.x installé
- pip et virtualenv
- Git

## Installation locale

```bash
git clone https://github.com/CHAFAI802/clinic_dental.git
cd clinic_dental
python -m venv venv
source venv/Scripts/activate  # sous Windows PowerShell
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

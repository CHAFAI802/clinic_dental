from django.test import TestCase, Client,RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from axes.utils import reset

User = get_user_model()


class CustomUserModelTest(TestCase):
    """Tests pour le modèle CustomUser"""
    
    def setUp(self):
        """Créer des utilisateurs de test"""
        self.medecin = User.objects.create_user(
            email='medecin@test.com',
            password='Test1234!',
            first_name='Jean',
            last_name='DUPONT',
            role='medecin'
        )
        
        self.secretaire = User.objects.create_user(
            email='secretaire@test.com',
            password='Test1234!',
            first_name='Marie',
            last_name='MARTIN',
            role='secretaire'
        )
    
    def test_user_creation(self):
        """Test de création d'utilisateur"""
        self.assertEqual(self.medecin.email, 'medecin@test.com')
        self.assertTrue(self.medecin.check_password('Test1234!'))
        self.assertEqual(self.medecin.role, 'medecin')
        self.assertTrue(self.medecin.is_active)
        self.assertFalse(self.medecin.is_staff)
    
    def test_superuser_creation(self):
        """Test de création de superutilisateur"""
        admin = User.objects.create_superuser(
            email='admin@test.com',
            password='Admin1234!'
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertEqual(admin.role, 'admin')
    
    def test_get_full_name(self):
        """Test de la méthode get_full_name"""
        self.assertEqual(self.medecin.get_full_name(), 'Jean DUPONT')
        
        # Test avec utilisateur sans nom
        user_no_name = User.objects.create_user(
            email='test@test.com',
            password='Test1234!'
        )
        self.assertEqual(user_no_name.get_full_name(), '')
    
    def test_get_short_name(self):
        """Test de la méthode get_short_name"""
        self.assertEqual(self.medecin.get_short_name(), 'Jean')
        
        # Test avec utilisateur sans prénom
        user_no_name = User.objects.create_user(
            email='nofirstname@test.com',
            password='Test1234!'
        )
        self.assertEqual(user_no_name.get_short_name(), 'nofirstname')
    
    def test_is_medecin(self):
        """Test de la méthode is_medecin"""
        self.assertTrue(self.medecin.is_medecin())
        self.assertFalse(self.secretaire.is_medecin())
    
    def test_is_secretaire(self):
        """Test de la méthode is_secretaire"""
        self.assertTrue(self.secretaire.is_secretaire())
        self.assertFalse(self.medecin.is_secretaire())
    
    def test_is_admin_user(self):
        """Test de la méthode is_admin_user"""
        admin = User.objects.create_superuser(
            email='admin@test.com',
            password='Admin1234!'
        )
        self.assertTrue(admin.is_admin_user())
        self.assertFalse(self.medecin.is_admin_user())
    
    def test_user_string_representation(self):
        """Test de la représentation en chaîne"""
        self.assertEqual(str(self.medecin), 'Jean DUPONT')
    
    def test_email_is_unique(self):
        """Test que l'email est unique"""
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email='medecin@test.com',  # Email déjà utilisé
                password='Test1234!'
            )


class CustomUserCreationFormTest(TestCase):
    """Tests pour le formulaire d'inscription"""
    
    def test_valid_form(self):
        """Test avec des données valides"""
        form_data = {
            'email': 'nouveau@test.com',
            'first_name': 'Pierre',
            'last_name': 'DURAND',
            'role': 'medecin',
            'password1': 'Test1234!',
            'password2': 'Test1234!',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_email_already_exists(self):
        """Test avec un email déjà existant"""
        User.objects.create_user(
            email='existing@test.com',
            password='Test1234!'
        )
        
        form_data = {
            'email': 'existing@test.com',
            'first_name': 'Pierre',
            'last_name': 'DURAND',
            'role': 'medecin',
            'password1': 'Test1234!',
            'password2': 'Test1234!',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_passwords_dont_match(self):
        """Test avec des mots de passe différents"""
        form_data = {
            'email': 'nouveau@test.com',
            'first_name': 'Pierre',
            'last_name': 'DURAND',
            'role': 'medecin',
            'password1': 'Test1234!',
            'password2': 'Different1234!',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
    
    def test_email_normalization(self):
        """Test de la normalisation de l'email (lowercase)"""
        form_data = {
            'email': 'UPPERCASE@TEST.COM',
            'first_name': 'Pierre',
            'last_name': 'durand',
            'role': 'medecin',
            'password1': 'Test1234!',
            'password2': 'Test1234!',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.email, 'uppercase@test.com')
        self.assertEqual(user.last_name, 'DURAND')  # Uppercase
        self.assertEqual(user.first_name, 'Pierre')  # Capitalize


class CustomAuthenticationFormTest(TestCase):
    """Tests pour le formulaire de connexion"""
    
    def setUp(self):
        """Créer un utilisateur de test et un RequestFactory"""
        self.user = User.objects.create_user(
            email='user@test.com',
            password='Test1234!',
            first_name='Test',
            last_name='USER'
        )
        self.factory = RequestFactory()
    
    def test_valid_login(self):
        """Test avec des identifiants valides"""
        form_data = {
            'username': 'user@test.com',
            'password': 'Test1234!',
        }
        request = self.factory.post('/login/', data=form_data)
        form = CustomAuthenticationForm(request=request, data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_email(self):
        """Test avec un email invalide"""
        form_data = {
            'username': 'invalid-email',
            'password': 'Test1234!',
        }
        form = CustomAuthenticationForm(data=form_data)
        self.assertFalse(form.is_valid())


class RegistrationViewTest(TestCase):
    """Tests pour la vue d'inscription"""
    
    def setUp(self):
        """Configurer le client de test"""
        self.client = Client()
        self.register_url = reverse('accounts:register')
    
    def test_register_page_loads(self):
        """Test du chargement de la page d'inscription"""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertContains(response, 'Créer un compte')
    
    def test_register_success(self):
        """Test d'inscription réussie"""
        response = self.client.post(self.register_url, {
            'email': 'newuser@test.com',
            'first_name': 'Nouveau',
            'last_name': 'UTILISATEUR',
            'role': 'secretaire',
            'password1': 'Test1234!',
            'password2': 'Test1234!',
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='newuser@test.com').exists())
        user = User.objects.get(email='newuser@test.com')
        self.assertEqual(user.first_name, 'Nouveau')
    
    def test_register_with_existing_email(self):
        """Test d'inscription avec un email existant"""
        User.objects.create_user(
            email='existing@test.com',
            password='Test1234!'
        )
        
        response = self.client.post(self.register_url, {
            'email': 'existing@test.com',
            'first_name': 'Test',
            'last_name': 'USER',
            'role': 'secretaire',
            'password1': 'Test1234!',
            'password2': 'Test1234!',
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', 
                           'Cette adresse email est déjà utilisée.')
    
    def test_register_redirects_if_authenticated(self):
        """Test que l'utilisateur connecté est redirigé"""
        user = User.objects.create_user(
            email='user@test.com',
            password='Test1234!'
        )
        self.client.login(username='user@test.com', password='Test1234!')
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 302)


class LoginViewTest(TestCase):
    """Tests pour la vue de connexion"""
    
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('accounts:login')
        self.user = User.objects.create_user(
            email='user@test.com',
            password='Test1234!',
            first_name='Test',
            last_name='USER'
        )
    
    def test_login_page_loads(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertContains(response, 'Connexion')
    
    def test_login_success(self):
        response = self.client.post(self.login_url, {
            'username': 'user@test.com',
            'password': 'Test1234!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_login_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': 'user@test.com',
            'password': 'WrongPassword!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'incorrect')
    
    def test_login_redirects_if_authenticated(self):
        self.client.login(username='user@test.com', password='Test1234!')
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 302)
    
    def test_login_with_next_parameter(self):
        next_url = reverse('core:dashboard')
        response = self.client.post(f'{self.login_url}?next={next_url}', {
            'username': 'user@test.com',
            'password': 'Test1234!',
        })
        self.assertRedirects(response, next_url)


class LogoutViewTest(TestCase):
    """Tests pour la vue de déconnexion"""
    
    def setUp(self):
        self.client = Client()
        self.logout_url = reverse('accounts:logout')
        self.user = User.objects.create_user(
            email='user@test.com',
            password='Test1234!',
            first_name='Test'
        )
        self.client.login(username='user@test.com', password='Test1234!')
    
    def test_logout_get_shows_confirmation(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/logout_confirm.html')
    
    def test_logout_post_success(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('accounts:home'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class PasswordResetTest(TestCase):
    """Tests pour la réinitialisation de mot de passe"""
    
    def setUp(self):
        self.client = Client()
        self.password_reset_url = reverse('accounts:password_reset')
        self.user = User.objects.create_user(
            email='user@test.com',
            password='Test1234!',
            first_name='Test'
        )
    
    def test_password_reset_page_loads(self):
        response = self.client.get(self.password_reset_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_reset.html')
    
    def test_password_reset_email_sent(self):
        response = self.client.post(self.password_reset_url, {
            'email': 'user@test.com',
        })
        self.assertEqual(response.status_code, 302)
        from django.core import mail
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Réinitialisation', mail.outbox[0].subject)


class HomeViewTest(TestCase):
    """Tests pour la page d'accueil"""
    
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('accounts:home')
    
    def test_home_page_loads(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/home.html')
    
    def test_home_shows_login_for_anonymous(self):
        response = self.client.get(self.home_url)
        self.assertContains(response, 'Connexion')
        self.assertContains(response, 'Inscription')
    
    def test_home_shows_dashboard_for_authenticated(self):
        user = User.objects.create_user(
            email='user@test.com',
            password='Test1234!',
            first_name='Test'
        )
        self.client.login(username='user@test.com', password='Test1234!')
        response = self.client.get(self.home_url)
        self.assertContains(response, 'Test')
        self.assertContains(response, 'tableau de bord')


class AxesLockoutTest(TestCase):
    """Tests pour vérifier le verrouillage Axes après plusieurs échecs"""

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('accounts:login')
        self.user = User.objects.create_user(
            email='locked@test.com',
            password='Valid1234!',
        )

    def tearDown(self):
        reset()

    def test_lockout_after_failed_attempts(self):
        for _ in range(5):  # AXES_FAILURE_LIMIT défini dans settings
            response = self.client.post(self.login_url, {
                'username': 'locked@test.com',
                'password': 'WrongPassword!',
            })
            self.assertEqual(response.status_code, 200)

        response = self.client.post(self.login_url, {
            'username': 'locked@test.com',
            'password': 'WrongPassword!',
        })

        self.assertTemplateUsed(response, 'accounts/account_locked.html')
        self.assertContains(response, "Votre compte a été verrouillé")

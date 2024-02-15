from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Policys, Claims


class YourAppViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_home_view(self):
        client = Client()
        client.login(username='testuser', password='testpassword')
        response = client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_signup_page(self):
        client = Client()
        response = client.post(reverse('signup'), {
            'firstname': 'Test',
            'lastname': 'User',
            'Username': 'testuser2',
            'email': 'test@example.com',
            'password': 'testpassword',
            'confirmpassword': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser2').exists())

    def test_login_page(self):
        User.objects.create_user(username='existinguser', password='testpassword')
        client = Client()
        response = client.post(reverse('login'), {'Name': 'existinguser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_logout_page(self):
        client = Client()
        client.force_login(self.user)
        response = client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_get_policy_view(self):
        policy = Policys.objects.create(
            user=self.user,
            holder_name='Test Holder',
            start_date='2024-01-01',
            end_date='2024-12-31',
            premuim=1000,
            coverage=5000,
            policy_type='health'
        )
        client = Client()
        client.force_login(self.user)
        response = client.get(reverse('get_policy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'policytable.html')
        self.assertContains(response, 'Test Holder')

    def test_get_claim_view(self):
        claim = Claims.objects.create(
            user=self.user,
            policy_number='00000000-0000-0000-0000-000000000001',
            status='Initiated',
            res_amt=1000,
            amt=500
        )
        client = Client()
        client.force_login(self.user)
        response = client.get(reverse('get_claim'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'claimtable.html')
        self.assertContains(response, '00000000-0000-0000-0000-000000000001')

    def test_create_claim_view(self):
        policy = Policys.objects.create(
            user=self.user,
            holder_name='Test Holder',
            start_date='2024-01-01',
            end_date='2024-12-31',
            premuim=1000,
            coverage=5000,
            policy_type='health'
        )
        client = Client()
        client.force_login(self.user)
        response = client.post(reverse('create_claim'), {'amt': 2000, 'policy_number': str(policy.policy_number)})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Claims.objects.filter(user=self.user, amt=2000, policy_number=policy.policy_number).exists())

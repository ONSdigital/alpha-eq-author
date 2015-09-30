from django.core.urlresolvers import reverse
from django.test.testcases import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def create_user(username, email, password):
    user = User.objects.create_user(username, email, password)
    user.save()
    return user

class LoginTest(TestCase):
    def test_unauthorized_access_to_protected_resource(self):
        # we get redirected to a login form when requesting a protected resource
        response = self.client.get(reverse('welcome'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('login' in response.url)

        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'username')


    def test_unsuccessful_login_attempt(self):
        # we get a login form when requesting a protected resource
        response = self.client.get(reverse('welcome'), follow=True)
        self.assertContains(response, 'username')

        login = self.client.login(username="invalid", password="IWillWork@Gattaca")

        self.assertFalse(login)

        response = self.client.get(reverse('welcome'), follow=True)
        self.assertContains(response, 'username')

    def test_successful_login(self):
        password = 'notANatural'
        user = create_user(username='user', email='valid@gattaca.com', password=password)

        login = self.client.login(username=user.username, password=password)

        self.assertTrue(login)

        response = self.client.get(reverse('welcome'), follow=True)
        self.assertContains(response, 'Surveys')
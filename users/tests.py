from django.test import TestCase

from users.models import User


# Create your tests here.


class UserCreationViewTestCase(TestCase):
    def setUp(self):
        pass

    def test_signup(self):
        data = {
            'email': 'testmail@mail.com',
            'password': 'testpass123',
        }
        response = self.client.post(
            '/users/signup/', data=data, content_type='application/json'
        )
        if User.objects.filter(email='testmail@mail.com').exists():
            self.assertEqual(response.status_code, 201)


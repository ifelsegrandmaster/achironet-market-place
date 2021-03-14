from django.test import TestCase, Client
from django.urls import reverse
from users.models import User
from agent.models import AgentProfile

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        # create a new user
        self.user = User.objects.create_user(
            email='johndoe@gmail.com',
            password='secretpass203',
            username='johndoe',
            is_superuser=True
        )
        # Now log in the test client
        password = "secretpass203"
        self.is_authenticated = self.client.login(
            username=self.user.username, password=password)

    # now test creating a new agent profile
    def test_create_agent_profile(self):
        url = reverse("agent:create-profile")
        response = self.client.post(
            url, {
                'first_name': 'John',
                'last_name': 'Doe',
                'phone_number': '+263782841339',
                'email': 'chaulapsx@gmail.com',
                'city': 'Gweru',
                'state': 'Midlands',
                'address': '4790 Mkoba 12'
            }
        )

        self.assertEquals(response.status_code, 302)



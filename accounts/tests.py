from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
    
    def test_profile_created(self):
        profile = self.user.profile
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.role, 'customer')

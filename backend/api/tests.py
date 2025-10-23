from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from .models import Publisher, Book 

User = get_user_model()

class PublisherTests(APITestCase):
    """
    Tests for the Publisher List/Create and Detail views.
    """
    def setUp(self):
        # 1. Create a regular user and an admin user for permission tests
        self.admin_user = User.objects.create_superuser('admin', 'admin@test.com', 'adminpass')
        self.regular_user = User.objects.create_user('user', 'user@test.com', 'userpass')

        # 2. Create initial data
        self.publisher1 = Publisher.objects.create(name='Example Publisher')
        self.publisher2 = Publisher.objects.create(name='Another Publisher')

        # 3. Define the URLs
        self.list_url = reverse('publisher-list')  
        self.detail_url = reverse('publisher-detail', kwargs={'pk': self.publisher1.pk})

    def test_list_publishers_unauthenticated(self):
        """
        Ensure unauthenticated users can view the publisher list (assuming AllowAny permission is default).
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_publisher_authenticated(self):
        """
        Ensure an authenticated user can create a publisher.
        """
        self.client.force_authenticate(user=self.regular_user)
        data = {'name': 'New Test Publisher'}
        response = self.client.post(self.list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Publisher.objects.count(), 3)
        self.assertEqual(response.data['name'], 'New Test Publisher')

    def test_update_publisher(self):
        """
        Ensure a publisher can be updated.
        """
        self.client.force_authenticate(user=self.admin_user)
        updated_name = 'Updated Publisher Name'
        data = {'name': updated_name}
        response = self.client.put(self.detail_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.publisher1.refresh_from_db()
        self.assertEqual(self.publisher1.name, updated_name)

    def test_delete_publisher_unauthenticated(self):
        """
        Ensure unauthenticated user cannot delete a publisher.
        """
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Publisher.objects.count(), 2)


# ----------------------------------------------------------------------

class AdminViewsTests(APITestCase):
    """
    Tests for the UserViewSet and GroupViewSet which require IsAdminUser permission.
    """
    def setUp(self):
        self.admin_user = User.objects.create_superuser('admin', 'admin@test.com', 'adminpass')
        self.regular_user = User.objects.create_user('user', 'user@test.com', 'userpass')
        
        # NOTE: Djoser often exposes users as 'users' or 'auth/users'
        self.user_list_url = reverse('user-list') 

    def test_list_users_as_admin(self):
        """
        Ensure admin can list users.
        """
        # Log in the admin user using the force_authenticate helper
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should contain at least the admin and regular user
        self.assertTrue(len(response.data) >= 2) 

    def test_list_users_as_regular_user(self):
        """
        Ensure regular user cannot list users due to IsAdminUser permission.
        """
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.user_list_url)
        # IsAdminUser permission blocks non-admin users
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) 

    def test_list_users_unauthenticated(self):
        """
        Ensure unauthenticated access is rejected (401).
        """
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
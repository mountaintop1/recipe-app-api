"""
Test models
"""
from unittest.mock import patch
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email='user@example.com', password='test123'):
    """
    Create and return a sample user
    """
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """
    Test models
    """
    def test_create_user_with_email_successful(self):
        """
        Test creating a new user with an email is successful
        """
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email, password=password
            )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        sample_email = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected_email in sample_email:
            user = get_user_model().objects.create_user(
                email=email, password='test123')
            self.assertEqual(user.email, expected_email)

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None, password='test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com', 'test123'
            )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test creating a recipe object successfully"""
        user = get_user_model().objects.create_user(
            'test@example.com', 'test123'
            )
        recipe = models.Recipe.objects.create(
                            user=user,
                            title='Sample recipe name',
                            time_minutes=5,
                            price=Decimal('5.50'),
                            description='Sample recipe description',
                            )
        self.assertEqual(recipe.user, user)
        self.assertEqual(recipe.title, 'Sample recipe name')
        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Test creating a tag object successfully"""
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='Tag1')

        self.assertEqual(tag.user, user)
        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        """Test creating an ingredient object successfully"""
        user = create_user()
        ingredient = models.Ingredient.objects.create(
            user=user, name='Ingredient1')

        self.assertEqual(ingredient.user, user)
        self.assertEqual(str(ingredient), ingredient.name)

    @patch('core.models.uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test generating image path for recipe"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        expected_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, expected_path)

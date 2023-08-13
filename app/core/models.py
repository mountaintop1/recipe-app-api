"""
Database models
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin


class UserManager(BaseUserManager):
    """User manager"""
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)  # using=self._db is required by Django
        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True  # is_staff is created by PermissionsMixin
        user.is_superuser = True  # is_superuser is created by PermissionsMixin
        user.save(using=self._db)  # using=self._db is required by Django
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'  # USERNAME_FIELD is required by Django


class Recipe(models.Model):
    """Recipe object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # settings.AUTH_USER_MODEL is required by Django
        on_delete=models.CASCADE  # on_delete=models.CASCADE is required by Django
        )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)  # blank=True means this field is optional
    #  ingredients = models.ManyToManyField('Ingredient')  # 'Ingredient' is a string because Ingredient is defined below
    #  tags = models.ManyToManyField('Tag')

    def __str__(self):
        """Return string representation of the recipe"""
        return str(self.title)

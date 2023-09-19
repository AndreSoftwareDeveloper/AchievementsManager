from django.db import models
from django.contrib.auth.models import AbstractUser
import bcrypt


class User(AbstractUser):
    nick = models.CharField(max_length=50)
    email = models.CharField(max_length=50, default="debug@debug.com")
    encrypted_password = models.TextField()
    npsso_token = models.CharField(max_length=64, default="")

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    @staticmethod
    def encrypt_password(raw_password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

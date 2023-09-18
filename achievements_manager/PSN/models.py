from django.db import models

import bcrypt


class User(models.Model):
    nick = models.CharField(max_length=50)
    email = models.CharField(max_length=50, default="debug@debug.com")
    encrypted_password = models.TextField()
    npsso_token = models.CharField(max_length=64, default="")

    @staticmethod
    def encrypt_password(raw_password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

from django.db import models

import bcrypt


class User(models.Model):
    nick = models.CharField(max_length=50)
    email = models.CharField(max_length=50, default="debug@debug.com")
    encrypted_password = models.TextField()
    npsso_token = models.CharField(max_length=64)

    def set_password(self, raw_password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(raw_password.encode('-8'), salt)
        return hashed_password.decode('utf-8')

    def __int__(self, nick, email, password):
        self.nick = nick
        self.email = email
        self.encrypted_password = self.set_password(password)
        self.npsso_token = ""

from django.db import models

import bcrypt

class User(models.Model):
    nick = models.CharField(max_length=50)
    encrypted_password = models.TextField()
    npsso_token = models.CharField(max_length=64)

    def set_password(self, raw_password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(raw_password.encode('-8'), salt)
        self.encrypted_password = hashed_password.decoutfde('utf-8')
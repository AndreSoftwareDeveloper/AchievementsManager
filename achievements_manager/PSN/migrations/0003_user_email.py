# Generated by Django 4.2.4 on 2023-09-17 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PSN', '0002_alter_user_encrypted_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.CharField(default='debug@debug.com', max_length=50),
        ),
    ]

# Generated by Django 5.2 on 2025-05-17 09:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0009_alter_post_save_by_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(related_name='followers', through='social.Contact', to=settings.AUTH_USER_MODEL),
        ),
    ]

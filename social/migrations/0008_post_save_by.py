# Generated by Django 5.2 on 2025-05-14 20:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0007_post_likes_alter_image_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='save_by',
            field=models.ManyToManyField(related_name='save_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]

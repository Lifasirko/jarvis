# Generated by Django 5.0.7 on 2024-07-22 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_customuser_storage_limit'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/'),
        ),
    ]
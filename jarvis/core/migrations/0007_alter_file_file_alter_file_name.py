# Generated by Django 5.0.7 on 2024-07-22 18:16

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_file_name_file_uploaded_at_alter_file_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to=core.models.user_directory_path),
        ),
        migrations.AlterField(
            model_name='file',
            name='name',
            field=models.CharField(default='Untitled', max_length=255),
        ),
    ]

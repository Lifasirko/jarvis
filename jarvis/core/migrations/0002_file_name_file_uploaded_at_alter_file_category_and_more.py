# Generated by Django 5.0.7 on 2024-07-22 18:44

import core.models
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='name',
            field=models.CharField(default='Untitled', max_length=255),
        ),
        migrations.AddField(
            model_name='file',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='file',
            name='category',
            field=models.CharField(choices=[('image', 'Image'), ('document', 'Document'), ('video', 'Video'), ('other', 'Other')], max_length=50),
        ),
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to=core.models.user_directory_path),
        ),
    ]

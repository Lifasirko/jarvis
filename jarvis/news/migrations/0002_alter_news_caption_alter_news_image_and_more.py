# Generated by Django 5.0.7 on 2024-07-26 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='caption',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.URLField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='image_caption',
            field=models.TextField(null=True),
        ),
    ]

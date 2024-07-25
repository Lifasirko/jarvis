# Generated by Django 5.0.7 on 2024-07-26 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.URLField(max_length=255, unique=True)),
                ('title', models.TextField(unique=True)),
                ('caption', models.TextField()),
                ('category', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('author', models.CharField(max_length=255)),
                ('image', models.URLField(max_length=255)),
                ('image_caption', models.TextField()),
                ('published_time', models.DateTimeField(null=True)),
            ],
        ),
    ]

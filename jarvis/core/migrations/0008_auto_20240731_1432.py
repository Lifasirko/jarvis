from django.db import migrations

from jarvis.config.settings import SOCIAL_AUTH_GOOGLE_OAUTH2_KEY, SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET


def create_site_and_social_app(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    SocialApp = apps.get_model('socialaccount', 'SocialApp')

    site, created = Site.objects.update_or_create(
        id=1,
        defaults={'domain': '127.0.0.1:8000', 'name': 'localhost:8000'}
    )
    if created:
        print("Site created")
    else:
        print("Site updated")

    SocialApp.objects.update_or_create(
        provider='google',
        defaults={
            'name': 'Google',
            'client_id': SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
            'secret': SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
            'sites': [site]
        }
    )


class Migration(migrations.Migration):
    # dependencies = [
    #     ('sites', '0007_profile_remove_contact_user_delete_news_and_more'),  # Залежить від вашої структури міграцій
    #     ('socialaccount', '0008_auto_20240731_1432'),  # Залежить від вашої структури міграцій
    # ]

    operations = [
        migrations.RunPython(create_site_and_social_app),
    ]

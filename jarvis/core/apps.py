from allauth.socialaccount.models import SocialApp
from django.apps import AppConfig
from django.contrib.sites.models import Site
from django.db.models.signals import post_migrate

from jarvis.config.settings import SOCIAL_AUTH_GOOGLE_OAUTH2_KEY, SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        post_migrate.connect(create_site_and_social_app, sender=self)


def create_site_and_social_app(sender, **kwargs):
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

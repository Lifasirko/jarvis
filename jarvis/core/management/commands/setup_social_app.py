from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp


class Command(BaseCommand):
    help = 'Set up site and Google social app'

    def handle(self, *args, **kwargs):
        site, created = Site.objects.get_or_create(id=1)
        if created:
            site.domain = settings.SITE_URL
            site.name = settings.SITE_URL
            site.save()
        else:
            if site.domain != settings.SITE_URL or site.name != settings.SITE_URL:
                site.domain = settings.SITE_URL
                site.name = settings.SITE_URL
                site.save()

        social_app, created = SocialApp.objects.get_or_create(provider='google')
        if created:
            social_app.name = settings.SOCIAL_ACC_NAME
            social_app.client_id = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
            social_app.secret = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET
            social_app.save()
            social_app.sites.add(site)
        else:
            updated = False
            if social_app.name != settings.SOCIAL_ACC_NAME:
                social_app.name = settings.SOCIAL_ACC_NAME
            if social_app.client_id != settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY:
                social_app.client_id = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
                updated = True
            if social_app.secret != settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET:
                social_app.secret = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET
                updated = True
            if updated:
                social_app.save()
            if site not in social_app.sites.all():
                social_app.sites.add(site)

        self.stdout.write(self.style.SUCCESS('Successfully set up site and Google social app'))

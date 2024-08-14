from django import template
from urllib.parse import urlparse

register = template.Library()

@register.filter
def get_domain(url):
    return urlparse(url).netloc
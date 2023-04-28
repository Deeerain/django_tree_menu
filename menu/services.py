from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from .models import MenuItem


def get_menu_items_by_menu_name(name: str):
    return MenuItem.objects.filter(menu__menu_name=name).values(
        'id', 'item_title', 'item_url', 'item_parent')


def reverse_url(url: str) -> str:
    try:
        url = reverse(url)
    except NoReverseMatch:
        pass

    if not url.startswith('/'):
        url = '/' + url

    return url

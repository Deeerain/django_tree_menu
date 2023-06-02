from typing import Any
import logging

from django import template

from menu.models import MenuItem

register = template.Library()
logger = logging.getLogger(__name__)


@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, menu_name: str) -> dict[str, Any]:
    objects = MenuItem.objects.filter(menu__menu_name=menu_name,
                                      item_parent=None)\
        .prefetch_related('parents')

    return {
        "menu_items": objects
    }

from typing import Generator, Any, Dict, List
import logging

from django import template
from django.db import connection

from ..services import get_menu_items_by_menu_name, reverse_url


register = template.Library()
logger = logging.getLogger(__name__)


class MenuNode:
    def __init__(self, id, title, url: str, parent, *,
                 ref_parent: 'MenuNode' = None) -> None:
        self.id: int = id
        self.title: str = title
        self._url: str = url
        self.parent: int = parent
        self.ref_parent: 'MenuNode' = ref_parent
        self._tree: 'MenuTree'
        self.collapse: bool = True

    @property
    def childrens(self) -> Generator['MenuNode', Any, Any]:
        for item in self._tree.nodes:
            if item.parent == self.id:
                yield item

    @property
    def url(self) -> str:
        url = reverse_url(self._url)

        return url

    def set_active(self) -> None:
        self.collapse = False

        if self.ref_parent is not None:
            self.ref_parent.set_active()

    def is_parent(self, value: 'MenuNode') -> bool:
        return self.id == value.parent


class MenuTree:
    def __init__(self) -> None:
        self.nodes: list[MenuNode] = []

    @property
    def root_nodes(self) -> Generator['MenuNode', Any, Any]:
        for node in self.nodes:
            if node.parent is None:
                yield node

    def get_parent(self, node: 'MenuNode') -> (MenuNode | None):
        for node_item in self.nodes:
            if node_item.is_parent(node):
                return node_item

    def add_children(self, node: MenuNode) -> MenuNode:
        node._tree = self
        node.ref_parent = self.get_parent(node)
        self.nodes.append(node)
        return node


def make_tree(items: List[Dict[str, Any]]) -> MenuTree:
    tree = MenuTree()

    for menu_item in items:
        tree.add_children(MenuNode(
            id=menu_item.get('id'),
            title=menu_item.get('item_title'),
            url=menu_item.get('item_url'),
            parent=menu_item.get('item_parent')
        ))

    return tree


def set_active_item(tree: MenuTree, url: str):
    for node in tree.nodes:
        if node.url == url:
            node.set_active()
            break


@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, menu_name: str) -> dict[str, Any]:

    curent_url = context['request'].get_full_path()
    menu_items = get_menu_items_by_menu_name(menu_name)
    menu_tree = make_tree(menu_items)

    set_active_item(menu_tree, curent_url)

    logger.debug('Requests when drawing the \
                 menuRequests when drawing the menu: %s',
                 len(connection.queries))

    return {
        "current_url": curent_url,
        "menu_tree": menu_tree
    }

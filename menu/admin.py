from django.contrib import admin
from .models import Menu, MenuItem


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    ordering = ('item_parent',)
    extra = 1


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'menu_name')
    search_fields = ['menu_name', 'url']
    list_filter = ['menu_name']
    inlines = (MenuItemInline,)


@admin.register(MenuItem)
class MenuItem(admin.ModelAdmin):
    list_display = ('id', 'item_title', 'item_url', 'menu')
    list_filter = ('menu__menu_name',)
    search_fields = ('menu__name', 'item_url', 'item_title')
    list_editable = ('item_title',)

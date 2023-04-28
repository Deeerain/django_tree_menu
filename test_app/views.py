from django.shortcuts import render


def index(request, menu_name=None, menu_item_title=None):
    return render(request, 'index.html',
                  context={'menu_name': menu_name,
                           'menu_item_title': menu_item_title})

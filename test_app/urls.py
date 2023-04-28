from django.urls import path
from .views import index
from menu.models import MenuItem

urlpatterns = [
    path("<str:menu_name>/<str:menu_item_title>/", index, name='home'),
    path("", index, name='home'),
]

for menu_items in MenuItem.objects.all():
    urlpatterns.append(path(menu_items.url, index))

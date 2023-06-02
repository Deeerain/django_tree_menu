from django.urls import path

from test_app import views

from menu.models import MenuItem

urlpatterns = [
    path("<str:menu_name>/<str:menu_item_title>/",
         views.HomePageView.as_view(), name='home'),
    path("", views.HomePageView.as_view(), name='home'),
]

for menu_items in MenuItem.objects.all():
    urlpatterns.append(path(menu_items.item_url, views.HomePageView.as_view()))

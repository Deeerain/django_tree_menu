from django.db import models


class Menu(models.Model):
    menu_name = models.CharField("Название", max_length=100, unique=True,
                                 default='main_menu')

    class Meta:
        verbose_name = "Меню"
        verbose_name_plural = "Меню"


class MenuItem(models.Model):
    item_title = models.CharField("Название", max_length=100)
    item_url = models.CharField("Ссылка", max_length=255, unique=True)
    item_parent = models.ForeignKey(verbose_name='Родитель', to='self',
                                    on_delete=models.SET_DEFAULT, null=True,
                                    blank=True, default=None,
                                    related_name='parents')
    menu = models.ForeignKey(verbose_name="Меню", to=Menu,
                             on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Пункт меню"
        verbose_name_plural = "Пункты меню"

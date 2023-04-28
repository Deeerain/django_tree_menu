from django.db import models


class AbstactMenuBase(models.Model):
    NAME_FIELD = 'menu_name'

    @property
    def name(self) -> str:
        return getattr(self, self.NAME_FIELD)

    def __str__(self) -> str:
        return self.name

    class Meta:
        abstract = True


class AbstractMenuItemBase(models.Model):
    TITLE_FIELD = 'item_title'
    URL_FIELD = 'item_url'

    @property
    def title(self) -> str:
        return getattr(self, self.TITLE_FIELD)

    @property
    def url(self) -> str:
        return getattr(self, self.URL_FIELD)

    def __str__(self) -> str:
        return self.url

    class Meta:
        abstract = True


class Menu(AbstactMenuBase):
    menu_name = models.CharField("Название", max_length=100, unique=True,
                                 default='main_menu')

    class Meta:
        verbose_name = "Меню"
        verbose_name_plural = "Меню"


class MenuItem(AbstractMenuItemBase):
    item_title = models.CharField("Название", max_length=100)
    item_url = models.CharField("Ссылка", max_length=255, unique=True)
    item_parent = models.ForeignKey(verbose_name='Родитель', to='self',
                                    on_delete=models.SET_DEFAULT, null=True,
                                    blank=True, default=0)
    menu = models.ForeignKey(verbose_name="Меню", to=Menu,
                             on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Пункт меню"
        verbose_name_plural = "Пункты меню"

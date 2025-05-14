from django.db import models
from django.urls import reverse, NoReverseMatch
from django.utils.translation import gettext_lazy

class MenuItem(models.Model):
    name = models.CharField(
        gettext_lazy('Название меню'), max_length=100
    )
    menu_name = models.CharField(
        'Название меню',
        max_length=50,
        help_text='Имя меню, к которому относится этот пункт'
    )
    named_url = models.CharField(
        'Именованный URL',
        max_length=100,
        blank=True,
        help_text='Именованный URL из urls.py'
    )
    url = models.CharField(
        'Явный URL',
        max_length=200,
        blank=True,
        help_text='Явный URL (если нет named URL)'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name = 'Родительский пункт меню'
    )
    order = models.PositiveIntegerField(
        'Порядок стортировки', default=0
    )

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_url(self):
        """Фнукция возврата named url или явного url"""
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                return self.named_url
        return self.url or '#'

    def is_active(self, current_url):
        """Определение активного меню"""
        return current_url == self.get_url()

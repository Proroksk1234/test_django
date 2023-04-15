from django.core.exceptions import ValidationError
from django.db import models

from .utils import slugify


class MenuModel(models.Model):
    name_menu = models.CharField(max_length=30, verbose_name='Название меню', null=False, blank=False)
    top_menu = models.ForeignKey('self', verbose_name='Пункт предыдущего меню', on_delete=models.CASCADE,
                                 blank=True, null=True)
    position = models.IntegerField(blank=False, null=False, verbose_name='Позиция вложенности')
    url = models.TextField(null=False, unique=True, db_index=True, verbose_name='URL')
    objects = models.Manager()

    class Meta:
        verbose_name = 'Меню сайта'
        verbose_name_plural = 'Меню сайта'
        ordering = ['id']

    def save(self, *args, **kwargs):
        """
        Метод валидации и сохранения объекта меню.

        Описание:
        1) Сохранение модели происходит через название меню.
        2) Предыдущее меню берется либо из админ панели по связи, либо из тега
        3) Позиция вложенности выбираеся с учетом вложенности предыдущего меню из звена.
        Если предыдущее меню отсутствует, позиция вложенности: 0
        4) Создается URL адрес по данному принципу:
            a) Если позиция вложенности 0, тогда URL создается по принципу: / + slugify(name_menu) + /
            б) Если позиция вложенности больше 1, тогда URL создается по принципу: старый URL + slugify(name_menu) + /

        Основная валидация:
        1) Максимальная вложенность меню равна 5
        2) Минимальная длина имени 1 символ. Символы & и / не считаются. Они исключаются их имени
        3) Максимальная длина имени 30 символов. Символы & и / не считаются. Они исключаются их имени
        4) Вложенность списка после создания изменить невозможно
        5) URL должен быть уникальным. Не может быть в 1 вложенном списке на одном
        и том же уровне 2 одинаковых по имени меню
        6) Единственное исключение: Если обновляется через админ панель объект.
        Тогда валидация на проверку URL отсутствует

        Если какая-лио валидация не проходит, вызывается исключение ValidationError


        """
        if len(str(self.url).split('&')) >= 5:
            raise ValidationError('Достигнута максимальная вложенность')
        if self.id:
            old_menu = MenuModel.objects.get(id=self.id)
            self.top_menu = old_menu.top_menu
        else:
            old_menu = None
        self.name_menu = self.name_menu.replace('&', '').replace('/', '')
        if len(self.name_menu) == 0 or len(self.name_menu) > 30:
            raise ValidationError(
                'Неверная длина введенного имени. Она должна быть не менее 1 символа и не более 30 символов;'
                'Символы & и / в имени не допускаются')
        if self.top_menu:
            self.position = self.top_menu.position + 1
            self.url = self.top_menu.url + f'&{slugify(name_menu=self.name_menu)}'
        else:
            self.position = 0
            self.url = f'{slugify(name_menu=self.name_menu)}'
        obj = MenuModel.objects.filter(url=self.url).values()
        if obj:
            if old_menu:
                if old_menu.id != obj[0]['id']:
                    raise ValidationError('Данное имя в данном вложенном меню уже существует!!!')
            else:
                raise ValidationError('Данное имя в данном вложенном меню уже существует!!!')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Название меню: {self.name_menu}; уровень вложенности: {self.position}'

from django import template
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from ..models import MenuModel
from ..sort_menu import create_sort_menu

register = template.Library()


@register.simple_tag(name='draw_menu')
def draw_menu(name_menu, url):
    """
    Тег создания меню по названию

    name_menu - название добавляемого меню
    url - url адрес, на который происходит переход

    Описание:
    1) Если имя меню не введено, тег пропускается
    2) Происходит получение предыдущего меню в звене по url:
        а) Если url пустой, т.е. добавление меню происходит с главной страницы, предыдущее меню принимает значение None
        б) Если url адрес не пустой, тогда происходит получение объекта предыдущего меню:
            a) Если объект обннаруживается, предыдущее меню равняется этому объекту
            б) Иначе вызывается исключение ValidationError
    3) Вызов метода создания и сохранения нового объекта по имени нового меню и обхекту предыдущего меню

    """
    if name_menu:
        if url != '':
            try:
                top_menu = MenuModel.objects.get(url=url)
            except ObjectDoesNotExist:
                raise ValidationError('Неверный url адрес')
        else:
            top_menu = None
        MenuModel.objects.create(name_menu=name_menu, top_menu=top_menu)
    return ''


@register.inclusion_tag('app_django/form.html', name='get_form')
def get_form(url, form):
    """
    Тег отображения формы

    url - url адрес, на который происходит переход
    form - объект формы

    Описание:
    1) Если длина url больше 5, отображения формы не происходит
    2) Иначе происходит отображение формы в html

    """
    list_url = url.split('&')
    if len(list_url) < 5 >= 0:
        return {'form': form}
    return None


@register.inclusion_tag('app_django/menu.html', name='get_menu')
def get_menu(url):
    """
    Тег получения всего списка меню с учетом url адреса

    url - url адрес, на который происходит переход

    Описание:
    1) Получение объектов меню:
        a) Объекты отсортированны по позиции вложения и id
        б) Отфильтрованы по длине url, т.е. позиция вложения должна быть равна или меньше списка разбитого url по &
    2) Происходит проверка url. Если в полученных объектах меню нет данного url, и url не равен пустому списку,
    вфзфвается исключение ValidationError
    3) Если после проверки url, список Queryset объектов равен None, возвращает None в меню-шаблон
    4) Иначе происходит метод создания отсортированного вложенного списка меню и возвращение его в меню-шаблон

    """
    list_url = url.split('&')
    menu = MenuModel.objects.all().order_by("position", "id").values().filter(position__lte=len(list_url))
    for count, x in enumerate(menu):
        if x['url'] == url:
            break
    else:
        if url != '':
            raise ValidationError("Неверный url адрес")
    if menu is None:
        return {'menu': None}
    sort_menu = create_sort_menu(menu=menu, list_url=list_url)
    return {'sort_menu': sort_menu}

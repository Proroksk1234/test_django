from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.views import View

from .forms import PostMenuForm


class GetCreateMenu(View):

    def get(self, request, url=''):
        """
        Вызов метода GET

        Возвращает в шаблон home.html url адрес, на который происходит переход, форму ввода и name_menu в значении None,
        чтобы не вызывался метод создания объекта меню

        """

        form = PostMenuForm()
        return render(request, 'app_django/home.html', context={'url': url, 'form': form, 'name_menu': None})

    def post(self, request, url=''):
        """
        Метод создания меню по названию через форму в html шаблоне

        Описание:
        Происходит получение данных из формы и проверятся их валидность
        Если данные не валидны, вызывается исключение ValidationError
        Возвращает в шаблон home.html url адрес, на который происходит переход, форму ввода и name_menu

        """
        form = PostMenuForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            name_menu = form_data['name_menu'].replace('&', '').replace('/', '')
            if len(name_menu) == 0:
                raise ValidationError("Введено неверное по размеру имя в форме")
            return render(request, 'app_django/home.html',
                          context={'url': url, 'form': form, 'name_menu': name_menu})
        raise ValidationError("Введено неверное по размеру имя в форме")

from django import forms

name_regex = r'^[-0-9A-Za-zА-Яа-я *!@#$%()"№;%:?]{1,30}$'


class PostMenuForm(forms.Form):
    """
    Форма ввода имени меню

    Валидация формы происходит через регулярное выражение.
    Максимальная длина: 30 символов, минимальная: 1 символ

    """
    name_menu = forms.CharField(max_length=30, min_length=1, label='Название меню', widget=forms.TextInput(
        attrs={'placeholder': 'Введите название добавляемого меню', 'required pattern': name_regex,
               'oninvalid': "this.setCustomValidity('Введите корректные значения')",
               'oninput': "setCustomValidity('')"}))

def create_sort_menu(menu, list_url):
    """
    Метод создания отсортированного вложенного списка меню

    menu - отсортированный по позиции и id список объектов меню с базы данных
    list_url - список разбитого url адреса по &

    1) Запуск цикла по пробежке по каждому из объектов меню
    2) Создание словаря из объекта меню. next_position является списком, куда будет вкладываться вложенное меню
    3) Если вложенное меню отсутствует, происходит добавление в список sort_menu (список отсортированного меню)
    4) Иначе происходит вызов рекурсионного метода добавления вложенного меню
    5) После выполнения цикла, возращается отсортированное меню

    """
    sort_menu = []
    for _ in menu:
        one_menu = {'id': _['id'], 'name_menu': _['name_menu'], 'url': _['url'], 'position': _['position'],
                    'top_menu_id': _['top_menu_id'], 'next_position': []}
        if one_menu['top_menu_id'] is None:
            sort_menu.append(one_menu)
        else:
            sort_menu = next_position_add(sort_menu=sort_menu, one_menu=one_menu, list_url=list_url)
    return sort_menu


def next_position_add(sort_menu, one_menu, list_url):
    """
    Рекурсионный метод добавления вложенного меню

    sort_menu - уже отсортированный на данный момент список меню
    one_menu - добавляемый словарь меню
    list_url - список разбитого url адреса по &

    1) Запуск цикла по пробежке по каждому из добавленному меню
    2) Если id добавленного меню, равен id в словаре, тогда происходит проверка на то,
    чтобы list_url равнялся до индекса позиции словаря меню совпадал с разбитым url адресом словаря меню по индексу
    3) Если совпадает, словарь добавляется в список sort_menu в ключ [next_position] и цикл прерывается
    4) Если id добавленного меню, не равен id в словаре, тогда проверяется вложенность добавленного в список меню
    5) Если она присутствует, вызывается рекурсия, иначе цикл продолжает выполняться
    6) Когда цикл выполнился, возвращается отсортированное меню

    """
    for count, y in enumerate(sort_menu):
        if y['id'] == one_menu['top_menu_id']:
            for x in range(one_menu['position']):
                if list_url[x] != one_menu['url'].split('&')[x]:
                    break
            else:
                sort_menu[count]['next_position'] = sort_menu[count]['next_position'] + [one_menu]
                break
        if sort_menu[count]['next_position']:
            sort_menu[count]['next_position'] = next_position_add(
                sort_menu=sort_menu[count]['next_position'], one_menu=one_menu, list_url=list_url)
    return sort_menu

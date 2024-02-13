import json
from typing import List, Dict

COMMANDS = {
    1: 'Вывод всех записей',
    2: 'Добавление новой записи',
    3: 'Редактировать запись',
    4: 'Поиск записи',
    0: 'Выход',
}


def read_file() -> List:
    """
    Чтение данных из файла 'data.json'

    Returns:
        Список записей из файла или пустой список, если файл не найден или произошла ошибка при чтении
    """
    try:
        with open(file='data.json', mode='r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("Файл data.json не найден. Создайте файл или добавьте данные.")
        return []
    except json.JSONDecodeError:
        print("Ошибка при чтении файла. Проверьте формат JSON.")
        return []


def save_to_file(data: List) -> None:
    """
    Сохранение данных в файл 'data.json'

    Args:
        data: Все записи, сохранение происходит в послеюнюю очередь
    """
    with open(file='data.json', mode='w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def show_page(page_num: int, data: Dict) -> None:
    """
    Вывод данных на экран постранично

    Args:
        page_num: Номер страницы
        data: Словарь страниц с записями

    """
    print(f'Введите номер страницы или 0 для выхода. Всего страниц - {page_num}')
    user_input = None

    while user_input != 0:
        user_input = int(input())
        count = 1

        if user_input in range(1, page_num + 1):
            for record in data[user_input]:
                print(f'Страница - {user_input}, номер записи - {count}')
                for key, value in record.items():
                    if key == "id":
                        continue
                    print(f'{key}: {value}')
                print('---------------------------------')
                count += 1
        else:
            print('Нет такой страницы')


def paginate_data(data: List) -> None:
    """
    Разбивка данных на страницы

    Args:
        data: Список записей для пагинации

    """
    count_on_page = 4
    # число элементов на странице

    total_records = len(data)

    while True:
        pages = {}
        key = 0
        count = 1
        records_on_page = []

        while key < total_records:
            records_on_page.append(data[key])

            if (key + 1) % count_on_page == 0:
                pages[count] = records_on_page
                count += 1
                records_on_page = []
            key += 1

        if records_on_page:
            pages[count] = records_on_page

        return show_page(count, pages)


def search_records(data: List) -> None:
    """
    Поиск записей по заданным критериям

    Args:
        data: Список записей, в котором происходит поиск
    """
    search_criteria = {}

    print("Введите параметры поиска (оставьте пустым, чтобы пропустить):")
    search_criteria["Фамилия"] = input("Фамилия: ")
    search_criteria["Имя"] = input("Имя: ")
    search_criteria["Отчество"] = input("Отчество: ")
    search_criteria["Организация"] = input("Организация: ")
    search_criteria["Рабочий_телефон"] = input("Рабочий телефон: ")
    search_criteria["Сотовый_телефон"] = input("Сотовый телефон: ")

    matched_records = []

    for record in data:
        if all(record[key] == value or not value for key, value in search_criteria.items()):
            matched_records.append(record)

    if matched_records:
        print("Найденные записи:")
        for matched_record in matched_records:
            print(matched_record)
    else:
        print("Записи не найдены.")


def del_rec(data: List, id: int) -> List:
    """
    Удаление записи по заданному id

    Args:
        data: Список записей
        id: id

    Returns:
        List: Обновленный список записей
    """
    del data[id - 1]
    return data


def edit_record(data: List) -> List:
    """
    Редактирование или удаление записи по выбору пользователя

    Args:
        data: Список записей

    Returns:
        List: Обновленный список записей
    """
    user_input = None
    id_to_edit = None
    while True:
        id_to_edit = int(input('Введите id записи, которую хотите редактировать или 0, чтобы вернуться назад '))

        if 0 < id_to_edit <= len(data):
            break
        else:
            print('Неверный id')

    while id_to_edit != 0:
        print('1 Редактирование записи')
        print('2 Удаление записи')
        print('0 Назад')

        user_input = int(input())
        if user_input == 1:
            record_to_edit = data[id_to_edit - 1]

            for key in record_to_edit:
                if key == 'id':
                    continue
                print(f'{key}:')
                record_to_edit[key] = input()
            return data
        elif user_input == 2:
            return del_rec(data, id_to_edit)
        else:
            print('Неверная опция')

    return data


def add_new_record(data: List) -> List:
    """
    Добавление новой записи в справочник

    Args:
        data: Список записей

    Returns:
        List: Обновленный список записей
    """
    new_record = {
        "id": data[-1]["id"] + 1,
        "Фамилия": input("Введите фамилию "),
        "Имя": input("Введите имя "),
        "Отчество": input("Введите отчество "),
        "Организация": input("Введите организацию "),
        "Рабочий_телефон": input("Введите рабочий телефон "),
        "Сотовый_телефон": input("Введите сотовый телефон "),
    }
    data.append(new_record)
    return data


def main() -> None:
    """
    Основная функция программы

    Запускает взаимодействие с пользователем и обрабатывает команды
    """
    data = read_file()
    user_choice = None

    while user_choice != 0:
        for key, value in COMMANDS.items():
            print(key, value)

        print('Введите номер опции: ', end='')
        user_choice = int(input())

        if user_choice not in range(0, 5):
            print('Неправильно введена цифра...')
        elif user_choice == 1:
            paginate_data(data)
        elif user_choice == 2:
            data = add_new_record(data)
        elif user_choice == 3:
            data = edit_record(data)
        elif user_choice == 4:
            search_records(data)
    save_to_file(data)


if __name__ == "__main__":
    main()

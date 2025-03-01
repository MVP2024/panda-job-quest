from typing import List, Dict, Any

from api.hh_api import HeadHunterAPI
from models.vacancy import Vacancy
from storage.json_storage import JSONStorage



def display_vacancies(vacancies: List[Vacancy]) -> None:
    """
    Вывод информации о вакансиях

    :param vacancies: Список вакансий для отображения
    """
    if not vacancies:
        print("Вакансии не найдены.")
        return

    for vacancy in vacancies:
        print(f"Название: {vacancy.title}")
        print(f"Зарплата: {vacancy.salary}")
        print(f"URL: {vacancy.url}")
        print(f"Описание: {vacancy.description}")
        print("---")



def main_menu() -> None:
    """
    Главное меню взаимодействия с пользователем
    """
    from api.hh_api import HeadHunterAPI
    from storage.json_storage import JSONStorage
    from models.vacancy import Vacancy

    api = HeadHunterAPI()
    storage = JSONStorage()

    while True:
        print("\n--- Поиск вакансий ---")
        print("1. Найти вакансии")
        print("2. Показать топ вакансий")
        print("3. Найти по ключевому слову")
        print("4. Выйти")

        choice = input("Выберите действие: ")

        try:
            if choice == '1':
                query = input("Введите поисковый запрос: ")
                vacancies_data = api.get_vacancies(query)

                # Преобразование данных API в объекты Vacancy
                vacancies = [
                    Vacancy(
                        title=vacancy['name'],
                        url=vacancy.get('alternate_url', ''),
                        salary=vacancy.get('salary', {}),
                        description=vacancy.get('snippet', {}).get('requirement', 'Описание отсутствует')
                    ) for vacancy in vacancies_data
                ]

                # Сохранение вакансий
                for vacancy in vacancies:
                    storage.add_vacancy(vacancy)

                print(f"Найдено и сохранено {len(vacancies)} вакансий")
                display_vacancies(vacancies)

            elif choice == '2':
                # Показать топ вакансий
                top_n = int(input("Сколько вакансий показать? "))
                all_vacancies = storage.get_vacancies()

                # Сортировка по зарплате
                sorted_vacancies = sorted(
                    [Vacancy(**v) for v in all_vacancies],
                    key=lambda x: x.salary or 0,
                    reverse=True
                )[:top_n]

                display_vacancies(sorted_vacancies)

            elif choice == '3':
                # Поиск по ключевому слову
                keyword = input("Введите ключевое слово: ")

                # Получение вакансий и преобразование в объекты Vacancy
                found_vacancies = storage.get_vacancies({'title': keyword})

                if not found_vacancies:
                    # Если по заголовку не нашли, ищем в описании
                    found_vacancies = storage.get_vacancies({'description': keyword})

                filtered_vacancies = [
                    Vacancy(**v) for v in found_vacancies
                ]

                display_vacancies(filtered_vacancies)

            elif choice == '4':
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

        except ValueError as e:
            print(f"Ошибка ввода: {e}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


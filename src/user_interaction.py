import os
import sys
from typing import List

from api.hh_api import HeadHunterAPI
from logger.logger import setup_logger
from models.vacancy import Vacancy
from storage.json_storage import JSONStorage

# Добавляем путь к корневой директории проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Настройка логгера
logger = setup_logger(__name__)


def display_vacancies(vacancies: List[Vacancy], brief_mode: bool = False) -> None:
    """
    Вывод информации о вакансиях

    :param vacancies: Список вакансий для отображения
    :param brief_mode: Краткий режим отображения (по умолчанию False)
    """
    logger.info(f"Отображение вакансий. Количество: {len(vacancies)}")

    if not vacancies:
        logger.warning("Вакансии не найдены.")
        print("Вакансии не найдены.")
        return

    for i, vacancy in enumerate(vacancies, 1):
        print(f"\n{i}. Название: {vacancy.title}")
        print(f"   Работодатель: {vacancy.employer}")
        print(f"   Зарплата: {vacancy.format_salary()}")
        print(f"   URL: {vacancy.url}")

        if brief_mode:
            # Краткий режим - первые 100 символов
            print(f"   Описание: {vacancy.description[:100]}...")
        else:
            # Полное описание
            print(f"   Описание: {vacancy.description}")

        print("-" * 50)


def main_menu() -> None:
    try:
        logger.info("Запуск главного меню")
        api = HeadHunterAPI()
        storage = JSONStorage()

        while True:
            print("\n--- Поиск работы ---")
            print("1. Найти вакансии")
            print("2. Показать лучшие предложения")
            print("3. Найти работу по ключевому слову")
            print("4. Выход")

            choice = input("Выберите действие: ")

            try:
                if choice == "1":
                    # Простой поиск вакансий
                    profession = input("Какую работу вы ищете? (например, программист, бухгалтер): ")
                    logger.info(f"Поиск вакансий по профессии: {profession}")
                    print(f"Выполняется поиск вакансий по запросу: {profession}")

                    vacancies_data = api.get_vacancies(profession)
                    logger.info(f"Получено вакансий из API: {len(vacancies_data)}")
                    print(f"Получено вакансий: {len(vacancies_data)}")

                    # Преобразование данных API в объекты Vacancy
                    vacancies = [
                        Vacancy(
                            title=vacancy["name"],
                            url=vacancy.get("alternate_url", ""),
                            salary=vacancy.get("salary", {}),
                            description=vacancy.get("snippet", {}).get("requirement", "Описание отсутствует"),
                            employer=vacancy.get("employer", {}).get("name", "Работодатель не указан"),
                        )
                        for vacancy in vacancies_data
                    ]

                    # Сохранение вакансий
                    for vacancy in vacancies:
                        storage.add_vacancy(vacancy)
                        logger.debug(f"Добавлена вакансия: {vacancy.title}")

                    logger.info(f"Найдено и сохранено вакансий: {len(vacancies)}")
                    print(f"Найдено {len(vacancies)} вакансий")
                    display_vacancies(vacancies)

                elif choice == "2":
                    # Топ вакансий по зарплате
                    top_n = int(input("Сколько лучших вакансий показать? "))
                    logger.info(f"Запрос топ-{top_n} вакансий")

                    all_vacancies = storage.get_vacancies()
                    logger.debug(f"Всего вакансий в хранилище: {len(all_vacancies)}")

                    # Сортировка по зарплате
                    sorted_vacancies = sorted(
                        [
                            Vacancy(**{**v, "employer": v.get("employer", "Работодатель не указан")})
                            for v in all_vacancies
                        ],
                        key=lambda x: x.salary or 0,
                        reverse=True,
                    )[:top_n]

                    logger.info(f"Отображение топ-{len(sorted_vacancies)} вакансий")
                    display_vacancies(sorted_vacancies)

                elif choice == "3":
                    # Поиск по ключевому слову
                    keyword = input("Введите ключевое слово для поиска (например, удаленная работа): ")
                    logger.info(f"Поиск вакансий по ключевому слову: {keyword}")

                    # Получение вакансий и преобразование в объекты Vacancy
                    found_vacancies = storage.get_vacancies({"title": keyword})
                    logger.debug(f"Найдено вакансий по заголовку: {len(found_vacancies)}")

                    if not found_vacancies:
                        # Если по заголовку не нашли, ищем в описании
                        found_vacancies = storage.get_vacancies({"description": keyword})
                        logger.debug(f"Найдено вакансий по описанию: {len(found_vacancies)}")

                    filtered_vacancies = [
                        Vacancy(**{**v, "employer": v.get("employer", "Работодатель не указан")})
                        for v in found_vacancies
                    ]

                    logger.info(f"Найдено вакансий по ключевому слову: {len(filtered_vacancies)}")
                    display_vacancies(filtered_vacancies)

                elif choice == "4":
                    logger.info("Выход из программы")
                    break
                else:
                    logger.warning(f"Выбран неверный пункт меню: {choice}")
                    print("Неверный выбор. Попробуйте снова.")

            except ValueError as e:
                logger.error(f"Ошибка ввода: {e}")
                print(f"Ошибка ввода: {e}")
            except Exception as e:
                logger.error(f"Произошла ошибка: {e}", exc_info=True)
                print(f"Произошла ошибка: {e}")

    except Exception as e:
        logger.critical(f"Критическая ошибка: {e}", exc_info=True)
        print(f"Критическая ошибка: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main_menu()

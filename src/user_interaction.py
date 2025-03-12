import json
import sys
import os
from typing import List, Dict, Any

# Добавляем путь к корневой директории проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
		print(f"Зарплата: {vacancy.format_salary()}")
		print(f"URL: {vacancy.url}")
		print(f"Описание: {vacancy.description}")
		print("---")


def main_menu() -> None:
	try:
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
				if choice == '1':
					# Простой поиск вакансий
					profession = input("Какую работу вы ищете? (например, программист, бухгалтер): ")
					print(f"Выполняется поиск вакансий по запросу: {profession}")

					vacancies_data = api.get_vacancies(profession)
					print(f"Получено вакансий: {len(vacancies_data)}")

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

					print(f"Найдено {len(vacancies)} вакансий")
					display_vacancies(vacancies)

				elif choice == '2':
					# Топ вакансий по зарплате
					top_n = int(input("Сколько лучших вакансий показать? "))
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
					keyword = input("Введите ключевое слово для поиска (например, удаленная работа): ")

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

	except Exception as e:
		print(f"Критическая ошибка: {e}")
		import traceback
		traceback.print_exc()


if __name__ == "__main__":
	main_menu()

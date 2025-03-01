from utils.user_interaction import main_menu
from api.hh_api import HeadHunterAPI


def main():
	"""
    Точка входа в приложение
    """
	try:
		# Тестирование API
		hh_api = HeadHunterAPI()
		vacancies = hh_api.get_vacancies("Электрик")

		for vacancy in vacancies:
			print(f"Название: {vacancy['name']}")
			print(f"Зарплата: {vacancy.get('salary', 'Не указана')}")
			print(f"Работодатель: {vacancy['employer']['name']}")
			print("---")

		# Основное меню приложения
		main_menu()
	except Exception as e:
		print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
	main()
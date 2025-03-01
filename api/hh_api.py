import requests
from .abstract_api import AbstractAPI


class HeadHunterAPI(AbstractAPI):
	BASE_URL = "https://api.hh.ru/vacancies"

	def get_vacancies(self, search_query: str, per_page: int = 50) -> list:
		"""
		Получение вакансий с платформы HeadHunter

		:param search_query: Поисковый запрос
		:param per_page: Количество вакансий на странице
		:return: Список вакансий
		"""
		params = {
			"text": search_query,
			"area": 1,  # Россия
			"per_page": per_page
		}

		try:
			response = requests.get(self.BASE_URL, params=params)
			response.raise_for_status()
			return response.json().get('items', [])
		except requests.RequestException as e:
			print(f"Ошибка при получении вакансий: {e}")
			return []

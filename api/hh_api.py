import requests
from typing import List, Dict, Any
from .abstract_api import AbstractAPI


class HeadHunterAPI(AbstractAPI):
	"""
	Класс для работы с API HeadHunter
	"""

	BASE_URL = "https://api.hh.ru/vacancies"

	def __init__(self):
		self._headers = {'User-Agent': 'PandaJobQuest/1.0'}

	def get_vacancies(self, search_query: str, per_page: int = 50) -> List[Dict[str, Any]]:
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
			response = requests.get(self.BASE_URL, params=params, headers=self._headers)
			response.raise_for_status()
			return response.json().get('items', [])
		except requests.RequestException as e:
			print(f"Ошибка при получении вакансий: {e}")
			return []

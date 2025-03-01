from abc import ABC, abstractmethod
from typing import List, Dict, Any


class AbstractAPI(ABC):
	"""
	Абстрактный базовый класс для работы с API вакансий
	"""

	@abstractmethod
	def get_vacancies(self, search_query: str, per_page: int = 50) -> List[Dict[str, Any]]:
		"""
		Абстрактный метод получения вакансий

		:param search_query: Поисковый запрос
		:param per_page: Количество вакансий на странице
		:return: Список вакансий
		"""
		pass

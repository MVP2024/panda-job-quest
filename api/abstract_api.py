from abc import ABC, abstractmethod

class AbstractAPI(ABC):
	@abstractmethod
	def get_vacancies(self, search_query: str) -> list:
		pass

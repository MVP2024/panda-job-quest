from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class AbstractStorage(ABC):
	"""
    Абстрактный базовый класс для работы с хранилищем вакансий
    """

	@abstractmethod
	def add_vacancy(self, vacancy: Any) -> None:
		"""
        Добавление вакансии в хранилище

        :param vacancy: Вакансия для добавления
        """
		pass

	@abstractmethod
	def get_vacancies(self, criteria: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
		"""
        Получение вакансий по критериям

        :param criteria: Критерии фильтрации
        :return: Список вакансий
        """
		pass

	@abstractmethod
	def delete_vacancy(self, criteria: Dict[str, Any]) -> None:
		"""
        Удаление вакансий по критериям

        :param criteria: Критерии удаления
        """
		pass

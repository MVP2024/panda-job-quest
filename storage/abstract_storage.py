from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class AbstractStorage(ABC):
    """
    Абстрактный базовый класс для работы с хранилищем вакансий
    """

    def __init__(self) -> None:
        """
        Инициализация абстрактного хранилища
        """
        self.vacancies: Optional[List[Any]] = None

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

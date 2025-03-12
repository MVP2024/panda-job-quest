from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from logger.logger import setup_logger

# Настройка логгера для этого модуля
logger = setup_logger(__name__)

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
        logger.debug(f"AbstractStorage: Попытка добавить вакансию {vacancy}")
        pass

    @abstractmethod
    def get_vacancies(self, criteria: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Получение вакансий по критериям

        :param criteria: Критерии фильтрации
        :return: Список вакансий
        """
        logger.debug(f"AbstractStorage: Получение вакансий с критериями {criteria}")
        pass

    @abstractmethod
    def delete_vacancy(self, criteria: Dict[str, Any]) -> None:
        """
        Удаление вакансий по критериям

        :param criteria: Критерии удаления
        """
        logger.debug(f"AbstractStorage: Попытка удалить вакансию с критериями {criteria}")
        pass

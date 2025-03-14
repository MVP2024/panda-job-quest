from abc import ABC, abstractmethod
from typing import List, Dict, Any
from logger.logger import setup_logger

class AbstractAPI(ABC):
    """
    Абстрактный базовый класс для работы с API вакансий

    Наследники должны реализовать логирование на всех этапах:
    - Начало поиска вакансий (logging.info)
    - Отладочная информация о запросе (logging.debug)
    - Успешное получение результатов (logging.info)
    - Обработка ошибок (logging.warning, logging.error)
    """
    logger = setup_logger(__name__)

    @abstractmethod
    def get_vacancies(self, search_query: str, per_page: int = 50) -> List[Dict[str, Any]]:
        """
        Абстрактный метод получения вакансий

        :param search_query: Поисковый запрос
        :param per_page: Количество вакансий на странице
        :return: Список вакансий

        Примечание: Метод должен включать логирование на разных уровнях
        """
        self.logger.debug(f"Вызов абстрактного метода get_vacancies с параметрами: search_query={search_query}, per_page={per_page}")
        raise NotImplementedError("Метод get_vacancies должен быть реализован в дочернем классе")

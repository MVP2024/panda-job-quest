import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from logger.logger import setup_logger


class BaseParser(ABC):
    """
    Абстрактный базовый класс для парсеров
    """

    def __init__(self, file_worker: Optional[Any] = None, logger: Optional[logging.Logger] = None) -> None:
        """
        Инициализация парсера

        :param file_worker: Объект для работы с файлами (опционально)
        :param logger: Экземпляр логгера (опционально)
        """
        self.logger = logger or setup_logger(__name__)
        self.logger.debug(f"Инициализация базового парсера с file_worker: {file_worker}")

        try:
            self.file_worker: Optional[Any] = file_worker
            self.logger.info(
                f"Базовый парсер успешно инициализирован с file_worker типа:" f" {type(file_worker).__name__}"
            )
        except Exception as e:
            self.logger.error(f"Ошибка при инициализации базового парсера: {e}")
            raise

    def load_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Абстрактный метод загрузки вакансий

        :param keyword: Ключевое слово для поиска
        :return: Список вакансий
        """
        try:
            self.logger.debug(f"Загрузка вакансий с ключевым словом: {keyword}")
            vacancies = self._load_vacancies(keyword)
            self.logger.info(f"Успешно загружено {len(vacancies)} вакансий с ключевым словом: {keyword}")
            return vacancies
        except Exception as e:
            self.logger.error(f"Ошибка при загрузке вакансий с ключевым словом: {keyword}: {e}")
            raise

    @abstractmethod
    def _load_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Внутренний абстрактный метод для загрузки вакансий.
        Этот метод должен быть реализован подклассами.

        :param keyword: Ключевое слово для поиска
        :return: Список вакансий
        """
        pass

from abc import ABC, abstractmethod
from logger.logger import setup_logger


class BaseParser(ABC):
    """
    Абстрактный базовый класс для парсеров
    """
    logger = setup_logger(__name__)  # Используем setup_logger вместо import logging

    def __init__(self, file_worker=None):
        """
        Инициализация парсера

        :param file_worker: Объект для работы с файлами (опционально)
        """
        self.logger.debug(f"Инициализация базового парсера с file_worker: {file_worker}")

        try:
            self.file_worker = file_worker
            (self.logger.info
             (f"Базовый парсер успешно инициализирован с file_worker типа: {type(file_worker).__name__}"))
        except Exception as e:
            self.logger.error(f"Ошибка при инициализации базового парсера: {e}")
            raise

    @abstractmethod
    def load_vacancies(self, keyword):
        """
        Абстрактный метод загрузки вакансий

        :param keyword: Ключевое слово для поиска
        :return: Список вакансий
        """
        # Абстрактный метод не должен содержать реализации
        pass

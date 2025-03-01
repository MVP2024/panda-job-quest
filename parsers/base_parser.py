from abc import ABC, abstractmethod

class BaseParser(ABC):
    """
    Абстрактный базовый класс для парсеров
    """
    def __init__(self, file_worker=None):
        """
        Инициализация парсера

        :param file_worker: Объект для работы с файлами (опционально)
        """
        self.file_worker = file_worker

    @abstractmethod
    def load_vacancies(self, keyword):
        """
        Абстрактный метод загрузки вакансий

        :param keyword: Ключевое слово для поиска
        :return: Список вакансий
        """
        pass

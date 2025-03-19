from typing import Any, Dict, List, Optional

import requests

from logger.logger import setup_logger

from .base_parser import BaseParser


class HHParser(BaseParser):
    """
    Класс для работы с API HeadHunter
    """

    def __init__(self, file_worker: Optional[Any] = None) -> None:
        """
        Инициализация парсера HeadHunter

        :param file_worker: Объект для работы с файлами (опционально)
        """
        super().__init__(file_worker)

        # Настройка логгера
        self.logger = setup_logger(__name__)

        self.url: str = "https://api.hh.ru/vacancies"
        self.headers: Dict[str, str] = {"User-Agent": "HH-User-Agent"}
        self.params: Dict[str, Any] = {"text": "", "page": 0, "per_page": 100}
        self.vacancies: List[Dict[str, Any]] = []

        self.logger.info("Инициализация HH парсера")

    def _load_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Внутренний метод для загрузки вакансий.

        :param keyword: Ключевое слово для поиска
        :return: Список вакансий
        """
        self.logger.info(f"Начало загрузки вакансий по ключевому слову: {keyword}")

        self.params["text"] = keyword
        self.params["page"] = 0  # Сбрасываем страницу перед новым поиском
        self.vacancies = []  # Очищаем список вакансий

        try:
            # Используем int для page
            current_page: int = 0
            while current_page < 20:  # Ограничиваем количество страниц
                self.logger.debug(f"Загрузка страницы {current_page}")

                # Используем приведение типов
                response = requests.get(self.url, headers=self.headers, params={**self.params, "page": current_page})
                response.raise_for_status()

                # Явное приведение типа
                page_vacancies: List[Dict[str, Any]] = response.json()["items"]
                self.vacancies.extend(page_vacancies)

                self.logger.info(f"Загружено вакансий на странице: {len(page_vacancies)}")

                # Проверка, есть ли еще страницы
                if len(page_vacancies) == 0:
                    self.logger.info("Больше вакансий нет, завершение парсинга")
                    break

                current_page += 1

            # Сохраняем вакансии с помощью file_worker, если он передан
            if self.file_worker:
                self.logger.info(f"Сохранение {len(self.vacancies)} вакансий")
                self.file_worker.save_vacancies(self.vacancies)

            self.logger.info(f"Всего загружено вакансий: {len(self.vacancies)}")
            return self.vacancies

        except requests.RequestException as e:
            error_message = f"Ошибка при загрузке вакансий: {e}"
            self.logger.error(error_message)  # Используем логгер
            return []

    def load_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        return super().load_vacancies(keyword)

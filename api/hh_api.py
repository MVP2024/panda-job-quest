import logging
import os
from typing import Any, Dict, List, Optional, Union

import requests
from dotenv import load_dotenv

from api.abstract_api import AbstractAPI

# Загрузка переменных окружения
load_dotenv()


class HeadHunterAPI(AbstractAPI):
    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
        requests_lib: Optional[Any] = None,
    ) -> None:
        super().__init__(logger)  # Вызов конструктора базового класса
        # Получение client_id и client_secret
        self._private_client_id = client_id or os.getenv("HH_CLIENT_ID")
        self._private_client_secret = client_secret or os.getenv("HH_CLIENT_SECRET")
        self._requests = requests_lib or requests

        # Логирование инициализации
        if self._private_client_id and self._private_client_secret:
            self.logger.info("Инициализация HeadHunterAPI с приватными учетными данными")
        else:
            self.logger.warning(
                "Инициализация HeadHunterAPI без приватных учетных данных. " "Будет использован публичный API."
            )

        # Добавляем _headers
        self._headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}

        # Список публичных API-ключей или API-адрес
        self._public_api_endpoints = [
            "https://api.hh.ru/vacancies",
            "https://hh.ru/search/vacancy",  # Альтернативный API-адрес
        ]

    def _get_access_token(self) -> str:
        """
        Получение токена доступа для приватного API HeadHunter

        :return: Токен доступа
        :raises ValueError: Если отсутствуют учетные данные
        :raises RequestException: При ошибках сети или авторизации
        """
        # Проверка наличия учетных данных
        if not self._private_client_id or not self._private_client_secret:
            self.logger.error("Попытка получения токена без учетных данных")
            raise ValueError("Отсутствуют учетные данные для приватного API")

        # URL для получения токена
        token_url = "https://hh.ru/oauth/token"

        # Параметры для получения токена
        token_data: Dict[str, str] = {
            "grant_type": "client_credentials",
            "client_id": self._private_client_id,
            "client_secret": self._private_client_secret,
        }

        try:
            self.logger.debug("Отправка запроса на получение токена")
            # Отправка запроса на получение токена
            response = self._requests.post(token_url, data=token_data)
            response.raise_for_status()

            # Извлечение токена из ответа
            token_info: Dict[str, str] = response.json()
            access_token: Optional[str] = token_info.get("access_token")

            if access_token:
                self.logger.info("Токен доступа успешно получен")
                return access_token
            else:
                self.logger.warning("Получен пустой токен доступа")
                raise ValueError("Не удалось получить токен доступа")

        except self._requests.RequestException as e:
            self.logger.error(f"Ошибка получения токена: {e}")
            raise

    def get_vacancies(self, search_query: str, per_page: int = 50) -> List[Dict[str, Any]]:
        # Логирование начала поиска вакансий
        self.logger.info(f"Начало поиска вакансий. Запрос: {search_query}, кол-во на странице: {per_page}")

        vacancies: List[Dict[str, Any]] = []

        # Сначала пытаемся использовать приватный API
        if self._private_client_id and self._private_client_secret:
            try:
                self.logger.debug("Попытка использовать приватный API")
                vacancies = self._get_private_api_vacancies(search_query, per_page)
                if vacancies:
                    return vacancies
            except Exception as private_api_error:
                self.logger.warning(f"Ошибка приватного API: {private_api_error}")

        # Если приватный API не сработал, используем публичные API-адрес
        for endpoint in self._public_api_endpoints:
            try:
                self.logger.debug(f"Попытка использовать публичный API: {endpoint}")
                public_vacancies = self._get_public_api_vacancies(endpoint, search_query, per_page)
                if public_vacancies:
                    self.logger.info(f"Найдено вакансий через {endpoint}: {len(public_vacancies)}")
                    vacancies.extend(public_vacancies)
            except Exception as public_api_error:
                self.logger.warning(f"Ошибка публичного API {endpoint}: {public_api_error}")

        # Если ни один API не сработал
        if not vacancies:
            self.logger.error("Не удалось получить вакансии ни через один API")
        return vacancies

    def _get_private_api_vacancies(self, search_query: str, per_page: int) -> List[Dict[str, Any]]:
        # Логика работы с приватным API
        self.logger.debug(
            f"Получение вакансий через приватный API. Запрос: {search_query}, кол-во на странице: {per_page}"
        )

        headers: Dict[str, str] = {"Authorization": f"Bearer {self._get_access_token()}", "User-Agent": "Mozilla/5.0"}
        params: Dict[str, Union[str, int]] = {"text": search_query, "per_page": per_page}

        try:
            response = self._requests.get("https://api.hh.ru/vacancies", headers=headers, params=params)
            response.raise_for_status()

            vacancies: List[Dict[str, Any]] = response.json().get("items", [])
            self.logger.info(f"Получено вакансий через приватный API: {len(vacancies)}")

            return vacancies

        except self._requests.RequestException as e:
            self.logger.error(f"Ошибка при получении вакансий через приватный API: {e}")
            return []

    def _get_public_api_vacancies(self, endpoint: str, search_query: str, per_page: int) -> List[Dict[str, Any]]:
        # Логика работы с публичным API
        self.logger.debug(
            f"Получение вакансий через публичный API. "
            f"Endpoint: {endpoint}, Запрос: {search_query}, кол-во на странице: {per_page}"
        )

        headers: Dict[str, str] = {
            "User-Agent": os.getenv("HH_USER_AGENT", "Mozilla/5.0"),
            "Accept": "application/json",
        }
        params: Dict[str, Union[str, int]] = {"text": search_query, "per_page": per_page}

        try:
            response = self._requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()

            vacancies: List[Dict[str, Any]] = response.json().get("items", [])
            self.logger.info(f"Получено вакансий через публичный API {endpoint}: {len(vacancies)}")

            return vacancies

        except self._requests.RequestException as e:
            self.logger.error(f"Ошибка при получении вакансий через публичный API {endpoint}: {e}")
            return []

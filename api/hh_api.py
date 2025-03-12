import os
import logging
import requests
from typing import List, Dict, Any
from dotenv import load_dotenv
from .abstract_api import AbstractAPI

# Загрузка переменных окружения
load_dotenv()


class HeadHunterAPI(AbstractAPI):
    def __init__(self, client_id=None, client_secret=None):
        self._private_client_id = client_id or os.getenv('HH_CLIENT_ID')
        self._private_client_secret = client_secret or os.getenv('HH_CLIENT_SECRET')

        # Добавляем _headers
        self._headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/json'
        }

        # Список публичных API-ключей или API-адрес
        self._public_api_endpoints = [
            'https://api.hh.ru/vacancies',
            'https://hh.ru/search/vacancy'  # Альтернативный API-адрес

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
            raise ValueError("Отсутствуют учетные данные для приватного API")

        # URL для получения токена
        token_url = 'https://hh.ru/oauth/token'

        # Параметры для получения токена
        token_data = {
            'grant_type': 'client_credentials',
            'client_id': self._private_client_id,
            'client_secret': self._private_client_secret
        }

        try:
            # Отправка запроса на получение токена
            response = requests.post(token_url, data=token_data)
            response.raise_for_status()

            # Извлечение токена из ответа
            token_info = response.json()
            return token_info.get('access_token')

        except requests.RequestException as e:
            logging.error(f"Ошибка получения токена: {e}")
            raise

    def get_vacancies(self, search_query: str, per_page: int = 50) -> List[Dict[str, Any]]:
        # Сначала пытаемся использовать приватный API
        try:
            if self._private_client_id and self._private_client_secret:
                return self._get_private_api_vacancies(search_query, per_page)
        except Exception as private_api_error:
            logging.warning(f"Ошибка приватного API: {private_api_error}")

        # Если приватный API не сработал, используем публичные API-адрес
        for endpoint in self._public_api_endpoints:
            try:
                vacancies = self._get_public_api_vacancies(endpoint, search_query, per_page)
                if vacancies:
                    return vacancies
            except Exception as public_api_error:
                logging.warning(f"Ошибка публичного API {endpoint}: {public_api_error}")

        # Если ни один API не сработал
        logging.error("Не удалось получить вакансии ни через один API")
        return []

    def _get_private_api_vacancies(self, search_query: str, per_page: int) -> List[Dict[str, Any]]:
        # Логика работы с приватным API
        headers = {
            'Authorization': f'Bearer {self._get_access_token()}',
            'User-Agent': 'Mozilla/5.0'
        }
        params = {"text": search_query, "per_page": per_page}

        response = requests.get('https://api.hh.ru/vacancies', headers=headers, params=params)
        response.raise_for_status()
        return response.json().get('items', [])

    @staticmethod
    def _get_public_api_vacancies(endpoint: str, search_query: str, per_page: int) -> List[Dict[str, Any]]:
        # Логика работы с публичным API
        headers = {
            'User-Agent': os.getenv('HH_USER_AGENT', 'Mozilla/5.0'),
            'Accept': 'application/json'
        }
        params = {"text": search_query, "per_page": per_page}

        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        return response.json().get('items', [])

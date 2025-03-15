import os
import requests
from typing import List, Dict, Any
from dotenv import load_dotenv
from .abstract_api import AbstractAPI
from logger.logger import setup_logger

# Загрузка переменных окружения
load_dotenv()

# Настройка логгера для модуля
logger = setup_logger(__name__)

class HeadHunterAPI(AbstractAPI):
    def __init__(self, client_id=None, client_secret=None):
        # Получение client_id и client_secret
        self._private_client_id = client_id or os.getenv('HH_CLIENT_ID')
        self._private_client_secret = client_secret or os.getenv('HH_CLIENT_SECRET')

        # Логирование инициализации
        if self._private_client_id and self._private_client_secret:
            logger.info("Инициализация HeadHunterAPI с приватными учетными данными")
        else:
            logger.warning(
                "Инициализация HeadHunterAPI без приватных учетных данных. Будет использован публичный API.")

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
            logger.error("Попытка получения токена без учетных данных")
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
            logger.debug("Отправка запроса на получение токена")
            # Отправка запроса на получение токена
            response = requests.post(token_url, data=token_data)
            response.raise_for_status()

            # Извлечение токена из ответа
            token_info = response.json()
            access_token = token_info.get('access_token')

            if access_token:
                logger.info("Токен доступа успешно получен")
                return access_token
            else:
                logger.warning("Получен пустой токен доступа")
                raise ValueError("Не удалось получить токен доступа")

        except requests.RequestException as e:
            logger.error(f"Ошибка получения токена: {e}")
            raise

    def get_vacancies(self, search_query: str, per_page: int = 50) -> List[Dict[str, Any]]:
        # Логирование начала поиска вакансий
        logger.info(f"Начало поиска вакансий. Запрос: {search_query}, кол-во на странице: {per_page}")

        # Сначала пытаемся использовать приватный API
        try:
            if self._private_client_id and self._private_client_secret:
                logger.debug("Попытка использовать приватный API")
                return self._get_private_api_vacancies(search_query, per_page)
        except Exception as private_api_error:
            logger.warning(f"Ошибка приватного API: {private_api_error}")

        # Если приватный API не сработал, используем публичные API-адрес
        for endpoint in self._public_api_endpoints:
            try:
                logger.debug(f"Попытка использовать публичный API: {endpoint}")
                vacancies = self._get_public_api_vacancies(endpoint, search_query, per_page)
                if vacancies:
                    logger.info(f"Найдено вакансий через {endpoint}: {len(vacancies)}")
                    return vacancies
            except Exception as public_api_error:
                logger.warning(f"Ошибка публичного API {endpoint}: {public_api_error}")

        # Если ни один API не сработал
        logger.error("Не удалось получить вакансии ни через один API")
        return []

    def _get_private_api_vacancies(self, search_query: str, per_page: int) -> List[Dict[str, Any]]:
        # Логика работы с приватным API
        logger.debug(f"Получение вакансий через приватный API. Запрос: {search_query}, кол-во на странице: {per_page}")

        headers = {
            'Authorization': f'Bearer {self._get_access_token()}',
            'User-Agent': 'Mozilla/5.0'
        }
        params = {"text": search_query, "per_page": per_page}

        try:
            response = requests.get('https://api.hh.ru/vacancies', headers=headers, params=params)
            response.raise_for_status()

            vacancies = response.json().get('items', [])
            logger.info(f"Получено вакансий через приватный API: {len(vacancies)}")

            return vacancies

        except requests.RequestException as e:
            logger.error(f"Ошибка при получении вакансий через приватный API: {e}")
            raise

    @staticmethod
    def _get_public_api_vacancies(endpoint: str, search_query: str, per_page: int) -> List[Dict[str, Any]]:
        # Логика работы с публичным API
        logger.debug(
            f"Получение вакансий через публичный API. Endpoint: {endpoint}, Запрос: {search_query}, кол-во на странице: {per_page}")

        headers = {
            'User-Agent': os.getenv('HH_USER_AGENT', 'Mozilla/5.0'),
            'Accept': 'application/json'
        }
        params = {"text": search_query, "per_page": per_page}

        try:
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()

            vacancies = response.json().get('items', [])
            logger.info(f"Получено вакансий через публичный API {endpoint}: {len(vacancies)}")

            return vacancies

        except requests.RequestException as e:
            logger.error(f"Ошибка при получении вакансий через публичный API {endpoint}: {e}")
            raise

import os
from dotenv import load_dotenv
import requests
from typing import List, Dict, Any
from .abstract_api import AbstractAPI

# Загрузка переменных окружения
load_dotenv()

class HeadHunterAPI(AbstractAPI):
    """
    Класс для работы с API HeadHunter
    """

    BASE_URL = os.getenv('HH_API_BASE_URL', 'https://api.hh.ru/vacancies')

    def __init__(self):
        self._headers = {'User-Agent': os.getenv('HH_USER_AGENT', 'PandaJobQuest/1.0')}

    def get_vacancies(self, search_query: str, per_page: int = 50) -> List[Dict[str, Any]]:
        """
        Получение вакансий с платформы HeadHunter
        """
        params = {
            "text": search_query,
            "area": 1,  # Россия
            "per_page": per_page,
            "page": 0   # Добавляем номер страницы
        }

        try:
            # Расширенные заголовки
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'application/json'
            }

            # Подробный вывод параметров запроса
            print(f"Параметры запроса: {params}")
            print(f"Заголовки: {headers}")

            response = requests.get(
                self.BASE_URL,
                params=params,
                headers=headers,
                timeout=10  # Добавляем таймаут
            )

            # Проверка статуса ответа
            print(f"Статус ответа: {response.status_code}")

            # Проверка содержимого ответа
            try:
                data = response.json()
                print(f"Получено вакансий: {len(data.get('items', []))}")
                return data.get('items', [])
            except ValueError as json_error:
                print(f"Ошибка декодирования JSON: {json_error}")
                print(f"Текст ответа: {response.text}")
                return []

        except requests.RequestException as e:
            print(f"Ошибка при получении вакансий: {e}")
            return []

import os
import json
import re
from datetime import datetime
from typing import List, Dict, Any, Optional
from .abstract_storage import AbstractStorage

class JSONStorage(AbstractStorage):
    def __init__(self, filename: str = None):
        if filename is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self._data_dir = os.path.join(base_dir, 'data')
            os.makedirs(self._data_dir, exist_ok=True)
            self._filename = os.path.join(self._data_dir, 'vacancies.json')
        else:
            self._filename = filename
            self._data_dir = os.path.dirname(filename)

    def add_vacancy(self, vacancy: Any, create_new_file: bool = False) -> None:
        """
        Добавление вакансии с опциональным созданием нового файла

        :param vacancy: Объект вакансии для добавления
        :param create_new_file: Флаг для создания нового файла с отметкой времени
        """
        # Если указан флаг создания нового файла или файл пустой
        if create_new_file or not os.path.exists(self._filename) or os.path.getsize(self._filename) == 0:
            # Создаем новый файл с отметкой времени
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename = os.path.join(self._data_dir, f'vacancies_{timestamp}.json')
            self._filename = new_filename

        vacancies = self._load_vacancies()
        vacancy_dict = vacancy.to_dict()

        # Очистка описания от HTML-тегов
        vacancy_dict['description'] = self._remove_html_tags(vacancy_dict['description'])

        # Проверка на дубликаты
        if vacancy_dict not in vacancies:
            vacancies.append(vacancy_dict)
            self._save_vacancies(vacancies)

    def get_vacancies(self, criteria: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Получение вакансий по критериям

        :param criteria: Критерии фильтрации
        :return: Список вакансий
        """
        vacancies = self._load_vacancies()

        if criteria:
            return [v for v in vacancies if self._match_criteria(v, criteria)]

        return vacancies

    def delete_vacancy(self, criteria: Dict[str, Any]) -> None:
        """
        Удаление вакансий по критериям

        :param criteria: Критерии удаления
        """
        vacancies = self._load_vacancies()
        vacancies = [v for v in vacancies if not self._match_criteria(v, criteria)]
        self._save_vacancies(vacancies)

    def get_vacancies_by_salary_range(self, min_salary: float = 0, max_salary: float = float('inf')) -> List[Dict[str, Any]]:
        """
        Получение вакансий в определенном диапазоне зарплат

        :param min_salary: Минимальная зарплата
        :param max_salary: Максимальная зарплата
        :return: Список вакансий в указанном диапазоне зарплат
        """
        vacancies = self._load_vacancies()
        return [
            vacancy for vacancy in vacancies
            if min_salary <= vacancy.get('salary', 0) <= max_salary
        ]

    def get_vacancies_by_profession(self, profession: str) -> List[Dict[str, Any]]:
        """
        Получение вакансий по профессии

        :param profession: Название профессии
        :return: Список вакансий по указанной профессии
        """
        return [
            vacancy for vacancy in self._load_vacancies()
            if profession.lower() in vacancy.get('title', '').lower()
        ]

    def _load_vacancies(self) -> List[Dict[str, Any]]:
        """
        Загрузка вакансий из JSON-файла

        :return: Список вакансий
        """
        try:
            with open(self._filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def _save_vacancies(self, vacancies: List[Dict[str, Any]]) -> None:
        """
        Сохранение вакансий в JSON-файл

        :param vacancies: Список вакансий для сохранения
        """
        with open(self._filename, 'w', encoding='utf-8') as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=2)

    def _match_criteria(self, vacancy: Dict[str, Any], criteria: Dict[str, Any]) -> bool:
        """
        Проверка соответствия вакансии заданным критериям

        :param vacancy: Словарь с информацией о вакансии
        :param criteria: Критерии для фильтрации
        :return: Результат проверки соответствия
        """
        return all(
            str(value).lower() in str(vacancy.get(key, '')).lower()
            for key, value in criteria.items()
        )

    def _remove_html_tags(self, text: str) -> str:
        """
        Удаление HTML-тегов из текста с декодированием специальных символов

        :param text: Текст с возможными HTML-тегами
        :return: Текст без HTML-тегов
        """
        from html import unescape
        import re

        if not text:
            return ''

        # Удаление HTML-тегов, включая теги с атрибутами
        clean_text = re.sub('<[^>]*>', '', text)

        # Декодирование HTML-сущностей
        clean_text = unescape(clean_text)

        # Удаление лишних пробелов и переводов строк
        clean_text = ' '.join(clean_text.split())

        return clean_text

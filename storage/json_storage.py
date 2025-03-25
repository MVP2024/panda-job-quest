import json
import os
import re
from datetime import datetime
from html import unescape
from typing import Any, Dict, List, Optional

from logger.logger import setup_logger

from .abstract_storage import AbstractStorage

# Настройка логгера
logger = setup_logger(__name__)


class JSONStorage(AbstractStorage):
    def __init__(self, filename: Optional[str] = None):
        """
        Инициализация JSONStorage

        :param filename: Путь к файлу для хранения данных (опционально)
        """
        logger.info(f"Инициализация JSONStorage с filename: {filename}")

        # Определение базовой директории и файла
        base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._data_dir: str = os.path.join(base_dir, "data")
        os.makedirs(self._data_dir, exist_ok=True)

        # Установка пути к файлу
        if filename is None:
            self._filename: str = os.path.join(self._data_dir, "vacancies.json")
        else:
            self._filename = filename
            self._data_dir = os.path.dirname(filename)

        logger.debug(f"Путь к файлу данных: {self._filename}")

    def add_vacancy(self, vacancy: Any, create_new_file: bool = False) -> None:
        """
        Добавление вакансии с опциональным созданием нового файла

        :param vacancy: Объект вакансии
        :param create_new_file: Флаг создания нового файла
        """
        logger.info(f"Добавление вакансии. Создание нового файла: {create_new_file}")

        # Если указан флаг создания нового файла или файл пустой
        if create_new_file or not os.path.exists(self._filename) or os.path.getsize(self._filename) == 0:
            # Создаем новый файл с отметкой времени
            timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename: str = os.path.join(self._data_dir, f"vacancies_{timestamp}.json")
            self._filename = new_filename
            logger.debug(f"Создан новый файл: {new_filename}")

        vacancies: List[Dict[str, Any]] = self._load_vacancies()
        vacancy_dict: Dict[str, Any] = vacancy.to_dict()

        # Очистка описания от HTML-тегов
        vacancy_dict["description"] = self._remove_html_tags(vacancy_dict["description"])

        # Проверка на дубликаты
        if vacancy_dict not in vacancies:
            vacancies.append(vacancy_dict)
            self._save_vacancies(vacancies)
            logger.info(f"Вакансия добавлена: {vacancy_dict.get('title', 'Без названия')}")
        else:
            logger.debug("Вакансия уже существует, пропуск добавления")

    def get_vacancies(self, criteria: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Получение вакансий по критериям

        :param criteria: Критерии фильтрации
        :return: Список вакансий
        """
        logger.info(f"Получение вакансий с критериями: {criteria}")

        vacancies: List[Dict[str, Any]] = self._load_vacancies()

        if criteria:
            filtered_vacancies: List[Dict[str, Any]] = [v for v in vacancies if self._match_criteria(v, criteria)]
            logger.debug(f"Найдено вакансий по критериям: {len(filtered_vacancies)}")
            return filtered_vacancies

        return vacancies

    def delete_vacancy(self, criteria: Dict[str, Any]) -> None:
        """
        Удаление вакансий по критериям

        :param criteria: Критерии удаления
        """
        logger.info(f"Удаление вакансий по критериям: {criteria}")

        vacancies: List[Dict[str, Any]] = self._load_vacancies()
        initial_count: int = len(vacancies)

        vacancies = [v for v in vacancies if not self._match_criteria(v, criteria)]
        self._save_vacancies(vacancies)

        deleted_count: int = initial_count - len(vacancies)
        logger.debug(f"Удалено вакансий: {deleted_count}")

    def get_vacancies_by_salary_range(
        self, min_salary: float = 0, max_salary: float = float("inf")
    ) -> List[Dict[str, Any]]:
        """
        Получение вакансий в определенном диапазоне зарплат

        :param min_salary: Минимальная зарплата
        :param max_salary: Максимальная зарплата
        :return: Список вакансий в указанном диапазоне зарплат
        """
        vacancies: List[Dict[str, Any]] = self._load_vacancies()
        return [
            vacancy
            for vacancy in vacancies
            if self._is_salary_in_range(vacancy.get("salary", {}), min_salary, max_salary)
        ]

    @staticmethod
    def _is_salary_in_range(salary: Dict[str, Any], min_salary: float, max_salary: float) -> bool:
        """
        Проверка попадания зарплаты в диапазон

        :param salary: Словарь зарплаты
        :param min_salary: Минимальная зарплата
        :param max_salary: Максимальная зарплата
        :return: находится ли зарплата в диапазоне
        """
        if not salary:
            return False

        # Проверяем диапазон 'from' и 'to'
        salary_from: float = float(salary.get("from", 0))
        salary_to: float = float(salary.get("to", float("inf")))

        return bool(
            (min_salary <= salary_from or min_salary <= salary_to)
            and (salary_from <= max_salary or salary_to <= max_salary)
        )

    def get_vacancies_by_profession(self, profession: str) -> List[Dict[str, Any]]:
        """
        Получение вакансий по профессии

        :param profession: Название профессии
        :return: Список вакансий по указанной профессии
        """
        return [vacancy for vacancy in self._load_vacancies()
                if profession.lower() in vacancy.get("title", "").lower()]

    def _load_vacancies(self) -> List[Dict[str, Any]]:
        """
        Загрузка вакансий из JSON-файла

        :return: Список вакансий
        """
        try:
            with open(self._filename, "r", encoding="utf-8") as f:
                # Явное приведение типа с проверкой
                loaded_data: List[Dict[str, Any]] = json.load(f)

                # Дополнительная проверка типа загруженных данных
                if not isinstance(loaded_data, list):
                    logger.warning(f"Некорректный формат данных в файле {self._filename}")
                    return []

                # Проверка, что каждый элемент - словарь
                if not all(isinstance(item, dict) for item in loaded_data):
                    logger.warning(f"Некоторые элементы в файле {self._filename} не являются словарями")
                    return []

                return loaded_data
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.warning(f"Ошибка при загрузке файла {self._filename}: {e}")
            return []

    def _save_vacancies(self, vacancies: List[Dict[str, Any]]) -> None:
        """
        Сохранение вакансий в JSON-файл

        :param vacancies: Список вакансий для сохранения
        """
        with open(self._filename, "w", encoding="utf-8") as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=2)

    @staticmethod
    def _match_criteria(vacancy: Dict[str, Any], criteria: Dict[str, Any]) -> bool:
        """
        Проверка соответствия вакансии заданным критериям

        :param vacancy: Словарь с информацией о вакансии
        :param criteria: Критерии для фильтрации
        :return: Результат проверки соответствия
        """
        return all(str(value).lower() in str(vacancy.get(key, "")).lower() for key, value in criteria.items())

    @staticmethod
    def _remove_html_tags(text: str) -> str:
        """
        Удаление HTML-тегов из текста с декодированием специальных символов

        :param text: Текст с возможными HTML-тегами
        :return: Текст без HTML-тегов
        """
        if not text:
            return ""

        # Удаление HTML-тегов, включая теги с атрибутами
        clean_text: str = re.sub("<[^>]*>", "", text)

        # Декодирование HTML-сущностей
        clean_text = unescape(clean_text)

        # Удаление лишних пробелов и переводов строк
        clean_text = " ".join(clean_text.split())

        return clean_text

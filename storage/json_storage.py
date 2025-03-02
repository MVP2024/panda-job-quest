import json
import os
from typing import List, Dict, Any, Optional
from .abstract_storage import AbstractStorage


class JSONStorage(AbstractStorage):
    """
    Класс для работы с JSON-хранилищем вакансий
    """

    def __init__(self, filename: str = None):
        """
        Инициализация JSON-хранилища с автоматическим созданием директории.
        """
        if filename is None:
            # Создаем абсолютный путь к файлу в директории data корня проекта
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            filename = os.path.join(base_dir, 'data', 'vacancies.json')

        os.makedirs(os.path.dirname(filename), exist_ok=True)
        self._filename = filename


    def add_vacancy(self, vacancy: Any) -> None:
        """
        Добавление вакансии в JSON-файл
        """
        vacancies = self._load_vacancies()
        vacancy_dict = vacancy.to_dict()  # Используйте новый метод

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
        return all(
            str(value).lower() in str(vacancy.get(key, '')).lower()
            for key, value in criteria.items()
        )

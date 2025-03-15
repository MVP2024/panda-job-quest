from logger.logger import setup_logger
from typing import Optional, Dict, Any, Union

# Настройка логгера для модуля
logger = setup_logger(__name__)

class Vacancy:
    """
    Класс для представления вакансии
    """
    __slots__ = ['_title', '_url', '_salary', '_description']

    def __init__(self, title: str, url: str, salary: Union[Dict[str, Any], float, None] = None,
                 description: str = "Описание отсутствует"):
        """
        Инициализация вакансии с валидацией и обработкой данных

        :param title: Название вакансии (обязательно)
        :param url: URL вакансии (обязательно)
        :param salary: Зарплата (опционально)
        :param description: Описание вакансии (опционально)
        """
        self._title = ''
        self._url = ''
        self._salary = 0.0
        self._description = ''

        # Используем setter-методы для установки значений
        try:
            self.title = title
            self.url = url
            self.description = description
            self.salary = salary

            self._validate_data()
            logger.info(f"Вакансия успешно создана: {title}")
        except ValueError as e:
            logger.error(f"Ошибка при создании вакансии: {e}")
            raise

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразование вакансии в словарь

        :return: Словарь с данными вакансии
        """
        vacancy_dict = {
            'title': self._title,
            'url': self._url,
            'salary': self._salary,
            'description': self._description
        }

        logger.info(f"Создан словарь вакансии: {vacancy_dict}")
        return vacancy_dict

    def _validate_data(self) -> None:
        """
        Приватный метод валидации данных вакансии
        """
        try:
            if not self._title:
                logger.warning("Попытка создания вакансии с пустым названием")
                raise ValueError("Название вакансии не может быть пустым")

            if not self._url:
                logger.warning("Попытка создания вакансии с пустым URL")
                raise ValueError("URL вакансии не может быть пустым")

            logger.info(f"Валидация вакансии '{self._title}' успешно завершена")
        except ValueError as e:
            logger.error(f"Ошибка валидации вакансии: {e}")
            raise

    def format_salary(self) -> str:
        if self.salary is None or self.salary == 0:
            logger.info(f"Зарплата для вакансии '{self._title}' не указана")
            return "Зарплата не указана"

        formatted_salary = f"{self.salary:,.2f} руб."
        logger.info(f"Отформатированная зарплата для вакансии '{self._title}': {formatted_salary}")
        return formatted_salary

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        """
        Setter для свойства title с валидацией

        :param value: Новое значение заголовка
        """
        try:
            if not value:
                logger.warning("Попытка установить пустое название вакансии")
                raise ValueError("Название вакансии не может быть пустым")

            self._title = value
            logger.info(f"Заголовок вакансии успешно установлен: {value}")
        except ValueError as e:
            logger.error(f"Ошибка при установке заголовка: {e}")
            raise

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, value: str) -> None:
        """
        Setter для свойства url с валидацией

        :param value: Новый URL
        """
        try:
            if not value:
                logger.warning("Попытка установить пустой URL вакансии")
                raise ValueError("URL вакансии не может быть пустым")

            self._url = value
            logger.info(f"URL вакансии успешно установлен: {value}")
        except ValueError as e:
            logger.error(f"Ошибка при установке URL: {e}")
            raise

    @property
    def salary(self) -> Optional[float]:
        return self._salary

    @salary.setter
    def salary(self, value: Union[Dict[str, Any], float, None]) -> None:
        """
        Setter для свойства salary с валидацией

        :param value: Новое значение зарплаты
        """
        try:
            if isinstance(value, dict):
                # Если зарплата из API HH
                salary_from = value.get('from', 0) or 0
                salary_to = value.get('to', 0) or 0
                self._salary = (salary_from + salary_to) / 2 if salary_from or salary_to else 0.0
                logger.info(
                    f"Зарплата установлена из словаря: from {salary_from}, to {salary_to}, средняя {self._salary}")
            elif value is None:
                # Если зарплата None
                self._salary = 0.0
                logger.info("Зарплата установлена как 0 (значение None)")
            else:
                # Если зарплата передана напрямую
                self._salary = float(value)
                logger.info(f"Зарплата установлена напрямую: {self._salary}")
        except Exception as e:
            logger.error(f"Ошибка при установке зарплаты: {e}")
            raise

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        """
        Setter для свойства description с валидацией

        :param value: Новое описание
        """
        original_value = value
        self._description = value or 'Описание отсутствует'

        logger.info(f"Описание вакансии установлено: {self._description}")

        if original_value is None or original_value.strip() == '':
            logger.warning("Установлено описание по умолчанию, так как переданное значение было пустым")

    def __lt__(self, other: 'Vacancy') -> bool:
        """
        Сравнение вакансий по зарплате

        :param other: Другая вакансия для сравнения
        :return: Результат сравнения
        """
        if not isinstance(other, Vacancy):
            logger.warning(f"Попытка сравнения с объектом, не являющимся вакансией: {type(other)}")
            return NotImplemented

        # Безопасное сравнение зарплат
        self_salary = self.salary if self.salary is not None else 0
        other_salary = other.salary if other.salary is not None else 0

        result = self_salary < other_salary
        logger.info(
            f"Результат сравнения зарплат: {self._title} ({self_salary}) < {other._title} ({other_salary}) = {result}")

        return result

    def __repr__(self) -> str:
        """
        Строковое представление вакансии

        :return: Строка с информацией о вакансии
        """
        repr_string = f"Vacancy(title={self._title}, salary={self._salary})"

        return repr_string

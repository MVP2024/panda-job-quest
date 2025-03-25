from typing import Any, Dict, Optional, Union

from logger.logger import setup_logger

# Настройка логгера для модуля
logger = setup_logger(__name__)


class Vacancy:
    """
    Класс для представления вакансии с расширенной валидацией и обработкой данных
    """

    __slots__ = ["_title", "_url", "_salary", "_description", "_employer"]

    def __init__(
        self,
        title: str,
        url: str,
        salary: Union[Dict[str, Any], float, None] = None,
        description: str = "Описание отсутствует",
        employer: Optional[str] = None,
    ):
        """
        Инициализация вакансии с валидацией и обработкой данных

        :param title: Название вакансии (обязательно)
        :param url: URL вакансии (обязательно)
        :param salary: Зарплата (опционально)
        :param description: Описание вакансии (опционально)
        :param employer: Название работодателя (опционально)
        """
        self._title: str = ""
        self._url: str = ""
        self._salary: Optional[float] = 0.0
        self._description: str = ""
        self._employer: str = ""

        try:
            self.title = self._validate_title(title)
            self.url = self._validate_url(url)
            self.description = self._validate_description(description)
            self.salary = self._process_salary(salary)
            self.employer = self._validate_employer(employer)

            logger.info(f"Вакансия успешно создана: {self._title}")
        except ValueError as e:
            logger.error(f"Ошибка при создании вакансии: {e}")
            raise

    def _validate_title(self, value: str) -> str:
        """
        Валидация и очистка названия вакансии

        :param value: Исходное название
        :return: Очищенное название
        """
        if not value or not value.strip():
            logger.warning("Попытка установить пустое название вакансии")
            raise ValueError("Название вакансии не может быть пустым")
        return value.strip()

    def _validate_url(self, value: str) -> str:
        """
        Валидация и очистка URL вакансии

        :param value: Исходный URL
        :return: Очищенный URL
        """
        if not value or not value.strip():
            logger.warning("Попытка установить пустой URL вакансии")
            raise ValueError("URL вакансии не может быть пустым")
        return value.strip()

    def _validate_description(self, value: Optional[str]) -> str:
        """
        Валидация и очистка описания вакансии

        :param value: Исходное описание
        :return: Очищенное описание
        """
        if not value or not value.strip():
            logger.warning("Описание вакансии пустое, установлено значение по умолчанию")
            return "Описание отсутствует"
        return value.strip()

    def _validate_employer(self, value: Optional[str]) -> str:
        """
        Валидация и очистка названия работодателя

        :param value: Исходное название работодателя
        :return: Очищенное название работодателя
        """
        if not value or not value.strip():
            logger.warning("Название работодателя пустое, установлено значение по умолчанию")
            return "Работодатель не указан"
        return value.strip()

    def _process_salary(self, value: Union[Dict[str, Any], float, None]) -> Optional[float]:
        """
        Обработка входящего значения зарплаты

        :param value: Входящее значение зарплаты
        :return: Обработанное значение зарплаты
        """
        try:
            if isinstance(value, dict):
                salary_from = value.get("from", 0) or 0
                salary_to = value.get("to", 0) or 0
                processed_salary = (salary_from + salary_to) / 2 if salary_from or salary_to else 0.0
                logger.info(
                    f"Зарплата обработана из словаря: from {salary_from}, to {salary_to}, средняя {processed_salary}"
                )
                return processed_salary
            elif value is None:
                logger.info("Зарплата обработана как 0 (значение None)")
                return 0.0
            else:
                processed_salary = float(value)
                logger.info(f"Зарплата обработана напрямую: {processed_salary}")
                return processed_salary
        except Exception as e:
            logger.error(f"Ошибка при обработке зарплаты: {e}")
            raise

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразование вакансии в словарь

        :return: Словарь с данными вакансии
        """
        return {
            "title": self._title,
            "url": self._url,
            "salary": self._salary,
            "description": self._description,
            "employer": self._employer,
        }

    def format_salary(self) -> str:
        """
        Форматирование зарплаты

        :return: Отформатированная строка зарплаты
        """
        if self.salary is None or self.salary == 0:
            logger.info(f"Зарплата для вакансии '{self._title}' не указана")
            return "Зарплата не указана"

        formatted_salary = f"{self.salary:,.2f} руб.".replace(",", " ")
        logger.info(f"Отформатированная зарплата для вакансии '{self._title}': {formatted_salary}")
        return formatted_salary

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._title = self._validate_title(value)
        logger.info(f"Заголовок вакансии успешно установлен: {self._title}")

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, value: str) -> None:
        self._url = self._validate_url(value)
        logger.info(f"URL вакансии успешно установлен: {self._url}")

    @property
    def salary(self) -> Optional[float]:
        return self._salary

    @salary.setter
    def salary(self, value: Union[Dict[str, Any], float, None]) -> None:
        self._salary = self._process_salary(value)

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = self._validate_description(value)
        logger.info(f"Описание вакансии установлено: {self._description}")

    @property
    def employer(self) -> str:
        return self._employer

    @employer.setter
    def employer(self, value: Optional[str]) -> None:
        self._employer = self._validate_employer(value)
        logger.info(f"Работодатель установлен: {self._employer}")

    def __lt__(self, other: "Vacancy") -> bool:
        """
        Сравнение вакансий по зарплате

        :param other: Другая вакансия для сравнения
        :return: Результат сравнения
        """
        if not isinstance(other, Vacancy):
            logger.warning(f"Попытка сравнения с объектом, не являющимся вакансией: {type(other)}")
            return NotImplemented

        self_salary = self.salary or 0
        other_salary = other.salary or 0

        result = self_salary < other_salary
        logger.info(
            f"Результат сравнения зарплат: {self._title} ({self_salary}) < {other._title} ({other_salary}) = {result}"
        )

        return result

    def __repr__(self) -> str:
        """
        Строковое представление вакансии

        :return: Строка с информацией о вакансии
        """
        return f"Vacancy(title={self._title}, salary={self._salary})"

from typing import Optional, Dict, Any, Union

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
        self.title = title
        self.url = url
        self.description = description
        self.salary = salary

        self._validate_data()

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразование вакансии в словарь

        :return: Словарь с данными вакансии
        """
        return {
            'title': self._title,
            'url': self._url,
            'salary': self._salary,
            'description': self._description
        }

    def _validate_data(self) -> None:
        """
        Приватный метод валидации данных вакансии
        """
        if not self._title:
            raise ValueError("Название вакансии не может быть пустым")

        if not self._url:
            raise ValueError("URL вакансии не может быть пустым")

    def format_salary(self) -> str:
        """
        Форматирование зарплаты для красивого отображения

        :return: Отформатированная строка зарплаты
        """
        if self.salary is None or self.salary == 0:
            return "Зарплата не указана"
        return f"{self.salary:,.2f} руб."

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        """
        Setter для свойства title с валидацией

        :param value: Новое значение заголовка
        """
        if not value:
            raise ValueError("Название вакансии не может быть пустым")
        self._title = value

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, value: str) -> None:
        """
        Setter для свойства url с валидацией

        :param value: Новый URL
        """
        if not value:
            raise ValueError("URL вакансии не может быть пустым")
        self._url = value

    @property
    def salary(self) -> Optional[float]:
        return self._salary

    @salary.setter
    def salary(self, value: Union[Dict[str, Any], float, None]) -> None:
        """
        Setter для свойства salary с валидацией

        :param value: Новое значение зарплаты
        """
        if isinstance(value, dict):
            # Если зарплата из API HH
            salary_from = value.get('from', 0) or 0
            salary_to = value.get('to', 0) or 0
            self._salary = (salary_from + salary_to) / 2 if salary_from or salary_to else 0.0
        elif value is None:
            # Если зарплата None
            self._salary = 0.0
        else:
            # Если зарплата передана напрямую
            self._salary = float(value)

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        """
        Setter для свойства description с валидацией

        :param value: Новое описание
        """
        self._description = value or 'Описание отсутствует'

    def __lt__(self, other: 'Vacancy') -> bool:
        """
        Сравнение вакансий по зарплате

        :param other: Другая вакансия для сравнения
        :return: Результат сравнения
        """
        if not isinstance(other, Vacancy):
            return NotImplemented

        # Безопасное сравнение зарплат
        self_salary = self.salary if self.salary is not None else 0
        other_salary = other.salary if other.salary is not None else 0

        return self_salary < other_salary

    def __repr__(self) -> str:
        """
        Строковое представление вакансии

        :return: Строка с информацией о вакансии
        """
        return f"Vacancy(title={self._title}, salary={self._salary})"

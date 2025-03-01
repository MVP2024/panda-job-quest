from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class Vacancy:
    """
    Класс для представления вакансии с использованием __slots__
    """
    __slots__ = ['_title', '_url', '_salary', '_description']

    title: str = field(default='')
    url: str = field(default='')
    salary: Optional[Dict[str, Any]] = field(default_factory=dict)
    description: str = field(default="Описание отсутствует")

    def __post_init__(self):
        """
        Валидация данных после инициализации
        """
        self._title = self.title
        self._url = self.url or ''

        # Обработка зарплаты
        if isinstance(self.salary, dict):
            # Если зарплата из API HH
            salary_from = self.salary.get('from', 0) or 0
            salary_to = self.salary.get('to', 0) or 0
            self._salary = (salary_from + salary_to) / 2 if salary_from or salary_to else 0.0
        else:
            # Если зарплата передана напрямую
            self._salary = self.salary if self.salary is not None else 0.0

        self._description = self.description or 'Описание отсутствует'
        self._validate_data()

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразование вакансии в словарь для сериализации
        """
        return {
            'title': self._title,
            'url': self._url,
            'salary': {
                'from': self.salary or 0,
                'to': None
            },
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

    def __init__(self):
        self._url = None

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
    def salary(self, value: Optional[float]) -> None:
        """
        Setter для свойства salary с валидацией

        :param value: Новое значение зарплаты
        """
        if value is not None and value < 0:
            raise ValueError("Зарплата не может быть отрицательной")
        self._salary = value if value is not None else 0.0


    @property
    def description(self) -> str:
        return self._description

    def __lt__(self, other: 'Vacancy') -> bool:
        """
        Сравнение вакансий по зарплате

        :param other: Другая вакансия для сравнения
        :return: Результат сравнения
        """
        if not isinstance(other, Vacancy):
            return NotImplemented

        # Безопасное сравнение зарплат
        return (self._salary or 0) < (other._salary or 0)


    def __repr__(self) -> str:
        """
        Строковое представление вакансии

        :return: Строка с информацией о вакансии
        """
        return f"Vacancy(title={self._title}, salary={self._salary})"

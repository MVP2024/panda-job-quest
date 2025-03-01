from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Vacancy:
    title: str
    url: str
    salary: Optional[float] = None
    description: str = "Описание отсутствует"

    def __post_init__(self):
        self._validate_data()

    def _validate_data(self):
        if not self.title:
            raise ValueError("Название вакансии не может быть пустым")

        if not self.url:
            raise ValueError("URL вакансии не может быть пустым")

        if self.salary is None:
            self.salary = 0.0

    def __lt__(self, other):
        """Сравнение вакансий по зарплате"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary < other.salary

    def __repr__(self):
        return f"Vacancy(title={self.title}, salary={self.salary})"

from typing import Any, Dict, List, Optional

import pytest

from utils.helpers import filter_vacancies_by_keyword, format_salary, sort_vacancies_by_salary


# Параметризация format_salary
@pytest.mark.parametrize(
    "salary, expected",
    [
        (None, "Зарплата не указана"),
        (float(1000), "1 000.00 руб."),
        (float(1000000), "1 000 000.00 руб."),
        (float(0), "0.00 руб."),
    ],
)
def test_format_salary(salary: Optional[float], expected: str) -> None:
    assert format_salary(salary) == expected


# Тесты filter_vacancies_by_keyword с параметризацией
@pytest.mark.parametrize(
    "keyword, expected_count",
    [
        ("python", 1),
        ("developer", 2),
        ("DEVELOPER", 2),
        ("machine", 1),
        ("backend", 1),
        ("", 0),  # Пустое ключевое слово
        ("non-existent", 0),
    ],
)
def test_filter_vacancies_by_keyword(
    helpers_sample_vacancies: List[Dict[str, Any]], keyword: str, expected_count: int
) -> None:
    filtered = filter_vacancies_by_keyword(helpers_sample_vacancies, keyword)
    assert len(filtered) == expected_count


def test_format_salary_with_decimal() -> None:
    """Тест форматирования зарплаты с десятичной частью"""
    assert format_salary(1234.56) == "1 234.56 руб."


def test_format_salary_large_number() -> None:
    """Тест форматирования очень больших чисел"""
    assert format_salary(1234567.89) == "1 234 567.89 руб."


def test_format_salary_negative_number() -> None:
    """Тест форматирования отрицательных чисел"""
    assert format_salary(-1000.0) == "-1 000.00 руб."


def test_sort_vacancies_by_salary(helpers_sample_vacancies: List[Dict[str, Any]]) -> None:
    # Сортировка по убыванию
    sorted_desc = sort_vacancies_by_salary(helpers_sample_vacancies)
    assert sorted_desc[0]["salary"] == 150000
    assert sorted_desc[-1]["salary"] == 100000

    # Сортировка по возрастанию
    sorted_asc = sort_vacancies_by_salary(helpers_sample_vacancies, reverse=False)
    assert sorted_asc[0]["salary"] == 100000
    assert sorted_asc[-1]["salary"] == 150000


def test_sort_vacancies_with_none_salary() -> None:
    vacancies: List[Dict[str, Any]] = [
        {"title": "Job1", "salary": None},
        {"title": "Job2", "salary": 50000},
        {"title": "Job3"},
    ]

    # Сортировка по убыванию
    sorted_desc = sort_vacancies_by_salary(vacancies)
    assert len(sorted_desc) == 3
    assert sorted_desc[0].get("salary", 0) == 50000


def test_filter_vacancies_empty_list() -> None:
    assert len(filter_vacancies_by_keyword([], "test")) == 0
    assert len(sort_vacancies_by_salary([])) == 0

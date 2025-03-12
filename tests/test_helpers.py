import pytest
from utils.helpers import format_salary, filter_vacancies_by_keyword, sort_vacancies_by_salary

# Параметризация
@pytest.mark.parametrize("salary, expected", [
    (None, "Зарплата не указана"),
    (1000, "1,000.00 руб."),
    (1000000, "1,000,000.00 руб.")
])
def test_format_salary(salary, expected):
    assert format_salary(salary) == expected

# Тесты с параметризацией
@pytest.mark.parametrize("keyword, expected_count", [
    ('python', 1),
    ('developer', 2),
    ('machine', 1),
    ('backend', 1),
    ('non-existent', 0)
])
def test_filter_vacancies_by_keyword(helpers_sample_vacancies, keyword, expected_count):
    filtered = filter_vacancies_by_keyword(helpers_sample_vacancies, keyword)
    assert len(filtered) == expected_count

# Тесты сортировки
def test_sort_vacancies_by_salary(helpers_sample_vacancies):
    # Сортировка по убыванию
    sorted_desc = sort_vacancies_by_salary(helpers_sample_vacancies)
    assert sorted_desc[0]['salary'] == 150000
    assert sorted_desc[-1]['salary'] == 100000

    # Сортировка по возрастанию
    sorted_asc = sort_vacancies_by_salary(helpers_sample_vacancies, reverse=False)
    assert sorted_asc[0]['salary'] == 100000
    assert sorted_asc[-1]['salary'] == 150000

# Тест с обработкой краевых случаев
def test_filter_vacancies_empty_list():
    assert len(filter_vacancies_by_keyword([], 'test')) == 0

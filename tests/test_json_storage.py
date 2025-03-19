import os
from typing import Any, Dict
from unittest.mock import Mock

from storage.json_storage import JSONStorage


def test_init_default() -> None:
    """Тест инициализации без параметров"""
    storage = JSONStorage()
    assert storage._filename.endswith("vacancies.json")
    assert os.path.exists(os.path.dirname(storage._filename))


def test_init_with_filename(temp_json_file: str) -> None:
    """Тест инициализации с указанием файла"""
    storage = JSONStorage(filename=temp_json_file)
    assert storage._filename == temp_json_file


def test_add_vacancy(json_storage: JSONStorage, sample_vacancy: Mock) -> None:
    """Тест добавления вакансии"""
    json_storage.add_vacancy(sample_vacancy)
    vacancies = json_storage.get_vacancies()
    assert len(vacancies) == 1
    assert vacancies[0]["name"] == "Python Developer"
    assert "Test description" in vacancies[0]["description"]


def test_get_vacancies_with_criteria(json_storage: JSONStorage, sample_vacancy: Mock) -> None:
    """Тест получения вакансий по критериям"""
    json_storage.add_vacancy(sample_vacancy)

    # Позитивный сценарий
    result_positive = json_storage.get_vacancies({"name": "Python"})
    assert len(result_positive) == 1

    # Негативный сценарий
    result_negative = json_storage.get_vacancies({"name": "Java"})
    assert len(result_negative) == 0


def test_delete_vacancy(json_storage: JSONStorage, sample_vacancy: Mock) -> None:
    """Тест удаления вакансии"""
    json_storage.add_vacancy(sample_vacancy)
    json_storage.delete_vacancy({"name": "Python Developer"})
    vacancies = json_storage.get_vacancies()
    assert len(vacancies) == 0


def test_get_vacancies_by_salary_range(json_storage: JSONStorage, sample_vacancy: Mock) -> None:
    """Тест получения вакансий по диапазону зарплат"""
    json_storage.add_vacancy(sample_vacancy)

    # Вакансия попадает в диапазон
    result_in_range = json_storage.get_vacancies_by_salary_range(50000, 150000)
    assert len(result_in_range) == 1

    # Вакансия не попадает в диапазон
    result_out_of_range = json_storage.get_vacancies_by_salary_range(200000, 300000)
    assert len(result_out_of_range) == 0


def test_get_vacancies_by_profession(json_storage: JSONStorage, sample_vacancy: Mock) -> None:
    """Тест получения вакансий по профессии"""
    modified_sample_vacancy = Mock()
    modified_sample_vacancy.to_dict.return_value = {
        "id": 1,
        "name": "Python Developer",
        "title": "Senior Python Developer",
        "description": "<p>Test description</p>",
        "salary": {"from": 100000, "to": 150000},
    }

    json_storage.add_vacancy(modified_sample_vacancy)

    # Нормальный сценарий
    result_positive = json_storage.get_vacancies_by_profession("Python")
    assert len(result_positive) == 1

    # Отрицательный сценарий
    result_negative = json_storage.get_vacancies_by_profession("Java")
    assert len(result_negative) == 0


def test_remove_html_tags_empty_string() -> None:
    """Тест удаления HTML-тегов из пустой строки"""
    clean_text = JSONStorage._remove_html_tags("")
    assert clean_text == ""


def test_remove_html_tags() -> None:
    """Тест удаления HTML-тегов"""
    html_text = "<p>Hello <b>World</b>!</p>"
    clean_text = JSONStorage._remove_html_tags(html_text)
    assert clean_text == "Hello World!"


def test_match_criteria() -> None:
    """Тест сопоставления критериев"""
    vacancy: Dict[str, Any] = {"name": "Python Developer", "description": "Senior level"}
    assert JSONStorage._match_criteria(vacancy, {"name": "Python"}) is True
    assert JSONStorage._match_criteria(vacancy, {"name": "Java"}) is False

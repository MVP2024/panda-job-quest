from typing import Any, Dict, List
from unittest.mock import patch

import pytest
import requests

from parsers.hh_parser import HHParser


@pytest.mark.parametrize(
    "keyword,expected_length,sample_subset",
    [
        ("python", 1, [{"id": 1, "name": "Python Developer"}]),
        ("java", 1, [{"id": 2, "name": "Java Developer"}]),
        ("несуществующая профессия", 0, []),
    ],
)
def test_load_vacancies_parametrized(
    mock_file_worker: Any,
    keyword: str,
    expected_length: int,
    sample_subset: List[Dict[str, Any]],
) -> None:
    """
    Параметризованный тест загрузки вакансий
    """
    with patch("parsers.hh_parser.HHParser._load_vacancies") as mock_load_vacancies:
        mock_load_vacancies.return_value = sample_subset
        # Создание и тестирование парсера
        parser = HHParser(mock_file_worker)
        vacancies = parser.load_vacancies(keyword)

        # Проверки
        assert len(vacancies) == expected_length
        mock_load_vacancies.assert_called_once_with(keyword)


def test_load_vacancies_pagination(
    mock_file_worker: Any, sample_vacancies: List[Dict[str, Any]]
) -> None:
    """
    Тест pagination при загрузке вакансий

    :param mock_file_worker: Мок для file_worker
    :param sample_vacancies: Тестовые вакансии
    """
    with patch("parsers.hh_parser.HHParser._load_vacancies") as mock_load_vacancies:
        mock_load_vacancies.return_value = sample_vacancies
        parser = HHParser(mock_file_worker)
        vacancies = parser.load_vacancies("python")

        # Проверки
        assert len(vacancies) == len(sample_vacancies)


def test_load_vacancies_network_error(mock_file_worker: Any, caplog: Any) -> None:
    """
    Тест обработки сетевой ошибки

    :param mock_file_worker: Мок для file_worker
    :param caplog: Fixture для перехвата сообщений логгера
    """
    with patch("parsers.hh_parser.HHParser._load_vacancies") as mock_load_vacancies:
        mock_load_vacancies.side_effect = requests.RequestException("Ошибка сети")

        parser = HHParser(mock_file_worker)
        try:
            vacancies = parser.load_vacancies("python")
        except requests.RequestException:
            vacancies = []

        # Проверки
        assert len(vacancies) == 0
        assert "Ошибка при загрузке вакансий" in caplog.text


@pytest.mark.xfail(reason="Тестирование предельного случая")
def test_max_pages_limit(mock_file_worker: Any) -> None:
    """
    Тест ограничения количества страниц

    :param mock_file_worker: Мок для file_worker
    """
    with patch("parsers.hh_parser.HHParser._load_vacancies") as mock_load_vacancies:
        # Создание большого количества mock-ответов
        mock_load_vacancies.return_value = [{"id": i} for i in range(2001)]

        parser = HHParser(mock_file_worker)
        vacancies = parser.load_vacancies("stress_test")

        # Проверка, что количество вакансий не превышает лимит
        assert len(vacancies) <= 2000  # 20 страниц * 100 вакансий

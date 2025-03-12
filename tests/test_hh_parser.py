from unittest.mock import Mock

import pytest
import requests
from parsers.hh_parser import HHParser


@pytest.mark.parametrize("keyword,expected_length,sample_subset", [
    ('python', 1, [{'id': 1, 'name': 'Python Developer'}]),
    ('java', 1, [{'id': 2, 'name': 'Java Developer'}]),
    ('несуществующая профессия', 0, [])
])
def test_load_vacancies_parametrized(
    mock_requests_get,
    mock_file_worker,
    keyword,
    expected_length,
    sample_subset
):
    """
    Параметризованный тест загрузки вакансий
    """
    # Создание mock-ответов для нескольких страниц
    mock_responses = [
        Mock(
            raise_for_status=lambda: None,
            json=lambda: {'items': sample_subset}
        ),
        Mock(
            raise_for_status=lambda: None,
            json=lambda: {'items': []}  # Пустой список для остановки пагинации
        )
    ]
    mock_requests_get.side_effect = mock_responses

    # Создание и тестирование парсера
    parser = HHParser(mock_file_worker)
    vacancies = parser.load_vacancies(keyword)

    # Проверки
    assert len(vacancies) == len(sample_subset)
    mock_requests_get.assert_called()
    mock_file_worker.save_vacancies.assert_called_once()


def test_load_vacancies_pagination(mock_requests_get, mock_file_worker, sample_vacancies):
    """
    Тест pagination при загрузке вакансий

    :param mock_requests_get: Мок для requests.get
    :param mock_file_worker: Мок для file_worker
    :param sample_vacancies: Тестовые вакансии
    """
    # Создание mock-ответов для нескольких страниц
    mock_responses = [
        Mock(
            raise_for_status=lambda: None,
            json=lambda: {'items': sample_vacancies[:1]}
        ),
        Mock(
            raise_for_status=lambda: None,
            json=lambda: {'items': sample_vacancies[1:2]}
        ),
        Mock(
            raise_for_status=lambda: None,
            json=lambda: {'items': []})
    ]
    mock_requests_get.side_effect = mock_responses

    parser = HHParser(mock_file_worker)
    vacancies = parser.load_vacancies('python')

    # Проверки
    assert len(vacancies) == 2
    assert mock_requests_get.call_count == 3


def test_load_vacancies_network_error(mock_requests_get, mock_file_worker, capfd):
    """
    Тест обработки сетевой ошибки

    :param mock_requests_get: Мок для requests.get
    :param mock_file_worker: Мок для file_worker
    :param capfd: Fixture для перехвата stdout
    """
    # Имитация сетевой ошибки
    mock_requests_get.side_effect = requests.RequestException("Ошибка сети")

    parser = HHParser(mock_file_worker)
    vacancies = parser.load_vacancies('python')

    # Проверки
    assert len(vacancies) == 0
    captured = capfd.readouterr()
    assert "Ошибка при загрузке вакансий" in captured.out


@pytest.mark.xfail(reason="Тестирование предельного случая")
def test_max_pages_limit(mock_requests_get, mock_file_worker):
    """
    Тест ограничения количества страниц

    :param mock_requests_get: Мок для requests.get
    :param mock_file_worker: Мок для file_worker
    """
    # Создание большого количества mock-ответов
    mock_responses = [
        Mock(
            raise_for_status=lambda: None,
            json=lambda: {'items': [{'id': i} for i in range(100)]}
        ) for _ in range(25)  # Больше 20 страниц
    ]
    mock_responses.append(Mock(raise_for_status=lambda: None, json=lambda: {'items': []}))
    mock_requests_get.side_effect = mock_responses

    parser = HHParser(mock_file_worker)
    vacancies = parser.load_vacancies('stress_test')

    # Проверка, что количество вакансий не превышает лимит
    assert len(vacancies) <= 2000  # 20 страниц * 100 вакансий

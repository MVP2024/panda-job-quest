#
# import requests
# from unittest.mock import patch
# from api.hh_api import HeadHunterAPI
# from api.abstract_api import AbstractAPI  # Добавьте этот импорт
#
# def test_hh_api_inherits_abstract_api():
#     """Проверка наследования от AbstractAPI"""
#     assert issubclass(HeadHunterAPI, AbstractAPI), "HeadHunterAPI должен наследоваться от AbstractAPI"
#
# def test_hh_api_initialization():
#     """Проверка инициализации HeadHunterAPI"""
#     hh_api = HeadHunterAPI()
#     assert hasattr(hh_api, '_headers'), "У экземпляра должен быть атрибут _headers"
#
# @patch('requests.get')
# def test_get_vacancies_success(mock_get):
#     """Тест успешного получения вакансий"""
#     # Подготовка mock-ответа
#     mock_response = mock_get.return_value
#     mock_response.status_code = 200
#     mock_response.json.return_value = {
#         'items': [
#             {'id': '1', 'name': 'Python Developer'},
#             {'id': '2', 'name': 'Data Scientist'}
#         ]
#     }
#
#     hh_api = HeadHunterAPI()
#     vacancies = hh_api.get_vacancies('python')
#
#     assert len(vacancies) == 2, "Должны быть возвращены вакансии"
#     assert vacancies[0]['name'] == 'Python Developer'
#     mock_get.assert_called_once()
#
# @patch('requests.get')
# def test_get_vacancies_network_error(mock_get):
#     """Тест обработки сетевой ошибки"""
#     mock_get.side_effect = requests.RequestException("Network error")
#
#     hh_api = HeadHunterAPI()
#     vacancies = hh_api.get_vacancies('python')
#
#     assert vacancies == [], "При ошибке сети должен возвращаться пустой список"
#
# def test_get_vacancies_method_signature():
#     """Проверка сигнатуры метода get_vacancies"""
#     from inspect import signature
#
#     sig = signature(HeadHunterAPI.get_vacancies)
#
#     assert 'search_query' in sig.parameters, "Должен быть параметр search_query"
#     assert 'per_page' in sig.parameters, "Должен быть параметр per_page"
#     assert sig.parameters['per_page'].default == 50, "Значение per_page по умолчанию должно быть 50"
#
#
# @patch('requests.get')
# def test_get_vacancies_params(mock_get):
#     """Проверка корректности параметров запроса"""
#     mock_response = mock_get.return_value
#     mock_response.status_code = 200
#     mock_response.json.return_value = {'items': []}
#
#     hh_api = HeadHunterAPI()
#     hh_api.get_vacancies('python', per_page=10)
#
#     # Проверяем, что requests.get был вызван с правильными параметрами
#     assert mock_get.call_count == 2
#
#     first_call = mock_get.call_args_list[0]
#     assert first_call[0][0] == 'https://api.hh.ru/vacancies'
#     assert first_call[1]['params'] == {'text': 'python', 'per_page': 10}
#
#     second_call = mock_get.call_args_list[1]
#     assert second_call[0][0] == 'https://hh.ru/search/vacancy'
#     assert second_call[1]['params'] == {'text': 'python', 'per_page': 10}
#
# @patch('requests.get')
# def test_get_vacancies_empty_result(mock_get):
#     """Тест обработки пустого результата"""
#     mock_response = mock_get.return_value
#     mock_response.status_code = 200
#     mock_response.json.return_value = {'items': []}
#
#     hh_api = HeadHunterAPI()
#     vacancies = hh_api.get_vacancies('nonexistent')
#
#     assert vacancies == [], "При пустом результате должен возвращаться пустой список"
#
#
# @patch('requests.get')
# def test_get_vacancies_headers(mock_get):
#     """Проверка корректности заголовков"""
#     mock_response = mock_get.return_value
#     mock_response.status_code = 200
#     mock_response.json.return_value = {'items': []}
#
#     hh_api = HeadHunterAPI()
#     hh_api.get_vacancies('python')
#
#     # Проверяем наличие обязательных заголовков
#     call_headers = mock_get.call_args[1]['headers']
#     assert 'User-Agent' in call_headers
#     assert 'Accept' in call_headers
#     assert call_headers['Accept'] == 'application/json'

import os
import pytest
import requests
from unittest.mock import patch, Mock
from api.hh_api import HeadHunterAPI


@pytest.mark.parametrize("client_id, client_secret", [
    ('test_id', 'test_secret'),
    (None, None)
])
def test_hh_api_initialization(client_id, client_secret, mock_env_vars):
    """Тест инициализации HeadHunterAPI с разными параметрами"""
    hh_api = HeadHunterAPI(client_id, client_secret)

    assert hasattr(hh_api, '_headers')
    assert '_public_api_endpoints' in hh_api.__dict__


def test_get_access_token(mock_env_vars):
    """Тест получения токена доступа"""
    with patch('requests.post') as mock_post:
        mock_response = Mock()
        mock_response.json.return_value = {'access_token': 'test_token'}
        mock_post.return_value = mock_response

        hh_api = HeadHunterAPI()
        token = hh_api._get_access_token()

        assert token == 'test_token'
        mock_post.assert_called_once()


def test_get_access_token_no_credentials():
    """Тест обработки отсутствия учетных данных"""
    with patch.dict(os.environ, clear=True):
        hh_api = HeadHunterAPI()
        with pytest.raises(ValueError, match="Отсутствуют учетные данные"):
            hh_api._get_access_token()


@pytest.mark.parametrize("search_query, per_page", [
    ('python', 50),
    ('data science', 10)
])
def test_get_vacancies_method(hh_api, search_query, per_page):
    """Тест метода получения вакансий с параметризацией"""
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {'items': [
            {'id': '1', 'name': f'{search_query} Developer'}
        ]}
        mock_get.return_value = mock_response

        vacancies = hh_api.get_vacancies(search_query, per_page)

        assert len(vacancies) > 0
        assert vacancies[0]['name'].lower().find(search_query.lower()) != -1


def test_get_vacancies_network_error(hh_api):
    """Тест обработки сетевой ошибки при получении вакансий"""
    with patch('requests.get', side_effect=requests.RequestException):
        vacancies = hh_api.get_vacancies('python')
        assert vacancies == []


def test_private_api_vacancies(mock_env_vars):
    """Тест получения вакансий через приватный API"""
    with patch('requests.get') as mock_get, \
        patch.object(HeadHunterAPI, '_get_access_token', return_value='test_token'):
        mock_response = Mock()
        mock_response.json.return_value = {'items': [{'id': '1', 'name': 'Test Vacancy'}]}
        mock_get.return_value = mock_response

        hh_api = HeadHunterAPI()
        vacancies = hh_api.get_vacancies('python')

        assert len(vacancies) > 0
        mock_get.assert_called_once()


def test_public_api_endpoints(hh_api):
    """Тест публичных API-эндпоинтов"""
    assert len(hh_api._public_api_endpoints) > 0
    assert all(isinstance(endpoint, str) for endpoint in hh_api._public_api_endpoints)
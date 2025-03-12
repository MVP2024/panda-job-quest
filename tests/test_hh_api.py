
import requests
from unittest.mock import patch
from api.hh_api import HeadHunterAPI
from api.abstract_api import AbstractAPI  # Добавьте этот импорт

def test_hh_api_inherits_abstract_api():
    """Проверка наследования от AbstractAPI"""
    assert issubclass(HeadHunterAPI, AbstractAPI), "HeadHunterAPI должен наследоваться от AbstractAPI"

def test_hh_api_initialization():
    """Проверка инициализации HeadHunterAPI"""
    hh_api = HeadHunterAPI()
    assert hasattr(hh_api, '_headers'), "У экземпляра должен быть атрибут _headers"

@patch('requests.get')
def test_get_vacancies_success(mock_get):
    """Тест успешного получения вакансий"""
    # Подготовка mock-ответа
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'items': [
            {'id': '1', 'name': 'Python Developer'},
            {'id': '2', 'name': 'Data Scientist'}
        ]
    }

    hh_api = HeadHunterAPI()
    vacancies = hh_api.get_vacancies('python')

    assert len(vacancies) == 2, "Должны быть возвращены вакансии"
    assert vacancies[0]['name'] == 'Python Developer'
    mock_get.assert_called_once()

@patch('requests.get')
def test_get_vacancies_network_error(mock_get):
    """Тест обработки сетевой ошибки"""
    mock_get.side_effect = requests.RequestException("Network error")

    hh_api = HeadHunterAPI()
    vacancies = hh_api.get_vacancies('python')

    assert vacancies == [], "При ошибке сети должен возвращаться пустой список"

def test_get_vacancies_method_signature():
    """Проверка сигнатуры метода get_vacancies"""
    from inspect import signature

    sig = signature(HeadHunterAPI.get_vacancies)

    assert 'search_query' in sig.parameters, "Должен быть параметр search_query"
    assert 'per_page' in sig.parameters, "Должен быть параметр per_page"
    assert sig.parameters['per_page'].default == 50, "Значение per_page по умолчанию должно быть 50"


@patch('requests.get')
def test_get_vacancies_params(mock_get):
    """Проверка корректности параметров запроса"""
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {'items': []}

    hh_api = HeadHunterAPI()
    hh_api.get_vacancies('python', per_page=10)

    # Проверяем, что requests.get был вызван с правильными параметрами
    assert mock_get.call_count == 2

    first_call = mock_get.call_args_list[0]
    assert first_call[0][0] == 'https://api.hh.ru/vacancies'
    assert first_call[1]['params'] == {'text': 'python', 'per_page': 10}

    second_call = mock_get.call_args_list[1]
    assert second_call[0][0] == 'https://hh.ru/search/vacancy'
    assert second_call[1]['params'] == {'text': 'python', 'per_page': 10}

@patch('requests.get')
def test_get_vacancies_empty_result(mock_get):
    """Тест обработки пустого результата"""
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {'items': []}

    hh_api = HeadHunterAPI()
    vacancies = hh_api.get_vacancies('nonexistent')

    assert vacancies == [], "При пустом результате должен возвращаться пустой список"


@patch('requests.get')
def test_get_vacancies_headers(mock_get):
    """Проверка корректности заголовков"""
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {'items': []}

    hh_api = HeadHunterAPI()
    hh_api.get_vacancies('python')

    # Проверяем наличие обязательных заголовков
    call_headers = mock_get.call_args[1]['headers']
    assert 'User-Agent' in call_headers
    assert 'Accept' in call_headers
    assert call_headers['Accept'] == 'application/json'

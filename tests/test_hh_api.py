
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

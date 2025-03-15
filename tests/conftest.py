from api.hh_api import HeadHunterAPI
from models.vacancy import Vacancy
from storage.abstract_storage import AbstractStorage
import pytest
from unittest.mock import Mock, patch
from storage.json_storage import JSONStorage


# фикстуры для class AbstractStorage(ABC)
class ConcreteStorage(AbstractStorage):
    def __init__(self):
        self.vacancies = []

    def add_vacancy(self, vacancy):
        self.vacancies.append(vacancy)

    def get_vacancies(self, criteria=None):
        return self.vacancies

    def delete_vacancy(self, criteria):
        pass

@pytest.fixture
def mock_file_worker():
    """Фикстура для создания mock объекта file_worker"""
    return Mock()

@pytest.fixture
def mock_requests_get():
    """Фикстура для мокинга requests.get"""
    with patch('requests.get') as mock_get:
        yield mock_get

@pytest.fixture
def sample_vacancies():
    """Фикстура с примером списка вакансий"""
    return [
        {'id': 1, 'name': 'Python Developer', 'salary': {'from': 100000, 'to': 150000}},
        {'id': 2, 'name': 'Data Scientist', 'salary': {'from': 120000, 'to': 180000}},
        {'id': 3, 'name': 'Backend Developer', 'salary': {'from': 90000, 'to': 130000}}
    ]

@pytest.fixture
def storage():
    """Фикстура для создания конкретной реализации хранилища"""
    return ConcreteStorage()


# фикстуры для json_storage
@pytest.fixture
def temp_json_file(tmpdir):
    """Создание временного JSON файла с использованием tmpdir"""
    return str(tmpdir.join('test_vacancies.json'))

@pytest.fixture
def json_storage(temp_json_file):
    """Фикстура для создания JSONStorage"""
    return JSONStorage(filename=temp_json_file)


@pytest.fixture
def sample_vacancy():
    """Фикстура с примером вакансии с использованием unittest.mock"""
    mock_vacancy = Mock()
    mock_vacancy.to_dict.return_value = {
        'id': 1,
        'name': 'Python Developer',
        'description': '<p>Test description</p>',
        'salary': {'from': 100000, 'to': 150000}
    }
    return mock_vacancy

# фикстуры для helpers
@pytest.fixture
def helpers_sample_vacancies():
    return [
        {
            'id': 1,
            'title': 'Python Developer',
            'description': 'Senior backend developer',
            'salary': 100000
        },
        {
            'id': 2,
            'title': 'Data Scientist',
            'description': 'Machine learning specialist',
            'salary': 150000
        },
        {
            'id': 3,
            'title': 'Java Developer',
            'description': 'Enterprise application development',
            'salary': 120000
        }
    ]

# фикстуры для vacancy
@pytest.fixture
def base_vacancy_data():
    """Базовые данные для создания вакансии"""
    return {
        'title': 'Python Developer',
        'url': 'https://example.com'
    }

@pytest.fixture
def vacancy_with_full_data(base_vacancy_data):
    """Фикстура с полными данными вакансии"""
    base_vacancy_data.update({
        'salary': 50000.0,
        'description': 'Требуется опытный разработчик'
    })
    return Vacancy(**base_vacancy_data)

# фикстуры для hh_api
@pytest.fixture
def hh_api():
    """Фикстура для создания экземпляра HeadHunterAPI"""
    return HeadHunterAPI()

@pytest.fixture
def mock_env_vars(monkeypatch):
    """Фикстура для установки mock-переменных окружения"""
    monkeypatch.setenv('HH_CLIENT_ID', 'test_client_id')
    monkeypatch.setenv('HH_CLIENT_SECRET', 'test_client_secret')

# фикстура для base_parser.py
@pytest.fixture
def base_parser_file_workers():
    """
    Фикстура с различными типами file_worker для BaseParser
    """
    return [
        None,  # Без file_worker
        Mock(),  # Простой Mock
        Mock(name='custom_file_worker'),  # Mock с именем
        Mock(save_vacancies=lambda x: print("Сохранение вакансий"))  # Mock с методом
    ]

@pytest.fixture
def base_parser_keywords():
    """
    Фикстура с ключевыми словами для тестирования BaseParser
    """
    return [
        'python',
        'java',
        'data science',
        '',  # Пустое ключевое слово
        None  # None значение
    ]

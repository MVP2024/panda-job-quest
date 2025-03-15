from typing import List, Dict, Any, Optional

from api.abstract_api import AbstractAPI
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
def abstract_api_class():
    """Фикстура для предоставления класса AbstractAPI"""
    return AbstractAPI


@pytest.fixture
def mock_concrete_api():
    """Фикстура для создания конкретной реализации AbstractAPI"""

    class ConcreteAPI(AbstractAPI):
        def get_vacancies(self, search_query: str, per_page: int = 50) -> List[Dict[str, Any]]:
            # Минимальная реализация для теста
            return [{'title': search_query}]

    return ConcreteAPI()

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
        'url': 'https://example.com',
        'employer': 'Test Company'  # Добавлено
    }

@pytest.fixture
def vacancy_with_full_data(base_vacancy_data):
    """Фикстура с полными данными вакансии"""
    base_vacancy_data.update({
        'salary': 50000.0,
        'description': 'Требуется опытный разработчик',
        'employer': 'Google'  # Добавлено
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

# фикстуры для abstract_storage
@pytest.fixture
def abstract_storage_class():
    """Фикстура для предоставления класса AbstractStorage"""
    return AbstractStorage


@pytest.fixture
def mock_concrete_storage():
    """Фикстура для создания конкретной реализации AbstractStorage"""

    class ConcreteStorage(AbstractStorage):
        def __init__(self):
            self.vacancies = []

        def add_vacancy(self, vacancy: Any) -> None:
            if vacancy is None:
                raise ValueError("Vacancy cannot be None")
            self.vacancies.append(vacancy)

        def get_vacancies(self, criteria: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
            if criteria is not None and not isinstance(criteria, dict):
                raise TypeError("Criteria must be a dictionary")

            if criteria:
                return [v for v in self.vacancies if all(v.get(k) == v for k, v in criteria.items())]
            return self.vacancies

        def delete_vacancy(self, criteria: Dict[str, Any]) -> None:
            if not criteria:
                raise ValueError("Criteria cannot be empty")

            # Корректная фильтрация с проверкой соответствия критериям
            self.vacancies = [
                vacancy for vacancy in self.vacancies
                if not all(
                    vacancy.get(key) == value
                    for key, value in criteria.items()
                )
            ]

    return ConcreteStorage()


@pytest.fixture
def sample_storage_vacancies():
    """Фикстура с примером списка вакансий для тестирования хранилища"""
    return [
        {'id': 1, 'title': 'Python Developer', 'salary': 100000},
        {'id': 2, 'title': 'Data Scientist', 'salary': 150000},
        {'id': 3, 'title': 'Backend Engineer', 'salary': 120000}
    ]

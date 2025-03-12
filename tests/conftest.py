import pytest
from storage.abstract_storage import AbstractStorage


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
import os
import pytest
from unittest.mock import Mock, patch
from storage.json_storage import JSONStorage


@pytest.fixture
def temp_json_file():
    """Создание временного JSON файла"""
    return os.path.join(os.path.dirname(__file__), 'test_vacancies.json')


@pytest.fixture
def json_storage(temp_json_file):
    """Фикстура для создания JSONStorage"""
    return JSONStorage(filename=temp_json_file)


@pytest.fixture
def sample_vacancy():
    """Фикстура с примером вакансии"""

    class MockVacancy:
        def to_dict(self):
            return {
                'id': 1,
                'name': 'Python Developer',
                'description': '<p>Test description</p>',
                'salary': {'from': 100000, 'to': 150000}
            }

    return MockVacancy()

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


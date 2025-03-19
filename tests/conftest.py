from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union, cast
from unittest.mock import Mock

import pytest
from _pytest.monkeypatch import MonkeyPatch

from api.abstract_api import AbstractAPI
from api.hh_api import HeadHunterAPI
from models.vacancy import Vacancy
from parsers.hh_parser import HHParser
from storage.abstract_storage import AbstractStorage
from storage.json_storage import JSONStorage

T = TypeVar("T")


class TestConcreteStorage(AbstractStorage):
    """Тестовая реализация абстрактного хранилища"""

    def __init__(self) -> None:
        super().__init__()
        self.vacancies: List[Any] = []

    def add_vacancy(self, vacancy: Any) -> None:
        """Добавление вакансии в хранилище"""
        if vacancy is None:
            raise ValueError("Vacancy cannot be None")
        self.vacancies.append(vacancy)

    def get_vacancies(self, criteria: Optional[Dict[str, Any]] = None) -> List[Any]:
        """Получение вакансий с опциональной фильтрацией"""
        if criteria is not None and not isinstance(criteria, dict):
            raise TypeError("Criteria must be a dictionary")

        if criteria:
            return [v for v in self.vacancies if all(v.get(k) == v for k, v in criteria.items())]
        return self.vacancies

    def delete_vacancy(self, criteria: Dict[str, Any]) -> None:
        """Удаление вакансий по критериям"""
        if not criteria:
            raise ValueError("Criteria cannot be empty")

        self.vacancies = [
            vacancy
            for vacancy in self.vacancies
            if not all(vacancy.get(key) == value for key, value in criteria.items())
        ]


def create_mock_api() -> AbstractAPI:
    """Создание мок-реализации AbstractAPI"""

    class ConcreteAPI(AbstractAPI):
        def get_vacancies(self, search_query: str, per_page: int = 50) -> List[Dict[str, Any]]:
            return [{"title": search_query}]

    return ConcreteAPI()


def create_mock_vacancy() -> Mock:
    """Создание мок-объекта вакансии"""
    mock_vacancy = Mock()
    mock_vacancy.to_dict.return_value = {
        "id": 1,
        "name": "Python Developer",
        "description": "<p>Test description</p>",
        "salary": {"from": 100000, "to": 150000},
    }
    return mock_vacancy


@pytest.fixture
def abstract_api_class() -> Type[AbstractAPI]:
    """Фикстура для предоставления класса AbstractAPI"""
    return AbstractAPI


@pytest.fixture
def mock_concrete_api() -> AbstractAPI:
    """Фикстура для создания конкретной реализации AbstractAPI"""
    return create_mock_api()


@pytest.fixture
def mock_file_worker() -> Mock:
    """Фикстура для создания mock объекта file_worker"""
    mock = Mock()
    mock.save_vacancies.return_value = None  # Добавляем заглушку для метода save_vacancies
    return mock


@pytest.fixture
def mock_requests_get() -> Callable[[List[Dict[str, Any]]], Mock]:
    """Фикстура для мокинга requests.get с возможностью задавать разные ответы"""

    def _mock_requests_get(responses: List[Dict[str, Any]]) -> Mock:
        mock = Mock()
        mock.side_effect = [
            Mock(raise_for_status=lambda: None, json=lambda r=response: r) for response in responses
        ]
        return mock

    return _mock_requests_get


@pytest.fixture
def temp_json_file(tmpdir: Any) -> str:
    """Создание временного JSON файла"""
    return str(tmpdir.join("test_vacancies.json"))


@pytest.fixture
def json_storage(temp_json_file: str) -> JSONStorage:
    """Фикстура для создания JSONStorage"""
    return JSONStorage(filename=temp_json_file)


@pytest.fixture
def base_vacancy_data() -> Dict[str, Union[str, float]]:
    """Базовые данные для создания вакансии"""
    return {"title": "Python Developer", "url": "https://example.com", "employer": "Test Company"}


@pytest.fixture
def vacancy_with_full_data(base_vacancy_data: Dict[str, Union[str, float]]) -> Vacancy:
    """Фикстура с полными данными вакансии"""
    full_data = base_vacancy_data.copy()
    full_data.update({"salary": 50000.0, "description": "Требуется опытный разработчик", "employer": "Google"})
    return Vacancy(**cast(Dict[str, Any], full_data))


@pytest.fixture
def mock_env_vars(monkeypatch: MonkeyPatch) -> None:
    """Установка mock-переменных окружения"""
    monkeypatch.setenv("HH_CLIENT_ID", "test_client_id")
    monkeypatch.setenv("HH_CLIENT_SECRET", "test_client_secret")


@pytest.fixture
def storage() -> TestConcreteStorage:
    """Создание конкретной реализации хранилища"""
    return TestConcreteStorage()


@pytest.fixture
def sample_vacancy() -> Mock:
    """Пример вакансии с использованием unittest.mock"""
    return create_mock_vacancy()


@pytest.fixture
def sample_vacancies() -> List[Dict[str, Any]]:
    """Пример списка вакансий"""
    return [
        {"id": 1, "name": "Python Developer", "salary": {"from": 100000, "to": 150000}},
        {"id": 2, "name": "Data Scientist", "salary": {"from": 120000, "to": 180000}},
        {"id": 3, "name": "Backend Developer", "salary": {"from": 90000, "to": 130000}},
    ]


@pytest.fixture
def helpers_sample_vacancies() -> List[Dict[str, Union[int, str]]]:
    """Образец вакансий для тестирования хелперов"""
    return [
        {"id": 1, "title": "Python Developer", "description": "Senior backend developer", "salary": 100000},
        {"id": 2, "title": "Data Scientist", "description": "Machine learning specialist", "salary": 150000},
        {"id": 3, "title": "Java Developer", "description": "Enterprise application development", "salary": 120000},
    ]


@pytest.fixture
def sample_storage_vacancies() -> List[Dict[str, Union[int, str]]]:
    """Образец вакансий для тестирования хранилища"""
    return [
        {"id": 1, "title": "Python Developer", "salary": 100000},
        {"id": 2, "title": "Data Scientist", "salary": 150000},
        {"id": 3, "title": "Backend Engineer", "salary": 120000},
    ]


@pytest.fixture
def sample_vacancies_user_interaction() -> List[Vacancy]:
    """Образец вакансий для тестирования взаимодействия с пользователем"""
    return [
        Vacancy(
            title="Python Developer",
            url="https://example.com/1",
            salary=100000,
            description="Крутая вакансия",
            employer="Google",
        ),
        Vacancy(
            title="Data Scientist",
            url="https://example.com/2",
            salary=120000,
            description="Аналитика данных",
            employer="Яндекс",
        ),
    ]


@pytest.fixture
def mock_input_sequence() -> Callable[[List[str]], List[str]]:
    """Создание последовательности пользовательского ввода"""

    def _create_input_sequence(choices: List[str]) -> List[str]:
        return choices

    return _create_input_sequence


@pytest.fixture
def mock_api_data() -> List[Dict[str, Any]]:
    """Mock-данные API"""
    return [
        {
            "name": "Python Developer",
            "alternate_url": "https://example.com",
            "salary": {"from": 100000},
            "snippet": {"requirement": "Test description"},
            "employer": {"name": "Test Company"},
        }
    ]


@pytest.fixture
def hh_api() -> HeadHunterAPI:
    """Фикстура для создания экземпляра HeadHunterAPI."""
    return HeadHunterAPI()


@pytest.fixture
def hh_parser(mock_file_worker: Mock) -> HHParser:
    """Фикстура для создания экземпляра HHParser с замокированным file_worker."""
    return HHParser(file_worker=mock_file_worker)

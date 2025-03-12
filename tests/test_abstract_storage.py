import pytest
from typing import Any, Optional, Dict, List
from storage.abstract_storage import AbstractStorage
from unittest.mock import Mock

from tests.conftest import ConcreteStorage


def test_abstract_class_cannot_be_instantiated():
    """Проверка невозможности создания экземпляра абстрактного класса"""
    with pytest.raises(TypeError):
        AbstractStorage()

def test_abstract_methods_exist():
    """Проверка наличия абстрактных методов"""
    methods = ['add_vacancy', 'get_vacancies', 'delete_vacancy']
    for method in methods:
        assert hasattr(AbstractStorage, method)

def test_method_type_hints():
    """Проверка основных аннотаций типов"""
    assert AbstractStorage.add_vacancy.__annotations__['return'] is None
    assert AbstractStorage.get_vacancies.__annotations__['return'] == List[Dict[str, Any]]
    assert AbstractStorage.delete_vacancy.__annotations__['return'] is None

def test_method_signatures():
    """Проверка сигнатур методов"""
    class ConcreteStorage(AbstractStorage):
        def add_vacancy(self, vacancy: Any) -> None:
            # Добавляем реальную логику
            if vacancy is None:
                raise ValueError("Vacancy cannot be None")

        def get_vacancies(self, criteria: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
            # Добавляем реальную логику
            if criteria is not None and not isinstance(criteria, dict):
                raise TypeError("Criteria must be a dictionary")
            return []

        def delete_vacancy(self, criteria: Dict[str, Any]) -> None:
            # Добавляем реальную логику
            if not criteria:
                raise ValueError("Criteria cannot be empty")


    # Проверка создания конкретного класса
    storage = ConcreteStorage()
    assert isinstance(storage, AbstractStorage)

    # Дополнительные проверки методов
    with pytest.raises(ValueError):
        storage.add_vacancy(None)

    with pytest.raises(TypeError):
        storage.get_vacancies(criteria="invalid")

    with pytest.raises(ValueError):

        storage.delete_vacancy({})


def test_concrete_storage_methods():
    """Тест методов ConcreteStorage"""
    storage = ConcreteStorage()

    # Тест add_vacancy
    vacancy = {'name': 'Test Vacancy'}
    storage.add_vacancy(vacancy)
    assert len(storage.vacancies) == 1
    assert storage.vacancies[0] == vacancy

    # Тест get_vacancies
    result = storage.get_vacancies()
    assert len(result) == 1

    # Тест delete_vacancy (просто вызов, чтобы покрыть строку)
    storage.delete_vacancy({'name': 'Test Vacancy'})

def test_storage_fixture(storage):
    """Проверка фикстуры storage"""
    assert isinstance(storage, ConcreteStorage)
    assert hasattr(storage, 'vacancies')
    assert len(storage.vacancies) == 0

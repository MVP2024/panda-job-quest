from inspect import signature
from typing import Any, Dict, List

import pytest

from api.abstract_api import AbstractAPI


class MockAPI(AbstractAPI):
    def get_vacancies(self, search_query: str, per_page: int = 50) -> List[Dict[str, Any]]:
        return []


def test_abstract_class_cannot_be_instantiated() -> None:
    """Проверка невозможности создания экземпляра абстрактного класса"""
    with pytest.raises(TypeError):
        AbstractAPI()  # type: ignore


def test_mock_api_can_be_instantiated() -> None:
    """Проверка возможности создания экземпляра подкласса"""
    api = MockAPI()
    assert isinstance(api, MockAPI)  # Убедитесь, что экземпляр корректный


class ConcreteAPI(AbstractAPI):
    """
    Конкретная реализация AbstractAPI для целей тестирования.
    """

    def get_vacancies(self, search_query: str, per_page: int = 50) -> List[Dict[str, Any]]:
        """
        Реализация абстрактного метода get_vacancies.
        """
        return [{"title": search_query}]


def test_abstract_method_exists() -> None:
    """Проверка наличия абстрактного метода get_vacancies"""
    assert hasattr(AbstractAPI, "get_vacancies"), "Метод get_vacancies должен существовать"


def test_method_signature() -> None:
    """Проверка сигнатуры метода get_vacancies"""
    method = AbstractAPI.get_vacancies
    sig = signature(method)

    # Проверка параметров
    parameters = list(sig.parameters.keys())
    assert parameters == ["self", "search_query", "per_page"], "Неверная сигнатура метода"

    # Проверка аннотаций типов
    annotations = method.__annotations__
    assert annotations["search_query"] == str, "search_query должен быть str"
    assert annotations["per_page"] == int, "per_page должен быть int"
    assert annotations["return"] == List[Dict[str, Any]], "Неверный тип возвращаемого значения"


def test_logger_exists() -> None:
    """Проверка наличия логгера в классе"""
    # Создаем экземпляр конкретного класса, реализующего AbstractAPI
    api_instance = ConcreteAPI()

    assert hasattr(api_instance, "logger"), "У экземпляра класса должен быть атрибут logger"
    assert api_instance.logger is not None, "Логгер не может быть None"


def test_docstring_exists() -> None:
    """Проверка наличия и непустого docstring"""
    assert AbstractAPI.__doc__ is not None, "У класса должен быть docstring"
    assert len(AbstractAPI.__doc__.strip()) > 0, "Docstring не должен быть пустым"


def test_method_docstring() -> None:
    """Проверка docstring метода get_vacancies"""
    method = AbstractAPI.get_vacancies
    assert method.__doc__ is not None, "У метода должен быть docstring"
    assert len(method.__doc__.strip()) > 0, "Docstring метода не должен быть пустым"

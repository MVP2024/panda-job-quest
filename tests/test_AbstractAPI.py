import pytest
from api.abstract_api import AbstractAPI
from typing import List, Dict, Any
from inspect import signature


def test_abstract_class_cannot_be_instantiated():
    """Проверка невозможности создания экземпляра абстрактного класса"""
    with pytest.raises(TypeError):
        AbstractAPI()


def test_abstract_method_exists():
    """Проверка наличия абстрактного метода get_vacancies"""
    assert hasattr(AbstractAPI, 'get_vacancies'), "Метод get_vacancies должен существовать"


def test_method_signature():
    """Проверка сигнатуры метода get_vacancies"""
    method = AbstractAPI.get_vacancies
    sig = signature(method)

    # Проверка параметров
    parameters = list(sig.parameters.keys())
    assert parameters == ['self', 'search_query', 'per_page'], "Неверная сигнатура метода"

    # Проверка аннотаций типов
    annotations = method.__annotations__
    assert annotations['search_query'] == str, "search_query должен быть str"
    assert annotations['per_page'] == int, "per_page должен быть int"
    assert annotations['return'] == List[Dict[str, Any]], "Неверный тип возвращаемого значения"


def test_logger_exists():
    """Проверка наличия логгера в классе"""
    assert hasattr(AbstractAPI, 'logger'), "У класса должен быть атрибут logger"
    assert AbstractAPI.logger is not None, "Логгер не может быть None"


def test_docstring_exists():
    """Проверка наличия и непустого docstring"""
    assert AbstractAPI.__doc__ is not None, "У класса должен быть docstring"
    assert len(AbstractAPI.__doc__.strip()) > 0, "Docstring не должен быть пустым"


def test_method_docstring():
    """Проверка docstring метода get_vacancies"""
    method = AbstractAPI.get_vacancies
    assert method.__doc__ is not None, "У метода должен быть docstring"
    assert len(method.__doc__.strip()) > 0, "Docstring метода не должен быть пустым"

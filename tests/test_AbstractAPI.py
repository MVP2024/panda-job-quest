import pytest
from api.abstract_api import AbstractAPI


def test_abstract_method_exists():
    """Проверка наличия абстрактного метода get_vacancies"""
    assert hasattr(AbstractAPI, 'get_vacancies'), "Метод get_vacancies должен существовать"

def test_cannot_instantiate_abstract_class():
    """Проверка невозможности создания экземпляра абстрактного класса"""
    with pytest.raises(TypeError):
        AbstractAPI()

def test_method_signature():
    """Проверка сигнатуры метода get_vacancies"""
    method = AbstractAPI.get_vacancies
    assert callable(method), "get_vacancies должен быть вызываемым методом"

    # Проверка аннотаций типов
    from inspect import signature
    sig = signature(method)
    assert len(sig.parameters) >= 2, "Метод должен принимать как минимум search_query"
    assert 'search_query' in sig.parameters, "Первый параметр должен быть search_query"
    assert 'per_page' in sig.parameters, "Должен быть параметр per_page"
from abc import ABC
from inspect import signature
from typing import Any, Dict, List, Optional, Type, Union

import pytest

from storage.abstract_storage import AbstractStorage


@pytest.fixture
def abstract_storage_class() -> Type[AbstractStorage]:
    return AbstractStorage


@pytest.fixture
def mock_concrete_storage() -> AbstractStorage:
    """Фикстура для создания конкретной реализации AbstractStorage"""
    class ConcreteStorage(AbstractStorage):
        def __init__(self) -> None:
            super().__init__()
            self.vacancies: List[Dict[str, Any]] = []

        def add_vacancy(self, vacancy: Any) -> None:
            if vacancy is None:
                raise ValueError("Vacancy cannot be None")
            self.vacancies.append(vacancy)

        def get_vacancies(self, criteria: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
            if criteria is not None and not isinstance(criteria, dict):
                raise TypeError("Criteria must be a dictionary")
            if criteria:
                return [v for v in self.vacancies if all(criteria[k] == v.get(k) for k in criteria)]
            return self.vacancies

        def delete_vacancy(self, criteria: Dict[str, Any]) -> None:
            if not criteria:
                raise ValueError("Criteria cannot be empty")
            self.vacancies = [v for v in self.vacancies if not all(criteria[k] == v.get(k) for k in criteria)]

    return ConcreteStorage()


def test_abstract_class_structure(abstract_storage_class: Type[AbstractStorage]) -> None:
    """Проверка структуры абстрактного класса"""
    assert issubclass(abstract_storage_class, ABC), "Должен быть абстрактным классом"
    assert hasattr(abstract_storage_class, "__abstractmethods__"), "Должен иметь абстрактные методы"


@pytest.mark.parametrize("method_name", ["add_vacancy", "get_vacancies", "delete_vacancy"])
def test_abstract_method_signatures(method_name: str) -> None:
    """Параметризованная проверка сигнатур абстрактных методов"""
    method = getattr(AbstractStorage, method_name)
    sig = signature(method)

    # Проверка базовых параметров
    parameters = list(sig.parameters.keys())
    assert parameters[0] == "self", f"Первый параметр {method_name} должен быть self"


@pytest.mark.parametrize(
    "method_name, params, expected_exception",
    [
        ("add_vacancy", [None], ValueError),
        ("get_vacancies", ["invalid"], TypeError),
        ("get_vacancies", [{"key": "value"}], None),
        ("delete_vacancy", [{}], ValueError),
    ],
)
def test_method_parameter_validation(
    mock_concrete_storage: AbstractStorage,
    method_name: str,
    params: List[Any],
    expected_exception: Optional[Type[Exception]],
) -> None:
    """
    Параметризованный тест валидации параметров методов
    """
    method = getattr(mock_concrete_storage, method_name)

    if expected_exception:
        with pytest.raises(expected_exception):
            method(*params)
    else:
        # Для методов без явного исключения проверяем, что метод вызывается без ошибок
        method(*params)


def test_method_type_hints() -> None:
    """Проверка аннотаций типов методов"""
    # add_vacancy
    add_vacancy_hints = AbstractStorage.add_vacancy.__annotations__
    assert add_vacancy_hints["vacancy"] == Any
    assert add_vacancy_hints["return"] is None

    # get_vacancies
    get_vacancies_hints = AbstractStorage.get_vacancies.__annotations__
    assert get_vacancies_hints["criteria"] == Optional[Dict[str, Any]]
    assert get_vacancies_hints["return"] == List[Dict[str, Any]]

    # delete_vacancy
    delete_vacancy_hints = AbstractStorage.delete_vacancy.__annotations__
    assert delete_vacancy_hints["criteria"] == Dict[str, Any]
    assert delete_vacancy_hints["return"] is None


def test_docstrings_exist() -> None:
    """Проверка наличия и непустых docstring"""
    # Docstring класса
    assert AbstractStorage.__doc__ is not None
    assert len(AbstractStorage.__doc__.strip()) > 0

    # Docstring методов
    methods = ["add_vacancy", "get_vacancies", "delete_vacancy"]
    for method_name in methods:
        method = getattr(AbstractStorage, method_name)
        assert method.__doc__ is not None
        assert len(method.__doc__.strip()) > 0


def test_concrete_storage_creation(
    mock_concrete_storage: AbstractStorage, sample_storage_vacancies: List[Dict[str, Union[int, str]]]
) -> None:
    """Тест создания и базовых операций конкретной реализации"""
    # Добавление вакансий
    for vacancy in sample_storage_vacancies:
        mock_concrete_storage.add_vacancy(vacancy)

    # Проверка добавления
    assert len(mock_concrete_storage.vacancies or []) == len(sample_storage_vacancies)

    # Получение всех вакансий
    all_vacancies = mock_concrete_storage.get_vacancies()
    assert len(all_vacancies) == len(sample_storage_vacancies)

    # Удаление вакансии
    mock_concrete_storage.delete_vacancy({"title": "Python Developer"})
    assert len(mock_concrete_storage.vacancies or []) == len(sample_storage_vacancies) - 1

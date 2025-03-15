import logging
from abc import ABC

import pytest
from unittest.mock import Mock
from parsers.base_parser import BaseParser


# Один класс ConcreteParser для всех тестов
class ConcreteParser(BaseParser):
    def load_vacancies(self, keyword):
        # Минимальная реализация для теста
        if not keyword:
            return []
        return [{'title': f'Vacancy for {keyword}'}]


# тест для __init__ класса BaseParser(ABC)
def test_base_parser_init_without_file_worker():
    """
    Тест инициализации парсера без file_worker
    """
    parser = ConcreteParser()
    assert parser.file_worker is None


def test_base_parser_init_with_file_worker():
    """
    Тест инициализации парсера с file_worker
    """
    mock_file_worker = Mock()
    parser = ConcreteParser(file_worker=mock_file_worker)
    assert parser.file_worker == mock_file_worker


@pytest.mark.parametrize("file_worker", [
    None,
    Mock(),
    Mock(name='custom_file_worker')
])
def test_base_parser_init_parametrized(file_worker):
    """
    Параметризованный тест инициализации с различными типами file_worker
    """
    parser = ConcreteParser(file_worker=file_worker)
    assert parser.file_worker == file_worker


# тесты для @abstractmethod def load_vacancies класса BaseParser(ABC)
def test_base_parser_abstract_method():
    """
    Проверка, что BaseParser является абстрактным классом
    """
    with pytest.raises(TypeError):
        BaseParser()


def test_load_vacancies_method_signature():
    """
    Проверка сигнатуры метода load_vacancies
    """
    from inspect import signature

    sig = signature(BaseParser.load_vacancies)
    assert len(sig.parameters) == 2  # self и keyword
    assert 'keyword' in sig.parameters


@pytest.mark.parametrize("keyword,expected", [
    ('python', [{'title': 'Vacancy for python'}]),
    ('java', [{'title': 'Vacancy for java'}]),
    ('', []),
    (None, [])
])
def test_concrete_parser_load_vacancies(keyword, expected):
    """
    Параметризованный тест загрузки вакансий
    """
    parser = ConcreteParser()
    result = parser.load_vacancies(keyword)
    assert result == expected


def test_load_vacancies_raises_not_implemented():
    """
    Проверка, что вызов load_vacancies на абстрактном классе вызывает ошибку
    """
    # Вариант 1: Минимальная реализация абстрактного метода
    class IncompleteParser(BaseParser):
        def load_vacancies(self, keyword):
            return []

    parser = IncompleteParser()
    result = parser.load_vacancies('test')
    assert result == []


def test_base_parser_logger_configuration():
    """
    Тест конфигурации логгера базового парсера
    """
    parser = ConcreteParser()

    # Проверяем настройки логгера
    assert parser.logger is not None
    assert isinstance(parser.logger, logging.Logger)
    assert parser.logger.name == 'parsers.base_parser'
    assert parser.logger.level == logging.DEBUG


def test_base_parser_file_worker_type_handling():
    """
    Тест обработки различных типов file_worker
    """

    class CustomFileWorker:
        def save_vacancies(self, vacancies):
            pass

    # Тест с стандартным file_worker
    custom_worker = CustomFileWorker()
    parser = ConcreteParser(file_worker=custom_worker)
    assert parser.file_worker == custom_worker

    # Тест с lambda-функцией в качестве file_worker
    lambda_worker = lambda x: print("Сохранение вакансий")
    parser_lambda = ConcreteParser(file_worker=lambda_worker)
    assert parser_lambda.file_worker == lambda_worker


def test_base_parser_logger_debug_message(caplog):
    """
    Тест debug-сообщения при инициализации
    """
    caplog.set_level(logging.DEBUG)

    mock_file_worker = Mock(name='test_debug_worker')
    ConcreteParser(file_worker=mock_file_worker)

    # Проверяем debug-сообщение
    debug_logs = [record for record in caplog.records if record.levelno == logging.DEBUG]
    assert any("Инициализация базового парсера" in record.message for record in debug_logs)
    assert any("test_debug_worker" in record.message for record in debug_logs)


def test_base_parser_abstract_method_contract():
    """
    Проверка контракта абстрактного метода load_vacancies
    """
    from inspect import signature

    # Проверяем сигнатуру метода
    sig = signature(BaseParser.load_vacancies)
    assert len(sig.parameters) == 2  # self и keyword
    assert list(sig.parameters.keys()) == ['self', 'keyword']

    # Проверяем, что нельзя создать экземпляр абстрактного класса без реализации
    with pytest.raises(TypeError):
        class MinimalParser(BaseParser, ABC):
            pass

        MinimalParser()


def test_load_vacancies_abstract_method_raises_error():
    """
    Проверка, что вызов load_vacancies на абстрактном классе BaseParser
    вызывает NotImplementedError
    """

    class MinimalParser(BaseParser, ABC):
        # Без реализации load_vacancies
        pass

    with pytest.raises(TypeError):
        MinimalParser()


def test_load_vacancies_method_contract():
    """
    Проверка контракта метода load_vacancies
    """
    from inspect import signature

    # Проверяем сигнатуру метода
    sig = signature(BaseParser.load_vacancies)

    # Проверяем количество параметров
    assert len(sig.parameters) == 2, "Метод должен иметь два параметра: self и keyword"

    # Проверяем имена параметров
    assert list(sig.parameters.keys()) == ['self', 'keyword'], "Неверные имена параметров"


def test_load_vacancies_method_documentation():
    """
    Проверка наличия документации для абстрактного метода
    """
    doc = BaseParser.load_vacancies.__doc__

    assert doc is not None, "Метод должен иметь документацию"
    assert "keyword" in doc, "Документация должна описывать параметр keyword"
    assert "Список вакансий" in doc, "Документация должна описывать возвращаемое значение"

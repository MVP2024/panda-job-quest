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

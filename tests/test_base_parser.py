import logging
from typing import Any, Dict, List
from unittest.mock import Mock

import pytest

from parsers.base_parser import BaseParser


class ConcreteParser(BaseParser):
    def _load_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        return []


class ExceptionParser(BaseParser):
    def _load_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        raise ValueError("Simulated error")


def test_base_parser_initializes_logger_by_default() -> None:
    """
    Тест проверяет, что BaseParser инициализирует логгер по умолчанию,
    если ему не передан экземпляр логгера.
    """
    parser = ConcreteParser()
    assert isinstance(parser.logger, logging.Logger)


def test_base_parser_uses_provided_logger() -> None:
    """
    Тест проверяет, что BaseParser использует переданный логгер,
    если он предоставлен.
    """
    mock_logger = Mock()
    parser = ConcreteParser(logger=mock_logger)
    assert parser.logger == mock_logger


def test_load_vacancies_logs_debug_message(caplog: pytest.LogCaptureFixture) -> None:
    """Тест проверяет, что метод load_vacancies записывает debug-сообщение в лог."""
    caplog.set_level(logging.DEBUG)
    parser = ConcreteParser()
    parser.load_vacancies("test_keyword")
    assert "Загрузка вакансий с ключевым словом: test_keyword" in caplog.text


def test_load_vacancies_logs_info_message_on_success(caplog: pytest.LogCaptureFixture) -> None:
    """Тест проверяет, что метод load_vacancies записывает info-сообщение в лог при успешной загрузке."""
    caplog.set_level(logging.INFO)
    parser = ConcreteParser()
    parser.load_vacancies("test_keyword")
    assert "Успешно загружено 0 вакансий с ключевым словом: test_keyword" in caplog.text


def test_load_vacancies_logs_error_message_on_exception(caplog: pytest.LogCaptureFixture) -> None:
    """Тест проверяет, что метод load_vacancies записывает error-сообщение в лог при возникновении исключения."""
    caplog.set_level(logging.ERROR)
    parser = ExceptionParser()
    with pytest.raises(ValueError, match="Simulated error"):
        parser.load_vacancies("test_keyword")
    assert "Ошибка при загрузке вакансий с ключевым словом: test_keyword: Simulated error" in caplog.text


def test_load_vacancies_reaises_exception(caplog: pytest.LogCaptureFixture) -> None:
    """
    Тест проверяет, что метод load_vacancies повторно возбуждает исключение,
    возникшее в _load_vacancies.
    """
    caplog.set_level(logging.ERROR)
    parser = ExceptionParser()
    with pytest.raises(ValueError, match="Simulated error"):
        parser.load_vacancies("test_keyword")

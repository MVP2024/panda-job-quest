import os
from typing import Any, Optional
from unittest.mock import Mock, patch

import pytest
import requests

from api.hh_api import HeadHunterAPI


@pytest.mark.parametrize("client_id, client_secret", [("test_id", "test_secret"), (None, None)])
def test_hh_api_initialization(client_id: Optional[str], client_secret: Optional[str], mock_env_vars: Any) -> None:
    """Тест инициализации HeadHunterAPI с разными параметрами"""
    hh_api = HeadHunterAPI(client_id, client_secret)

    assert hasattr(hh_api, "_headers")
    assert "_public_api_endpoints" in hh_api.__dict__


def test_get_access_token(mock_env_vars: Any) -> None:
    """Тест получения токена доступа"""
    with patch("requests.post") as mock_post:
        mock_response = Mock()
        mock_response.json.return_value = {"access_token": "test_token"}
        mock_post.return_value = mock_response

        hh_api = HeadHunterAPI()
        token = hh_api._get_access_token()

        assert token == "test_token"
        mock_post.assert_called_once()


def test_get_access_token_no_credentials() -> None:
    """Тест обработки отсутствия учетных данных"""
    with patch.dict(os.environ, clear=True):
        hh_api = HeadHunterAPI()
        with pytest.raises(ValueError, match="Отсутствуют учетные данные"):
            hh_api._get_access_token()


@pytest.mark.parametrize("search_query, per_page", [("python", 50), ("data science", 10)])
def test_get_vacancies_method(hh_api: HeadHunterAPI, search_query: str, per_page: int) -> None:
    """Тест метода получения вакансий с параметризацией"""
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {"items": [{"id": "1", "name": f"{search_query} Developer"}]}
        mock_get.return_value = mock_response

        vacancies = hh_api.get_vacancies(search_query, per_page)

        assert len(vacancies) > 0
        assert vacancies[0]["name"].lower().find(search_query.lower()) != -1


def test_get_vacancies_network_error(hh_api: HeadHunterAPI) -> None:
    """Тест обработки сетевой ошибки при получении вакансий"""
    with patch("requests.get", side_effect=requests.RequestException):
        vacancies = hh_api.get_vacancies("python")
        assert vacancies == []


def test_private_api_vacancies(mock_env_vars: Any) -> None:
    """Тест получения вакансий через приватный API"""
    with (patch("requests.get")
          as mock_get, patch.object(HeadHunterAPI, "_get_access_token", return_value="test_token")):
        mock_response = Mock()
        mock_response.json.return_value = {"items": [{"id": "1", "name": "Test Vacancy"}]}
        mock_get.return_value = mock_response

        hh_api = HeadHunterAPI()
        vacancies = hh_api.get_vacancies("python")

        assert len(vacancies) > 0
        mock_get.assert_called_once()


def test_public_api_endpoints(hh_api: HeadHunterAPI) -> None:
    """Тест публичных API-эндофитов"""
    assert len(hh_api._public_api_endpoints) > 0
    assert all(isinstance(endpoint, str) for endpoint in hh_api._public_api_endpoints)

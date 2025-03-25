from typing import Any, Dict, List
from unittest.mock import patch

from models.vacancy import Vacancy
from src.user_interaction import display_vacancies, main_menu


def test_display_vacancies_empty(capsys: Any) -> None:
    """Тест отображения пустого списка вакансий"""
    display_vacancies([])
    captured = capsys.readouterr()
    assert "Вакансии не найдены" in captured.out


def test_display_vacancies_with_data(capsys: Any, sample_vacancies_user_interaction: List[Vacancy]) -> None:
    """Тест отображения вакансий"""
    display_vacancies(sample_vacancies_user_interaction)
    captured = capsys.readouterr()

    assert "Python Developer" in captured.out
    assert "Data Scientist" in captured.out
    assert "Google" in captured.out
    assert "Яндекс" in captured.out


class TestMainMenu:
    def test_main_menu_flow(self, mock_input_sequence: Any, mock_api_data: List[Dict[str, Any]]) -> None:
        """
        Комплексный тест потока main_menu
        Проверяем основной сценарий поиска вакансий
        """
        input_sequence = mock_input_sequence(["1", "python", "4"])

        with (
            patch("builtins.input", side_effect=input_sequence),
            patch("src.user_interaction.HeadHunterAPI.get_vacancies", return_value=mock_api_data)
            as mock_get_vacancies,
            patch("src.user_interaction.JSONStorage.add_vacancy") as mock_add_vacancy,
            patch("src.user_interaction.display_vacancies") as mock_display,
        ):
            main_menu()

            # Проверяем вызовы методов
            mock_get_vacancies.assert_called_once_with("python")
            assert mock_add_vacancy.call_count > 0
            mock_display.assert_called_once()

    def test_main_menu_invalid_choice(self, mock_input_sequence: Any) -> None:
        """
        Тест обработки некорректного выбора
        """
        input_sequence = mock_input_sequence(["5", "4"])

        with (
            patch("builtins.input", side_effect=input_sequence),
            patch("src.user_interaction.HeadHunterAPI"),
            patch("src.user_interaction.JSONStorage"),
            patch("builtins.print") as mock_print,
        ):
            main_menu()

            # Проверяем вывод сообщения о неверном выборе
            mock_print.assert_any_call("Неверный выбор. Попробуйте снова.")

    def test_main_menu_top_vacancies(self, mock_input_sequence: Any) -> None:
        """
        Тест получения топ вакансий
        """
        input_sequence = mock_input_sequence(["2", "1", "4"])

        with (
            patch("builtins.input", side_effect=input_sequence),
            patch("src.user_interaction.HeadHunterAPI"),
            patch(
                "src.user_interaction.JSONStorage.get_vacancies",
                return_value=[
                    {
                        "title": "Python Developer",
                        "salary": 100000,
                        "employer": "Google",
                        "url": "https://example.com/1",
                        "description": "Python developer description",
                    },
                    {
                        "title": "Data Scientist",
                        "salary": 150000,
                        "employer": "Яндекс",
                        "url": "https://example.com/2",
                        "description": "Data scientist description",
                    },
                ],
            ) as _,  # Используем _, чтобы подавить предупреждение
            patch("src.user_interaction.display_vacancies") as mock_display,
        ):
            main_menu()

            # Проверяем вызов display_vacancies
            mock_display.assert_called_once()

            # Проверяем аргументы вызова
            args, _ = mock_display.call_args
            sorted_vacancies = args[0]

            # Проверяем сортировку по зарплате
            assert sorted_vacancies[0].title == "Data Scientist"
            assert sorted_vacancies[0].salary == 150000

    def test_main_menu_search_by_keyword(self, mock_input_sequence: Any) -> None:
        """
        Тест поиска вакансий по ключевому слову
        """
        input_sequence = mock_input_sequence(["3", "python", "4"])

        with (
            patch("builtins.input", side_effect=input_sequence),
            patch("src.user_interaction.HeadHunterAPI"),
            patch(
                "src.user_interaction.JSONStorage.get_vacancies",
                side_effect=[
                    [],  # Пустой результат по заголовку
                    [
                        {
                            "title": "Python Developer",
                            "description": "Python backend",
                            "url": "https://example.com/1",
                            "employer": "Test Company",
                            "salary": 100000,
                        }
                    ],  # Результат по описанию
                ],
            ) as mock_get_vacancies,
            patch("src.user_interaction.display_vacancies") as mock_display,
        ):
            main_menu()

            # Проверяем вызов get_vacancies
            assert mock_get_vacancies.call_count == 2  # Два вызова - по заголовку и описанию

            # Проверяем вызов display_vacancies
            mock_display.assert_called_once()

    def test_main_menu_error_handling(self, mock_input_sequence: Any) -> None:
        """
        Тест обработки ошибок ввода
        """
        input_sequence = mock_input_sequence(["2", "abc", "4"])

        with (
            patch("builtins.input", side_effect=input_sequence),
            patch("src.user_interaction.HeadHunterAPI"),
            patch("src.user_interaction.JSONStorage"),
            patch("builtins.print") as mock_print,
        ):
            main_menu()

            # Проверяем вывод сообщения об ошибке ввода
            mock_print.assert_any_call("Ошибка ввода: invalid literal for int() with base 10: 'abc'")

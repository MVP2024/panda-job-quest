from typing import List, Dict, Any


def format_salary(salary: float) -> str:
	"""
	Форматирование зарплаты для красивого отображения

	:param salary: Значение зарплаты
	:return: Отформатированная строка зарплаты
	"""
	if salary is None:
		return "Зарплата не указана"

	# Используем locale для форматирования с пробелами и запятой
	return f"{salary:,.2f} руб.".replace('.', ',').replace(',', ' ')


def filter_vacancies_by_keyword(vacancies: List[Dict[str, Any]], keyword: str) -> List[Dict[str, Any]]:
	"""
	Фильтрация вакансий по ключевому слову

	:param vacancies: Список вакансий
	:param keyword: Ключевое слово для поиска
	:return: Отфильтрованный список вакансий
	"""
	# Если ключевое слово пустое, возвращаем пустой список
	if not keyword or not keyword.strip():
		return []

	return [
		vacancy for vacancy in vacancies
		if keyword.lower() in vacancy.get('description', '').lower() or
		   keyword.lower() in vacancy.get('title', '').lower()
	]


def sort_vacancies_by_salary(vacancies: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
	"""
	Сортировка вакансий по зарплате

	:param vacancies: Список вакансий
	:param reverse: Направление сортировки (по убыванию или возрастанию)
	:return: Отсортированный список вакансий
	"""
	return sorted(vacancies, key=lambda x: x.get('salary', 0) or 0, reverse=reverse)

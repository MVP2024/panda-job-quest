import pytest
from models.vacancy import Vacancy


# тесты для _slots
def test_vacancy_slots():
	"""Проверка, что класс использует __slots__"""
	vacancy = Vacancy(title="Test", url="http://test.com")

	# Проверка, что можно установить только определенные атрибуты
	assert hasattr(vacancy, '_title'), "Слот '_title' должен существовать"
	assert hasattr(vacancy, '_url'), "Слот '_url' должен существовать"
	assert hasattr(vacancy, '_salary'), "Слот '_salary' должен существовать"
	assert hasattr(vacancy, '_description'), "Слот '_description' должен существовать"


def test_vacancy_slots_prevent_new_attributes():
	"""Проверка, что нельзя добавить новые атрибуты"""
	vacancy = Vacancy(title="Test", url="http://test.com")

	with pytest.raises(AttributeError, match="'Vacancy' object has no attribute"):
		vacancy.new_attribute = "Попытка добавить новый атрибут"


def test_vacancy_default_fields():
	"""Проверка значений по умолчанию"""
	vacancy = Vacancy()

	assert vacancy.title == '', "Заголовок должен быть пустой строкой по умолчанию"
	assert vacancy.url == '', "URL должен быть пустой строкой по умолчанию"
	assert vacancy.salary == {}, "Зарплата должна быть пустым словарем по умолчанию"
	assert vacancy.description == "Описание отсутствует", "Описание должно быть по умолчанию"


def test_vacancy_custom_initialization():
	"""Проверка инициализации с пользовательскими значениями"""
	vacancy = Vacancy(
		title="Python Developer",
		url="https://example.com/job",
		salary=50000,
		description="Крутая работа"
	)

	assert vacancy.title == "Python Developer"
	assert vacancy.url == "https://example.com/job"
	assert vacancy.salary == 50000.0
	assert vacancy.description == "Крутая работа"
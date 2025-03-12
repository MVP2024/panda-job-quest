import pytest
from models.vacancy import Vacancy

def test_vacancy_init_default():
    """Тест инициализации вакансии с пустыми обязательными параметрами"""
    with pytest.raises(ValueError, match="Название вакансии не может быть пустым"):
        Vacancy(title='', url='')

def test_vacancy_init_with_minimal_values():
    """Тест инициализации вакансии с минимальными обязательными значениями"""
    vacancy = Vacancy(
        title='Python Developer',
        url='https://example.com'
    )
    assert vacancy.title == 'Python Developer'
    assert vacancy.url == 'https://example.com'
    assert vacancy.salary == 0.0
    assert vacancy.description == 'Описание отсутствует'

def test_vacancy_init_with_full_values():
    """Тест инициализации вакансии с полными значениями"""
    vacancy = Vacancy(
        title='Python Developer',
        url='https://example.com',
        salary=50000.0,
        description='Требуется опытный разработчик'
    )
    assert vacancy.title == 'Python Developer'
    assert vacancy.url == 'https://example.com'
    assert vacancy.salary == 50000.0
    assert vacancy.description == 'Требуется опытный разработчик'

def test_vacancy_init_salary_dict():
    """Тест инициализации с зарплатой в виде словаря"""
    salary_dict = {'from': 50000, 'to': 100000}
    vacancy = Vacancy(
        title='Python Developer',
        url='https://example.com',
        salary=salary_dict
    )
    assert vacancy.salary == 75000.0

def test_vacancy_init_empty_title_raises_error():
    """Тест, что пустое название вакансии вызывает ошибку"""
    with pytest.raises(ValueError, match="Название вакансии не может быть пустым"):
        Vacancy(title='', url='https://example.com')

def test_vacancy_init_empty_url_raises_error():
    """Тест, что пустой URL вызывает ошибку"""
    with pytest.raises(ValueError, match="URL вакансии не может быть пустым"):
        Vacancy(title='Python Developer', url='')

def test_vacancy_init_none_salary():
    """Тест инициализации с None в качестве зарплаты"""
    vacancy = Vacancy(
        title='Python Developer',
        url='https://example.com',
        salary=None
    )
    assert vacancy.salary == 0.0

def test_vacancy_init_description_default():
    """Тест, что при пустом описании устанавливается значение по умолчанию"""
    vacancy = Vacancy(
        title='Python Developer',
        url='https://example.com',
        description=''
    )
    assert vacancy.description == 'Описание отсутствует'

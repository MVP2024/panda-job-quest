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


@pytest.mark.parametrize("invalid_title", ['', None])
def test_vacancy_invalid_title(base_vacancy_data, invalid_title):
    """Тест на невалидное название вакансии"""
    base_vacancy_data['title'] = invalid_title
    with pytest.raises(ValueError, match="Название вакансии не может быть пустым"):
        Vacancy(**base_vacancy_data)


@pytest.mark.parametrize("invalid_url", ['', None])
def test_vacancy_invalid_url(base_vacancy_data, invalid_url):
    """Тест на невалидный URL"""
    base_vacancy_data['url'] = invalid_url
    with pytest.raises(ValueError, match="URL вакансии не может быть пустым"):
        Vacancy(**base_vacancy_data)


@pytest.mark.parametrize("salary_input, expected", [
    (None, 0.0),
    (50000, 50000.0),
    ({'from': 50000, 'to': 100000}, 75000.0)
])
def test_vacancy_salary_handling(base_vacancy_data, salary_input, expected):
    """Тест обработки различных вариантов зарплаты"""
    base_vacancy_data['salary'] = salary_input
    vacancy = Vacancy(**base_vacancy_data)
    assert vacancy.salary == expected


def test_vacancy_description_default(base_vacancy_data):
    """Тест установки описания по умолчанию"""
    base_vacancy_data['description'] = ''
    vacancy = Vacancy(**base_vacancy_data)
    assert vacancy.description == 'Описание отсутствует'


def test_vacancy_to_dict(vacancy_with_full_data):
    """Тест преобразования вакансии в словарь"""
    vacancy_dict = vacancy_with_full_data.to_dict()
    assert isinstance(vacancy_dict, dict)
    assert all(key in vacancy_dict for key in ['title', 'url', 'salary', 'description'])


def test_vacancy_comparison(base_vacancy_data):
    """Тест сравнения вакансий по зарплате"""
    base_vacancy_data['salary'] = 50000
    vacancy1 = Vacancy(**base_vacancy_data)

    base_vacancy_data['salary'] = 60000
    vacancy2 = Vacancy(**base_vacancy_data)

    assert vacancy1 < vacancy2
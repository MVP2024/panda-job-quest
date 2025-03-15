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
    assert vacancy.employer == 'Работодатель не указан'


def test_vacancy_init_with_full_values():
    """Тест инициализации вакансии с полными значениями"""
    vacancy = Vacancy(
        title='Python Developer',
        url='https://example.com',
        salary=50000.0,
        description='Требуется опытный разработчик',
        employer='Google'
    )
    assert vacancy.title == 'Python Developer'
    assert vacancy.url == 'https://example.com'
    assert vacancy.salary == 50000.0
    assert vacancy.description == 'Требуется опытный разработчик'
    assert vacancy.employer == 'Google'


@pytest.mark.parametrize("salary_input, expected", [
    (None, 0.0),
    (50000, 50000.0),
    ({'from': 50000, 'to': 100000}, 75000.0),
    ({'from': 0, 'to': 0}, 0.0)
])
def test_vacancy_salary_handling(base_vacancy_data, salary_input, expected):
    """Тест обработки различных вариантов зарплаты"""
    base_vacancy_data['salary'] = salary_input
    vacancy = Vacancy(**base_vacancy_data)
    assert vacancy.salary == expected


@pytest.mark.parametrize("employer_input, expected", [
    (None, 'Работодатель не указан'),
    ('', 'Работодатель не указан'),
    ('Yandex', 'Yandex'),
    (' ', 'Работодатель не указан')
])
def test_vacancy_employer_handling(base_vacancy_data, employer_input, expected):
    """Тест обработки различных вариантов работодателя"""
    base_vacancy_data['employer'] = employer_input
    vacancy = Vacancy(**base_vacancy_data)
    assert vacancy.employer == expected


@pytest.mark.parametrize("invalid_title", ['', None, '   '])
def test_vacancy_invalid_title(base_vacancy_data, invalid_title):
    """Тест на невалидное название вакансии"""
    base_vacancy_data['title'] = invalid_title
    with pytest.raises(ValueError, match="Название вакансии не может быть пустым"):
        Vacancy(**base_vacancy_data)


@pytest.mark.parametrize("invalid_url", ['', None, '   '])
def test_vacancy_invalid_url(base_vacancy_data, invalid_url):
    """Тест на невалидный URL"""
    base_vacancy_data['url'] = invalid_url
    with pytest.raises(ValueError, match="URL вакансии не может быть пустым"):
        Vacancy(**base_vacancy_data)


@pytest.mark.parametrize("description_input, expected", [
    ('', 'Описание отсутствует'),
    (None, 'Описание отсутствует'),
    ('   ', 'Описание отсутствует'),
    ('Тестовое описание', 'Тестовое описание')
])
def test_vacancy_description_handling(base_vacancy_data, description_input, expected):
    """Тест обработки различных вариантов описания"""
    base_vacancy_data['description'] = description_input
    vacancy = Vacancy(**base_vacancy_data)
    assert vacancy.description == expected


def test_vacancy_to_dict(base_vacancy_data):
    """Тест преобразования вакансии в словарь"""
    base_vacancy_data.update({
        'salary': 50000.0,
        'description': 'Тестовое описание',
        'employer': 'Google'
    })
    vacancy = Vacancy(**base_vacancy_data)
    vacancy_dict = vacancy.to_dict()

    assert isinstance(vacancy_dict, dict)
    assert all(key in vacancy_dict for key in ['title', 'url', 'salary', 'description', 'employer'])
    assert vacancy_dict['title'] == base_vacancy_data['title']
    assert vacancy_dict['url'] == base_vacancy_data['url']
    assert vacancy_dict['salary'] == 50000.0
    assert vacancy_dict['description'] == 'Тестовое описание'
    assert vacancy_dict['employer'] == 'Google'


def test_vacancy_comparison(base_vacancy_data):
    """Тест сравнения вакансий по зарплате"""
    base_vacancy_data['salary'] = 50000
    vacancy1 = Vacancy(**base_vacancy_data)

    base_vacancy_data['salary'] = 60000
    vacancy2 = Vacancy(**base_vacancy_data)

    assert vacancy1 < vacancy2
    assert not (vacancy2 < vacancy1)


def test_vacancy_repr(base_vacancy_data):
    """Тест строкового представления вакансии"""
    base_vacancy_data['salary'] = 50000
    vacancy = Vacancy(**base_vacancy_data)
    repr_str = repr(vacancy)

    assert 'Vacancy' in repr_str
    assert base_vacancy_data['title'] in repr_str
    assert '50000' in repr_str


def test_vacancy_format_salary(base_vacancy_data):
    """Тест форматирования зарплаты"""
    base_vacancy_data['salary'] = 50000
    vacancy = Vacancy(**base_vacancy_data)

    formatted_salary = vacancy.format_salary()
    assert '50 000.00 руб.' in formatted_salary


def test_vacancy_format_salary_zero(base_vacancy_data):
    """Тест форматирования нулевой зарплаты"""
    base_vacancy_data['salary'] = 0
    vacancy = Vacancy(**base_vacancy_data)

    formatted_salary = vacancy.format_salary()
    assert 'Зарплата не указана' in formatted_salary

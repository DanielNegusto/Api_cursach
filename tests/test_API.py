from unittest.mock import patch
from src.API import HeadHunterAPI


# Тестирование метода get_vacancies
@patch('requests.Session.get')
def test_get_vacancies(mock_get):
    api = HeadHunterAPI()

    # Настраиваем mock для возврата желаемого значения
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        'items': [{'name': 'Python Developer'}]
    }

    result = api.get_vacancies("Python")

    assert result == {'items': [{'name': 'Python Developer'}]}
    mock_get.assert_called_once_with('https://api.hh.ru/vacancies',
                                     params={'text': 'Python', 'per_page': 100, 'page': 0})


# Тестирование метода get_company_vacancies
@patch('requests.Session.get')
def test_get_company_vacancies(mock_get):
    api = HeadHunterAPI()

    # Настраиваем mock для возврата желаемого значения
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        'items': [{'name': 'Vacancy 1'}]
    }

    result = api.get_company_vacancies("123")

    assert result == {'items': [{'name': 'Vacancy 1'}]}
    mock_get.assert_called_once_with('https://api.hh.ru/vacancies',
                                     params={'employer_id': '123', 'per_page': 100, 'page': 0})


# Тестирование метода get_employer
@patch('requests.get')
def test_get_employer(mock_get):
    api = HeadHunterAPI()

    # Настраиваем mock для возврата желаемого значения
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        'name': 'Company XYZ'
    }

    result = api.get_employer("456")

    assert result == {'name': 'Company XYZ'}
    mock_get.assert_called_once_with('https://api.hh.ru/employers/456')

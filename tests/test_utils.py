from src.classes import Vacancy
from src.utils import filter_vacancies, get_top_vacancies, get_vacancies_by_salary, print_vacancies, sort_vacancies


def test_filter_vacancies():
    vacancies = [
        Vacancy(title="Software Engineer", link="https://example.com", area="Moscow", employer="Company"),
        Vacancy(
            title="Data Scientist", link="https://example2.com", area="Saint Petersburg", employer="Another Company"
        ),
        Vacancy(title="Product Manager", link="https://example3.com", area="Moscow", employer="Tech Corp"),
    ]
    keywords = ["Engineer", "Tech"]

    filtered = filter_vacancies(vacancies, keywords)

    assert len(filtered) == 2
    assert filtered[0].title == "Software Engineer"
    assert filtered[1].title == "Product Manager"


def test_get_vacancies_by_salary(vacancies, capsys):
    salary_range = "1000-2000"

    filtered = get_vacancies_by_salary(vacancies, salary_range)

    assert len(filtered) == 2
    assert filtered[0].title == "Software Engineer"
    assert filtered[1].title == "Data Scientist"

    # Test invalid salary range
    salary_range_invalid = "2000"
    filtered_invalid = get_vacancies_by_salary(vacancies, salary_range_invalid)
    captured = capsys.readouterr()
    assert "Неправильный формат диапазона зарплаты" in captured.out
    assert len(filtered_invalid) == 0


def test_sort_vacancies(vacancies):

    sorted_vacancies = sort_vacancies(vacancies)

    assert sorted_vacancies[0].title == "Data Scientist"
    assert sorted_vacancies[1].title == "Software Engineer"
    assert sorted_vacancies[2].title == "Product Manager"


def test_get_top_vacancies(vacancies):

    top_vacancies = get_top_vacancies(vacancies, 2)

    assert len(top_vacancies) == 2
    assert top_vacancies[0].title == "Software Engineer"
    assert top_vacancies[1].title == "Data Scientist"


def test_print_vacancies(capsys):
    vacancies = [
        Vacancy(
            title="Software Engineer",
            link="https://example.com",
            salary_from="1000",
            salary_to="2000",
            currency="USD",
            area="Moscow",
            employer="Company",
        )
    ]

    print_vacancies(vacancies)
    captured = capsys.readouterr()

    assert "Вакансия: Software Engineer" in captured.out
    assert "Зарплата: 1000 - 2000 USD" in captured.out
    assert "Регион: Moscow" in captured.out
    assert "Работодатель: Company" in captured.out

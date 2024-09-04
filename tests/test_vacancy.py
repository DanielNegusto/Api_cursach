from src.vacancy import Vacancy, filter_vacancies, get_vacancies_by_salary, sort_vacancies, get_top_vacancies


def test_vacancy_initialization():
    vacancy = Vacancy(
        title="Developer",
        link="https://example.com",
        salary_from="1000",
        salary_to="2000",
        currency="USD",
        area="New York",
        employer="Tech Corp"
    )
    assert vacancy.title == "Developer"
    assert vacancy.link == "https://example.com"
    assert vacancy.salary_from == "1000"
    assert vacancy.salary_to == "2000"
    assert vacancy.currency == "USD"
    assert vacancy.area == "New York"
    assert vacancy.employer == "Tech Corp"


def test_vacancy_invalid_link():
    vacancy = Vacancy(title="Developer", link="example.com")
    assert vacancy.link is None


def test_vacancy_invalid_salary():
    vacancy = Vacancy(title="Developer", link="https://example.com", salary_from="abc")
    assert vacancy.salary_from is None


def test_cast_to_object_list(vacancies):
    json_data = {
        "items": [
            {
                "name": "Developer",
                "alternate_url": "https://example.com",
                "salary": {"from": "1000", "to": "2000", "currency": "USD"},
                "area": {"name": "New York"},
                "employer": {"name": "Tech Corp"}
            }
        ]
    }
    vacancies = Vacancy.cast_to_object_list(json_data)
    assert len(vacancies) == 1
    assert vacancies[0].title == "Developer"


def test_filter_vacancies():
    vacancies = [
        Vacancy(title="Developer", link="https://example.com", area="New York", employer="Tech Corp"),
        Vacancy(title="Designer", link="https://example.com", area="Los Angeles", employer="Design Studio"),
    ]
    filtered = filter_vacancies(vacancies, ["developer"])
    assert len(filtered) == 1
    assert filtered[0].title == "Developer"


def test_get_vacancies_by_salary():
    vacancies = [
        Vacancy(title="Developer", link="https://example.com", salary_from="1000", salary_to="2000"),
        Vacancy(title="Designer", link="https://example.com", salary_from="3000", salary_to="4000"),
    ]
    filtered = get_vacancies_by_salary(vacancies, "1500-3500")
    assert len(filtered) == 2


def test_sort_vacancies():
    vacancies = [
        Vacancy(title="Developer", link="https://example.com", salary_from="1000", salary_to="2000"),
        Vacancy(title="Designer", link="https://example.com", salary_from="3000", salary_to="4000"),
    ]
    sorted_vacancies = sort_vacancies(vacancies)
    assert sorted_vacancies[0].title == "Designer"


def test_get_top_vacancies():
    vacancies = [
        Vacancy(title="Developer", link="https://example.com"),
        Vacancy(title="Designer", link="https://example.com"),
    ]
    top_vacancies = get_top_vacancies(vacancies, 1)
    assert len(top_vacancies) == 1
    assert top_vacancies[0].title == "Developer"

import pytest

from src.vacancy import Vacancy


@pytest.fixture
def vacancies():
    return [
        Vacancy(
            title="Software Engineer", link="http://example.com", salary_from="1000", salary_to="2000", currency="USD"
        ),
        Vacancy(
            title="Data Scientist", link="http://example2.com", salary_from="1500", salary_to="2500", currency="USD"
        ),
        Vacancy(title="Product Manager", link="http://example3.com", salary_from=None, salary_to=None, currency="USD"),
    ]

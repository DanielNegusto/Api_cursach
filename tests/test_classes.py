from unittest.mock import MagicMock, patch

from src.classes import HeadHunterAPI, JSONSaver, Vacancy


# Тесты для Vacancy
def test_vacancy_initialization():
    vacancy = Vacancy(
        title="Software Engineer",
        link="https://example.com",
        salary_from="1000",
        salary_to="2000",
        currency="USD",
        area="Moscow",
        employer="Company",
    )
    assert vacancy.title == "Software Engineer"
    assert vacancy.link == "https://example.com"
    assert vacancy.salary_from == "1000"
    assert vacancy.salary_to == "2000"
    assert vacancy.currency == "USD"
    assert vacancy.area == "Moscow"
    assert vacancy.employer == "Company"


def test_vacancy_validation():
    vacancy = Vacancy(title="Software Engineer", link="invalid_link", salary_from="invalid_salary")
    assert vacancy.link is None
    assert vacancy.salary_from is None


# Тесты для HeadHunterAPI
@patch("src.classes.requests.Session.get")
def test_get_vacancies(mock_get, vacancies):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"items": []}
    mock_get.return_value = mock_response

    api = HeadHunterAPI()
    vacancies = api.get_vacancies("python")
    assert vacancies == {"items": []}
    mock_get.assert_called_with(api.BASE_URL, params={"text": "python", "per_page": 100, "page": 0})


# Тесты для JSONSaver
def test_json_saver_add_vacancy(tmpdir):
    file_path = tmpdir.join("vacancies.json")
    saver = JSONSaver(file_name=str(file_path))

    vacancy = Vacancy(title="Software Engineer", link="https://example.com")

    saver.add_vacancy(vacancy)
    data = saver.get_vacancies()

    assert len(data) == 1
    assert data[0]["title"] == "Software Engineer"
    assert data[0]["link"] == "https://example.com"


def test_json_saver_delete_vacancy(tmpdir):
    file_path = tmpdir.join("vacancies.json")
    saver = JSONSaver(file_name=str(file_path))

    vacancy = Vacancy(title="Software Engineer", link="https://example.com")

    saver.add_vacancy(vacancy)
    saver.delete_vacancy(vacancy)
    data = saver.get_vacancies()

    assert len(data) == 0


def test_cast_to_object_list(vacancies):
    json_data = {
        "items": [
            {
                "name": "Software Engineer",
                "alternate_url": "https://example.com",
                "salary": {"from": 1000, "to": 2000, "currency": "USD"},
                "area": {"name": "Moscow"},
                "employer": {"name": "Company"},
            },
            {
                "name": "Data Scientist",
                "alternate_url": "https://example2.com",
                "salary": None,
                "area": {"name": "Saint Petersburg"},
                "employer": {"name": "Another Company"},
            },
        ]
    }

    vacancies = Vacancy.cast_to_object_list(json_data)

    assert len(vacancies) == 2

    vacancy1 = vacancies[0]
    assert vacancy1.title == "Software Engineer"
    assert vacancy1.link == "https://example.com"
    assert vacancy1.salary_from == "1000"
    assert vacancy1.salary_to == "2000"
    assert vacancy1.currency == "USD"
    assert vacancy1.area == "Moscow"
    assert vacancy1.employer == "Company"

    vacancy2 = vacancies[1]
    assert vacancy2.title == "Data Scientist"
    assert vacancy2.link == "https://example2.com"
    assert vacancy2.salary_from is None
    assert vacancy2.salary_to is None
    assert vacancy2.currency == ""
    assert vacancy2.area == "Saint Petersburg"
    assert vacancy2.employer == "Another Company"


def test_update_vacancy(tmpdir):
    file_path = tmpdir.join("vacancies.json")
    saver = JSONSaver(file_name=str(file_path))

    old_vacancy = Vacancy(title="Software Engineer", link="https://example.com")
    new_vacancy = Vacancy(title="Senior Software Engineer", link="https://example.com")

    saver.add_vacancy(old_vacancy)
    saver.update_vacancy(old_vacancy, new_vacancy)
    data = saver.get_vacancies()

    assert len(data) == 1
    assert data[0]["title"] == "Senior Software Engineer"


def test_update_vacancy_not_found(tmpdir, capsys):
    file_path = tmpdir.join("vacancies.json")
    saver = JSONSaver(file_name=str(file_path))

    old_vacancy = Vacancy(title="Software Engineer", link="https://example.com")
    new_vacancy = Vacancy(title="Senior Software Engineer", link="https://example.com")

    saver.update_vacancy(old_vacancy, new_vacancy)
    captured = capsys.readouterr()
    assert "Вакансия не найдена" in captured.out


def test_update_vacancy_file(tmpdir):
    file_path = tmpdir.join("vacancies.json")
    saver = JSONSaver(file_name=str(file_path))

    vacancies = [
        Vacancy(title="Software Engineer", link="https://example.com"),
        Vacancy(title="Data Scientist", link="https://example2.com"),
    ]

    saver.update_vacancy_file(vacancies)
    data = saver.get_vacancies()

    assert len(data) == 2
    assert data[0]["title"] == "Software Engineer"
    assert data[1]["title"] == "Data Scientist"

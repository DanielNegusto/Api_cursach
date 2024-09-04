from unittest.mock import patch, Mock
from src.API import HeadHunterAPI


def test_connect_success():
    api = HeadHunterAPI()
    with patch('requests.Session.get') as mocked_get:
        mocked_response = Mock()
        mocked_response.status_code = 200
        mocked_get.return_value = mocked_response

        response = api._connect()
        assert response.status_code == 200
        mocked_get.assert_called_once_with(api.BASE_URL)


def test_get_vacancies():
    api = HeadHunterAPI()
    mock_data = {"items": [{"name": "Developer"}]}

    with patch('requests.Session.get') as mocked_get:
        mocked_response = Mock()
        mocked_response.status_code = 200
        mocked_response.json.return_value = mock_data
        mocked_get.return_value = mocked_response

        data = api.get_vacancies("Developer")
        assert data == mock_data
        mocked_get.assert_called_with(api.BASE_URL, params={"text": "Developer", "per_page": 100, "page": 0})

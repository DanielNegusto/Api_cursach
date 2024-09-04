import json
from unittest.mock import patch, mock_open, ANY

import pytest

from src.file_handler import JSONSaver
from src.vacancy import Vacancy


@pytest.fixture
def vacancy():
    return Vacancy("Developer", "OpenAI")


@pytest.fixture
def json_saver():
    return JSONSaver("test_vacancies.json")


def test_add_vacancy(json_saver, vacancy):
    with patch("builtins.open", mock_open(read_data="[]")), patch("os.path.exists", return_value=True):
        with patch("json.dump") as mock_json_dump:
            json_saver.add_vacancy(vacancy)
            mock_json_dump.assert_called_once_with([vacancy.to_dict()], ANY, ensure_ascii=False, indent=4)


def test_delete_vacancy(json_saver, vacancy):
    with patch("builtins.open", mock_open(read_data=json.dumps([vacancy.to_dict()]))), patch("os.path.exists", return_value=True):
        with patch("json.dump") as mock_json_dump:
            json_saver.delete_vacancy(vacancy)
            mock_json_dump.assert_called_once_with([], ANY, ensure_ascii=False, indent=4)

def test_get_vacancies(json_saver, vacancy, vacancies):
    with patch("builtins.open", mock_open(read_data=json.dumps([vacancy.to_dict()]))), patch("os.path.exists", return_value=True):
        vacancies = json_saver.get_vacancies()
        assert vacancies == [vacancy.to_dict()]

def test_update_vacancy(json_saver, vacancy):
    new_vacancy = Vacancy("Senior Developer", "OpenAI")
    with patch("builtins.open", mock_open(read_data=json.dumps([vacancy.to_dict()]))), patch("os.path.exists", return_value=True):
        with patch("json.dump") as mock_json_dump:
            json_saver.update_vacancy(vacancy, new_vacancy)
            mock_json_dump.assert_called_once_with([new_vacancy.to_dict()], ANY, ensure_ascii=False, indent=4)

def test_update_vacancy_file(json_saver, vacancy):
    new_vacancy = Vacancy("Senior Developer", "OpenAI")
    with patch("builtins.open", mock_open(read_data=json.dumps([]))), patch("os.path.exists", return_value=True):
        with patch("json.dump") as mock_json_dump:
            json_saver.update_vacancy_file([vacancy, new_vacancy])
            mock_json_dump.assert_called_once_with([vacancy.to_dict(), new_vacancy.to_dict()], ANY, ensure_ascii=False, indent=4)
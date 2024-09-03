import json
import os
from abc import ABC, abstractmethod

import requests


class AbstractFileHandler(ABC):
    @abstractmethod
    def add_vacancy(self, data):
        pass

    @abstractmethod
    def delete_vacancy(self, data):
        pass


class VacancyAPI(ABC):
    @abstractmethod
    def _connect(self):
        """Приватный метод для подключения к API"""
        pass

    @abstractmethod
    def get_vacancies(self, keyword):
        """Метод для получения вакансий"""
        pass


class HeadHunterAPI(VacancyAPI):
    BASE_URL = "https://api.hh.ru/vacancies"

    def __init__(self):
        self.__session = requests.Session()

    def _connect(self):
        response = self.__session.get(self.BASE_URL)
        if response.status_code != 200:
            response.raise_for_status()
        return response

    def get_vacancies(self, keyword):
        self._connect()

        params = {"text": keyword, "per_page": 100, "page": 0}
        response = self.__session.get(self.BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        return data


class Vacancy:
    __slots__ = ("title", "link", "salary_from", "salary_to", "currency", "area", "employer")

    def __init__(
        self,
        title: str,
        link: str,
        salary_from: str = None,
        salary_to: str = None,
        currency: str = "",
        area: str = "",
        employer: str = "",
    ):
        self.title = title
        self.link = self._validate_link(link)
        self.salary_from = self._validate_salary(salary_from)
        self.salary_to = self._validate_salary(salary_to)
        self.currency = currency
        self.area = area
        self.employer = employer

    @staticmethod
    def _validate_salary(salary):
        if salary is None:
            return None
        if not isinstance(salary, str):
            salary = str(salary)
        if salary.replace(" ", "").replace("-", "").isdigit():
            return salary
        else:
            return None

    @staticmethod
    def _validate_link(link):
        if link is None:
            return None
        if not isinstance(link, str):
            link = str(link)
        if link.startswith("http"):
            return link
        else:
            return None

    @classmethod
    def cast_to_object_list(cls, json_data):
        vacancies = []
        for item in json_data.get("items", []):
            title = item.get("name")
            link = item.get("alternate_url")
            salary = item.get("salary")
            salary_from = salary["from"] if salary else None
            salary_to = salary["to"] if salary else None
            currency = salary["currency"] if salary else ""
            area = item.get("area", {}).get("name")
            employer = item.get("employer", {}).get("name")

            vacancy = cls(title, link, salary_from, salary_to, currency)
            vacancy.area = area
            vacancy.employer = employer
            vacancies.append(vacancy)

        return vacancies

    def to_dict(self):
        return {
            "title": self.title,
            "link": self.link,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
            "currency": self.currency,
            "area": self.area,
            "employer": self.employer,
        }

    @staticmethod
    def _convert_salary(salary):
        return float(salary) if salary is not None else 0.0

    def __lt__(self, other):
        return self._convert_salary(self.salary_from) < self._convert_salary(other.salary_from)

    def __le__(self, other):
        return self._convert_salary(self.salary_from) <= self._convert_salary(other.salary_from)

    def __gt__(self, other):
        return self._convert_salary(self.salary_from) > self._convert_salary(other.salary_from)

    def __ge__(self, other):
        return self._convert_salary(self.salary_from) >= self._convert_salary(other.salary_from)

    def __eq__(self, other):
        return self._convert_salary(self.salary_from) == self._convert_salary(other.salary_from)


class JSONSaver(AbstractFileHandler):

    def __init__(self, file_name: str = "data/vacancies.json"):
        self.__file_name = file_name

    def _read_file(self):
        """Чтение данных из файла."""
        if not os.path.exists(self.__file_name):
            return []
        with open(self.__file_name, "r", encoding="utf-8") as file:
            return json.load(file)

    def _write_file(self, data):
        """Запись данных в файл."""
        with open(self.__file_name, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy):
        data = self._read_file()
        if vacancy.to_dict() not in data:
            data.append(vacancy.to_dict())
            self._write_file(data)

    def delete_vacancy(self, vacancy):
        data = self._read_file()
        if vacancy.to_dict() in data:
            data.remove(vacancy.to_dict())
            self._write_file(data)
        else:
            print("Вакансия не найдена")

    def get_vacancies(self):
        return self._read_file()

    def update_vacancy(self, old_vacancy, new_vacancy):
        data = self._read_file()
        if old_vacancy.to_dict() in data:
            data.remove(old_vacancy.to_dict())
            data.append(new_vacancy.to_dict())
            self._write_file(data)
        else:
            print("Вакансия не найдена")

    def update_vacancy_file(self, vacancies):
        self._write_file([vac.to_dict() for vac in vacancies])

class Vacancy:
    """
    Класс для представления вакансии.

    Атрибуты:
    ----------
    title : str
        Название вакансии.
    link : str
        Ссылка на вакансию.
    salary_from : str
        Нижняя граница зарплаты.
    salary_to : str
        Верхняя граница зарплаты.
    currency : str
        Валюта зарплаты.
    area : str
        Регион работы.
    employer : str
        Работодатель.
    """

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
        """
        Проверяет и форматирует значение зарплаты.

        Параметры:
        ----------
        salary : str
            Значение зарплаты.

        Возвращает:
        ----------
        str
            Форматированное значение зарплаты или None.
        """
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
        """
        Проверяет и форматирует ссылку на вакансию.

        Параметры:
        ----------
        link : str
            Ссылка на вакансию.

        Возвращает:
        ----------
        str
            Форматированная ссылка или None.
        """
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
        """
        Преобразует JSON данные в список объектов Vacancy.

        Параметры:
        ----------
        json_data : dict
            JSON данные с вакансиями.

        Возвращает:
        ----------
        list
            Список объектов Vacancy.
        """
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
        """
        Преобразует объект Vacancy в словарь.

        Возвращает:
        ----------
        dict
            Словарь с данными вакансии.
        """
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
        """
        Преобразует значение зарплаты в число.

        Параметры:
        ----------
        salary : str
            Значение зарплаты.

        Возвращает:
        ----------
        float
            Числовое значение зарплаты.
        """
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


def filter_vacancies(vacancies, keywords):
    """
    Фильтрует вакансии по ключевым словам.

    Параметры:
    ----------
    vacancies : list
        Список объектов Vacancy.
    keywords : list
        Список ключевых слов для фильтрации.

    Возвращает:
    ----------
    list
        Список вакансий, содержащих ключевые слова в названии, регионе или работодателе.
    """
    return [
        v for v in vacancies
        if any(keyword.lower() in (v.title + v.area + v.employer).lower() for keyword in keywords)
    ]


def get_vacancies_by_salary(vacancies, salary_range):
    """
    Фильтрует вакансии по диапазону зарплаты.

    Параметры:
    ----------
    vacancies : list
        Список объектов Vacancy.
    salary_range : str
        Строка с диапазоном зарплаты в формате 'min-max'.

    Возвращает:
    ----------
    list
        Список вакансий, попадающих в указанный диапазон зарплаты.
    """
    if "-" not in salary_range:
        print("Неправильный формат диапазона зарплаты. Пожалуйста, используйте формат 'min-max'.")
        return []

    min_salary, max_salary = map(int, salary_range.split("-"))

    def is_in_range(value, min_value, max_value):
        if value is None:
            return False
        try:
            value = int(value.replace(" ", ""))
        except ValueError:
            return False
        return min_value <= value <= max_value

    return [
        v for v in vacancies
        if (is_in_range(v.salary_from, min_salary, max_salary) or is_in_range(v.salary_to, min_salary, max_salary))
    ]


def sort_vacancies(vacancies):
    """
    Сортирует вакансии по зарплате в порядке убывания.

    Параметры:
    ----------
    vacancies : list
        Список объектов Vacancy.

    Возвращает:
    ----------
    list
        Отсортированный список вакансий.
    """

    def get_salary(v):
        salary_from = int(v.salary_from.replace(" ", "")) if v.salary_from is not None else 0
        salary_to = int(v.salary_to.replace(" ", "")) if v.salary_to is not None else 0
        return salary_from, salary_to

    return sorted(vacancies, key=get_salary, reverse=True)


def get_top_vacancies(vacancies, top_n):
    """
    Возвращает топ N вакансий.

    Параметры:
    ----------
    vacancies : list
        Список объектов Vacancy.
    top_n : int
        Количество вакансий для возврата.

    Возвращает:
    ----------
    list
        Список из top_n вакансий.
    """
    return vacancies[:top_n]


def print_vacancies(vacancies):
    """
    Выводит информацию о вакансиях на экран.

    Параметры:
    ----------
    vacancies : list
        Список объектов Vacancy.
    """
    for vacancy in vacancies:
        print(
            f"\nВакансия: {vacancy.title}\n"
            f"Зарплата: {vacancy.salary_from} - {vacancy.salary_to} {vacancy.currency}\n"
            f"Регион: {vacancy.area}\n"
            f"Работодатель: {vacancy.employer}\n"
        )

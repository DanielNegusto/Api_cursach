from abc import ABC, abstractmethod
import requests


class VacancyAPI(ABC):
    """
    Абстрактный класс для взаимодействия с API вакансий.
    """

    @abstractmethod
    def _connect(self):
        """
        Приватный метод для подключения к API.
        """
        pass

    @abstractmethod
    def get_vacancies(self, keyword):
        """
        Метод для получения вакансий по ключевому слову.
        """
        pass


class HeadHunterAPI(VacancyAPI):
    """
    Класс для взаимодействия с API HeadHunter для получения вакансий.

    Атрибуты:
    ----------
    BASE_URL : str
        Базовый URL для API запросов к HeadHunter.

    Методы:
    -------
    _connect():
        Устанавливает соединение с API и возвращает ответ.
    get_vacancies(keyword: str):
        Получает вакансии, соответствующие заданному ключевому слову.
    """

    BASE_URL = "https://api.hh.ru/vacancies"

    def __init__(self):
        """
        Инициализирует объект HeadHunterAPI и создает сессию для HTTP-запросов.
        """
        self.__session = requests.Session()

    def _connect(self):
        """
        Устанавливает соединение с API HeadHunter.

        Возвращает:
        ----------
        response : requests.Response
            Ответ от сервера HeadHunter.

        Исключения:
        -----------
        HTTPError
            Если ответ от сервера имеет статус код, отличный от 200.
        """
        response = self.__session.get(self.BASE_URL)
        if response.status_code != 200:
            response.raise_for_status()
        return response

    def get_vacancies(self, keyword):
        """
        Получает список вакансий, соответствующих заданному ключевому слову.

        Параметры:
        ----------
        keyword : str
            Ключевое слово для поиска вакансий.

        Возвращает:
        ----------
        data : dict
            Данные с информацией о вакансиях.

        Исключения:
        -----------
        HTTPError
            Если запрос не был успешным.
        """
        self._connect()

        params = {"text": keyword, "per_page": 100, "page": 0}
        response = self.__session.get(self.BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        return data

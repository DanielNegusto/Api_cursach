from abc import ABC, abstractmethod
import requests


class VacancyAPI(ABC):
    """
    Абстрактный класс для взаимодействия с API вакансий.
    """

    @abstractmethod
    def _connect(self, url: str, params: dict = None):
        """
        Приватный метод для подключения к API.
        """
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str):
        """
        Метод для получения вакансий по ключевому слову.
        """
        pass

    @abstractmethod
    def get_company_vacancies(self, company_id: str):
        """
        Метод для получения вакансий компании по её ID.
        """
        pass

    @abstractmethod
    def get_employer(self, company_id: str):

        pass


class HeadHunterAPI(VacancyAPI):
    """
    Класс для взаимодействия с API HeadHunter для получения вакансий.
    """

    BASE_URL = "https://api.hh.ru"

    def __init__(self):
        """
        Инициализирует объект HeadHunterAPI и создает сессию для HTTP-запросов.
        """
        self.__session = requests.Session()

    def _connect(self, endpoint: str, params: dict = None):
        """
        Устанавливает соединение с API HeadHunter.

        Параметры:
        ----------
        endpoint : str
            Конкретный эндпоинт API.
        params : dict
            Параметры запроса.

        Возвращает:
        ----------
        response : requests.Response
            Ответ от сервера HeadHunter.

        Исключения:
        -----------
        HTTPError
            Если ответ от сервера имеет статус код, отличный от 200.
        """
        url = self.BASE_URL + endpoint
        try:
            response = self.__session.get(url, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}")
            return None
        return response

    def get_vacancies(self, keyword: str, city: str = None, experience: str = None):
        """
        Получает список вакансий, соответствующих заданному ключевому слову.

        Параметры:
        ----------
        keyword : str
            Ключевое слово для поиска вакансий.
        city : str, optional
            Город для фильтрации вакансий.
        experience : str, optional
            Уровень опыта для фильтрации вакансий.

        Возвращает:
        ----------
        data : dict
            Данные с информацией о вакансиях.
        """
        params = {"text": keyword, "per_page": 100, "page": 0}

        if city:
            params["area"] = city
        if experience:
            params["experience"] = experience

        response = self._connect("/vacancies", params)
        if response:
            return response.json()
        else:
            return {}

    def get_company_vacancies(self, company_id: str):
        """
        Получает вакансии конкретной компании по её ID.

        Параметры:
        ----------
        company_id : str
            ID компании для поиска вакансий.

        Возвращает:
        ----------
        data : dict
            Данные с информацией о вакансиях компании.
        """
        params = {"employer_id": company_id, "per_page": 100, "page": 0}
        response = self._connect("/vacancies", params=params)
        if response:
            return response.json()
        else:
            return {}

    def get_employer(self, employer_id):
        url = f"https://api.hh.ru/employers/{employer_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

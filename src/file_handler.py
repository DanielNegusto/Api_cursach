import json
import os
from abc import ABC, abstractmethod


class AbstractFileHandler(ABC):
    """
    Абстрактный класс для обработки файлов с вакансиями.
    """

    @abstractmethod
    def add_vacancy(self, data):
        """
        Добавляет вакансию в файл.
        """
        pass

    @abstractmethod
    def delete_vacancy(self, data):
        """
        Удаляет вакансию из файла.
        """
        pass


class JSONSaver(AbstractFileHandler):
    """
    Класс для сохранения и управления вакансиями в JSON файле.

    Атрибуты:
    ----------
    file_name : str
        Имя файла для сохранения данных.

    Методы:
    -------
    add_vacancy(vacancy: Vacancy):
        Добавляет вакансию в JSON файл.
    delete_vacancy(vacancy: Vacancy):
        Удаляет вакансию из JSON файла.
    get_vacancies():
        Получает все вакансии из JSON файла.
    update_vacancy(old_vacancy: Vacancy, new_vacancy: Vacancy):
        Обновляет вакансию в JSON файле.
    update_vacancy_file(vacancies: list):
        Обновляет файл с вакансиями.
    """

    def __init__(self, file_name: str = "data/vacancies.json"):
        """
        Инициализирует объект JSONSaver с заданным именем файла.
        """
        self.__file_name = file_name

    def _read_file(self):
        """
        Чтение данных из файла.

        Возвращает:
        ----------
        list
            Список данных из файла.
        """
        if not os.path.exists(self.__file_name):
            return []
        with open(self.__file_name, "r", encoding="utf-8") as file:
            return json.load(file)

    def _write_file(self, data):
        """
        Запись данных в файл.

        Параметры:
        ----------
        data : list
            Список данных для записи в файл.
        """
        with open(self.__file_name, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy):
        """
        Добавляет вакансию в файл, если её там нет.

        Параметры:
        ----------
        vacancy : Vacancy
            Объект вакансии для добавления.
        """
        data = self._read_file()
        if vacancy.to_dict() not in data:
            data.append(vacancy.to_dict())
            self._write_file(data)

    def delete_vacancy(self, vacancy):
        """
        Удаляет вакансию из файла, если она там есть.

        Параметры:
        ----------
        vacancy : Vacancy
            Объект вакансии для удаления.
        """
        data = self._read_file()
        if vacancy.to_dict() in data:
            data.remove(vacancy.to_dict())
            self._write_file(data)
        else:
            print("Вакансия не найдена")

    def get_vacancies(self):
        """
        Возвращает все вакансии из файла.

        Возвращает:
        ----------
        list
            Список вакансий.
        """
        return self._read_file()

    def update_vacancy(self, old_vacancy, new_vacancy):
        """
        Обновляет вакансию в файле.

        Параметры:
        ----------
        old_vacancy : Vacancy
            Объект старой вакансии.
        new_vacancy : Vacancy
            Объект новой вакансии.
        """
        data = self._read_file()
        if old_vacancy.to_dict() in data:
            data.remove(old_vacancy.to_dict())
            data.append(new_vacancy.to_dict())
            self._write_file(data)
        else:
            print("Вакансия не найдена")

    def update_vacancy_file(self, new_vacancies):
        """
        Дополняет файл новыми вакансиями.

        Параметры:
        ----------
        new_vacancies : list
            Список объектов вакансий для добавления в файл.
        """
        # Загрузка существующих данных
        existing_vacancies = self._read_file()

        # Преобразование новых вакансий в список словарей
        new_vacancies_dict = [vac.to_dict() for vac in new_vacancies]

        # Добавление новых вакансий, если их нет в существующих
        for vacancy in new_vacancies_dict:
            if vacancy not in existing_vacancies:
                existing_vacancies.append(vacancy)

        # Сохранение обновленного списка вакансий в файл
        self._write_file(existing_vacancies)

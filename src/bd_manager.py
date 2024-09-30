import json

import psycopg2
from psycopg2.extras import DictCursor


class DBManager:
    def __init__(self, dbname, user, password, host="localhost", port=5432):
        """
        Инициализация менеджера БД.

        Параметры:
        ----------
        dbname : str
            Название базы данных.
        user : str
            Имя пользователя базы данных.
        password : str
            Пароль для доступа к базе данных.
        host : str
            Хост базы данных.
        port : int
            Порт для подключения к базе данных.
        """
        self.connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        self.connection.autocommit = True

    def tables_exist(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'companies')")
            companies_exist = cursor.fetchone()[0]
            cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'vacancies')")
            vacancies_exist = cursor.fetchone()[0]
            return companies_exist and vacancies_exist

    def create_tables(self):
        """
        Создает таблицы companies и vacancies.
        """
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS companies (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    employer_id INTEGER UNIQUE NOT NULL
                );
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS vacancies (
                    id SERIAL PRIMARY KEY,
                    company_id INTEGER REFERENCES companies(id),
                    title VARCHAR(255),
                    salary_min INTEGER,
                    salary_max INTEGER,
                    url VARCHAR(255),
                    description TEXT,
                    published_at TIMESTAMP
                );
            """
            )

    def insert_company(self, name, employer_id):
        """
        Вставляет новую компанию в таблицу companies.
        """
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO companies (name, employer_id) VALUES (%s, %s) ON CONFLICT (employer_id) DO NOTHING;",
                (name, employer_id),
            )

    def insert_vacancy(self, company_id, title, salary_min, salary_max, url, description, published_at):
        """
        Вставляет вакансию в таблицу vacancies.
        """
        with self.connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO vacancies (company_id, title, salary_min, salary_max, url, description, published_at)
                   VALUES (%s, %s, %s, %s, %s, %s, %s);""",
                (company_id, title, salary_min, salary_max, url, description, published_at),
            )

    def load_companies_from_json(self, file_path):
        """
        Загружает данные о компаниях из JSON-файла и вставляет их в таблицу companies.

        Параметры:
        ----------
        file_path : str
            Путь до файла с данными компаний.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            companies = json.load(file)

        for company in companies:
            name = company["name"]
            employer_id = company["employer_id"]
            self.insert_company(name, employer_id)

    def get_all_companies(self):
        """
        Получает все компании из таблицы companies.

        Возвращает:
        ----------
        companies : list
            Список компаний с их именами и employer_id.
        """
        with self.connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT id, name, employer_id FROM companies;")
            return cursor.fetchall()

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        with self.connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                """
                SELECT c.name, COUNT(v.id) as vacancies_count
                FROM companies c
                LEFT JOIN vacancies v ON c.id = v.company_id
                GROUP BY c.id;
            """
            )
            return cursor.fetchall()

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.
        """
        with self.connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                """
                SELECT c.name as company_name, v.title as vacancy_title, v.salary_min, v.salary_max, v.url
                FROM vacancies v
                JOIN companies c ON v.company_id = c.id;
            """
            )
            return cursor.fetchall()

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        """
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT AVG(COALESCE(salary_min, salary_max, 0)) as avg_salary
                FROM vacancies;
            """
            )
            return cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней.
        """
        avg_salary = self.get_avg_salary()
        with self.connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                """
                SELECT c.name as company_name, v.title as vacancy_title, v.salary_min, v.salary_max, v.url
                FROM vacancies v
                JOIN companies c ON v.company_id = c.id
                WHERE ((v.salary_min + v.salary_max) / 2) > %s;
            """,
                (avg_salary,),
            )
            return cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова.
        """
        with self.connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                """
                SELECT c.name as company_name, v.title as vacancy_title, v.salary_min, v.salary_max, v.url
                FROM vacancies v
                JOIN companies c ON v.company_id = c.id
                WHERE v.title ILIKE %s;
            """,
                (f"%{keyword}%",),
            )
            return cursor.fetchall()

    def clear_vacancies_table(self):
        with self.connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("""TRUNCATE TABLE vacancies""")
        self.connection.commit()

    def close(self):
        """
        Закрывает соединение с базой данных.
        """
        self.connection.close()

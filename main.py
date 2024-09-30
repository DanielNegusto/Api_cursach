import os
from datetime import datetime

from dotenv import load_dotenv

from src.API import HeadHunterAPI
from src.bd_manager import DBManager

load_dotenv()


def user_interaction():
    # Подключение к базе данных
    db = DBManager(os.getenv("DB_NAME"), os.getenv("DB_USER"), os.getenv("DB_PASSWORD"))

    # Проверяем наличие таблиц
    if not db.tables_exist():
        db.create_tables()
        print("Таблицы созданы.")

    # Загружаем компании из JSON
    db.load_companies_from_json("data/companies.json")

    while True:
        print("\nДобро пожаловать в систему управления вакансиями!")
        print("Выберите действие:")
        print("1. Загрузить данные о компаниях и вакансиях в базу данных")
        print("2. Показать список компаний и количество вакансий у каждой")
        print("3. Показать все вакансии")
        print("4. Показать среднюю зарплату по вакансиям")
        print("5. Показать вакансии с зарплатой выше средней")
        print("6. Поиск вакансий по ключевому слову")
        print("7. Очистить базу данных")
        print("8. Добавить компанию в базу данных")
        print("9. Выйти")

        choice = input("Введите номер действия: ")

        if choice == "1":
            api = HeadHunterAPI()
            companies = db.get_all_companies()

            for company in companies:
                if "id" in company and company["id"] is not None:
                    company_id = company["id"]
                    employer_id = company["employer_id"]  # Используем employer_id
                    vacancies = api.get_company_vacancies(employer_id)

                    for vacancy in vacancies.get("items", []):
                        title = vacancy["name"]  # Название вакансии
                        salary_min = vacancy["salary"]["from"] if vacancy["salary"] else None  # Минимальная зарплата
                        salary_max = vacancy["salary"]["to"] if vacancy["salary"] else None  # Максимальная зарплата
                        url = vacancy["alternate_url"]  # Ссылка на вакансию
                        description = (
                            vacancy["snippet"]["responsibility"] if "snippet" in vacancy else None
                        )  # Описание вакансии
                        published_at = datetime.fromisoformat(
                            vacancy["published_at"].replace("Z", "+00:00")
                        )  # Дата публикации

                        # Вставка вакансии в базу данных
                        db.insert_vacancy(
                            company_id=company_id,
                            title=title,
                            salary_min=salary_min,
                            salary_max=salary_max,
                            url=url,
                            description=description,
                            published_at=published_at,
                        )
                else:
                    print(f"Skipping company with no id: {company}")

            print("Данные успешно загружены в базу данных.")

        elif choice == "2":
            # Показать список компаний и количество вакансий
            companies_and_vacancies = db.get_companies_and_vacancies_count()
            for row in companies_and_vacancies:
                print(f"Компания: {row['name']}, Количество вакансий: {row['vacancies_count']}")

        elif choice == "3":
            # Показать все вакансии
            vacancies = db.get_all_vacancies()
            for vacancy in vacancies:
                print(
                    f"Компания: {vacancy['company_name']}, Вакансия: {vacancy['vacancy_title']}, "
                    f"Зарплата: от {vacancy['salary_min']} до {vacancy['salary_max']}, Ссылка: {vacancy['url']}"
                )

        elif choice == "4":
            # Показать среднюю зарплату
            avg_salary = db.get_avg_salary()
            print(f"Средняя зарплата по всем вакансиям: {avg_salary}")

        elif choice == "5":
            # Показать вакансии с зарплатой выше средней
            vacancies = db.get_vacancies_with_higher_salary()
            for vacancy in vacancies:
                print(
                    f"Компания: {vacancy['company_name']}, Вакансия: {vacancy['vacancy_title']}, "
                    f"Зарплата: от {vacancy['salary_min']} до {vacancy['salary_max']}, Ссылка: {vacancy['url']}"
                )

        elif choice == "6":
            # Поиск вакансий по ключевому слову
            keyword = input("Введите ключевое слово для поиска: ")
            vacancies = db.get_vacancies_with_keyword(keyword)
            for vacancy in vacancies:
                print(
                    f"Компания: {vacancy['company_name']}, Вакансия: {vacancy['vacancy_title']}, "
                    f"Зарплата: от {vacancy['salary_min']} до {vacancy['salary_max']}, Ссылка: {vacancy['url']}"
                )

        elif choice == "7":
            db.clear_vacancies_table()
            print("База данных очищена.")

        elif choice == "8":
            # Добавить компанию
            employer_id = input("Введите employer_id компании: ")
            api = HeadHunterAPI()
            company_info = api.get_employer(employer_id)
            if company_info:
                company_name = company_info["name"]
                print(f"Компания с employer_id {employer_id} найдена: {company_name}")
                response = input("Добавить компанию в базу данных? (да/нет): ")
                if response.lower() == "да":
                    db.insert_company(company_name, employer_id)
                    print("Компания добавлена в базу данных.")
                else:
                    print("Компания не добавлена.")
            else:
                print("Компания с таким employer_id не найдена.")

        elif choice == "9":
            # Выйти из программы
            db.close()
            print("Программа завершена.")
            break

        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")


if __name__ == "__main__":
    user_interaction()

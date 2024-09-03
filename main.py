from src.classes import HeadHunterAPI, JSONSaver, Vacancy
from src.utils import (filter_vacancies, get_top_vacancies, get_vacancies_by_salary, print_vacancies,
                       prompt_for_file_overwrite, sort_vacancies)


def user_interaction():
    json_saver = JSONSaver()
    print("Добро пожаловать в программу поиска вакансий на hh.ru!")

    query = input("Введите вакансию, по которой вы хотите найти информацию: ")
    vacancies_list = hh_api.get_vacancies(query)
    vacancies = Vacancy.cast_to_object_list(vacancies_list)

    json_saver.update_vacancy_file(vacancies)
    print("Вакансии сохранены в файл.")

    while True:
        print("1. Фильтровать вакансии по ключевым словам")
        print("2. Получить вакансии в определенном диапазоне зарплат")
        print("3. Сортировать вакансии по зарплате")
        print("4. Получить топ N вакансий")
        print("5. Печать всех вакансий")
        print("6. Изменить поисковый запрос")
        print("7. Выход")

        choice = input("Введите номер действия: ")

        if choice == "1":
            keywords = input("Введите ключевые слова для фильтрации: ").split()
            filtered_vacancies = filter_vacancies(vacancies, keywords)
            prompt_for_file_overwrite(json_saver, filtered_vacancies)
            print_vacancies(filtered_vacancies)

        elif choice == "2":
            salary_range = input("Введите диапазон зарплат (например, 50000-100000): ")
            filtered_vacancies = get_vacancies_by_salary(vacancies, salary_range)
            prompt_for_file_overwrite(json_saver, filtered_vacancies)
            print_vacancies(filtered_vacancies)

        elif choice == "3":
            sorted_vacancies = sort_vacancies(vacancies)
            prompt_for_file_overwrite(json_saver, sorted_vacancies)
            print_vacancies(sorted_vacancies)

        elif choice == "4":
            top_n = int(input("Введите количество вакансий для вывода: "))
            top_vacancies = get_top_vacancies(sort_vacancies(vacancies), top_n)
            prompt_for_file_overwrite(json_saver, top_vacancies)
            print_vacancies(top_vacancies)

        elif choice == "5":
            print_vacancies(vacancies)

        elif choice == "6":
            query = input("Введите новую вакансию для поиска: ")
            vacancies_list = hh_api.get_vacancies(query)
            vacancies = Vacancy.cast_to_object_list(vacancies_list)
            print("Поисковый запрос изменен.")

        elif choice == "7":
            print("До свидания!")
            break

        else:
            print("Неправильный выбор. Попробуйте еще раз.")


if __name__ == "__main__":
    hh_api = HeadHunterAPI()
    user_interaction()

from src.API import HeadHunterAPI
from src.file_handler import JSONSaver
from src.vacancy import Vacancy, filter_vacancies, print_vacancies, get_vacancies_by_salary, sort_vacancies, \
    get_top_vacancies


def user_interaction():
    json_saver = JSONSaver()
    print("Добро пожаловать в программу поиска вакансий на hh.ru!")

    while True:
        query = input("Введите вакансию, по которой вы хотите найти информацию: ")
        vacancies_list = hh_api.get_vacancies(query)
        vacancies = Vacancy.cast_to_object_list(vacancies_list)

        if vacancies:
            print("Найдены вакансии по вашему запросу.")
            break
        else:
            print("Вакансий по вашему запросу не найдено. Попробуйте другой запрос.")

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
            print_vacancies(filtered_vacancies)
            if filtered_vacancies:
                save_choice = input("Хотите сохранить отфильтрованные вакансии в файл? (да/нет): ")
                if save_choice.lower() == "да":
                    json_saver.update_vacancy_file(filtered_vacancies)
                    print("Отфильтрованные вакансии сохранены в файл.")
            else:
                print("Вакансий по заданным ключевым словам не найдено.")

        elif choice == "2":
            salary_range = input("Введите диапазон зарплат (например, 50000-100000): ")
            filtered_vacancies = get_vacancies_by_salary(vacancies, salary_range)
            print_vacancies(filtered_vacancies)
            if filtered_vacancies:
                save_choice = input("Хотите сохранить вакансии в файл? (да/нет): ")
                if save_choice.lower() == "да":
                    json_saver.update_vacancy_file(filtered_vacancies)
                    print("Вакансии в заданном диапазоне зарплат сохранены в файл.")
            else:
                print("Вакансий в заданном диапазоне зарплат не найдено.")

        elif choice == "3":
            sorted_vacancies = sort_vacancies(vacancies)
            print_vacancies(sorted_vacancies)
            save_choice = input("Хотите сохранить отсортированные вакансии в файл? (да/нет): ")
            if save_choice.lower() == "да":
                json_saver.update_vacancy_file(sorted_vacancies)
                print("Отсортированные вакансии сохранены в файл.")

        elif choice == "4":
            top_n = int(input("Введите количество вакансий для вывода: "))
            top_vacancies = get_top_vacancies(sort_vacancies(vacancies), top_n)
            print_vacancies(top_vacancies)
            save_choice = input(f"Хотите сохранить топ {top_n} вакансий в файл? (да/нет): ")
            if save_choice.lower() == "да":
                json_saver.update_vacancy_file(top_vacancies)
                print(f"Топ {top_n} вакансий сохранены в файл.")

        elif choice == "5":
            print_vacancies(vacancies)

        elif choice == "6":
            while True:
                query = input("Введите новую вакансию для поиска: ")
                vacancies_list = hh_api.get_vacancies(query)
                vacancies = Vacancy.cast_to_object_list(vacancies_list)
                if vacancies:
                    print("Найдены вакансии по вашему новому запросу.")
                    break
                else:
                    print("Вакансий по вашему новому запросу не найдено. Попробуйте другой запрос.")
            print("Поисковый запрос изменен.")

        elif choice == "7":
            print("До свидания!")
            break

        else:
            print("Неправильный выбор. Попробуйте еще раз.")





if __name__ == "__main__":
    hh_api = HeadHunterAPI()
    user_interaction()

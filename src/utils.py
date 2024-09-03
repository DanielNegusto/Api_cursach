def filter_vacancies(vacancies, keywords):
    return [
        v for v in vacancies if any(keyword.lower() in (v.title + v.area + v.employer).lower() for keyword in keywords)
    ]


def get_vacancies_by_salary(vacancies, salary_range):
    if "-" not in salary_range:
        print("Неправильный формат диапазона зарплаты. Пожалуйста, используйте формат 'in-max'.")
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
        v
        for v in vacancies
        if (is_in_range(v.salary_from, min_salary, max_salary) or is_in_range(v.salary_to, min_salary, max_salary))
    ]


def sort_vacancies(vacancies):
    def get_salary(v):
        salary_from = int(v.salary_from.replace(" ", "")) if v.salary_from is not None else 0
        salary_to = int(v.salary_to.replace(" ", "")) if v.salary_to is not None else 0
        return salary_from, salary_to

    return sorted(vacancies, key=get_salary, reverse=True)


def get_top_vacancies(vacancies, top_n):
    return vacancies[:top_n]


def print_vacancies(vacancies):
    for vacancy in vacancies:
        print(
            f"\nВакансия: {vacancy.title}\nЗарплата: {vacancy.salary_from} - {vacancy.salary_to} {vacancy.currency}"
            f"Регион: {vacancy.area}\nРаботодатель: {vacancy.employer}\n"
        )


def prompt_for_file_overwrite(json_saver, sorted_vacancies):
    """Запрашивает у пользователя подтверждение на перезапись файла и обновляет файл, если пользователь согласен."""
    while True:
        overwrite_choice = (
            input("Вы хотите перезаписать файл с отсортированными вакансиями? (да/нет): ").strip().lower()
        )
        if overwrite_choice == "да":
            json_saver.update_vacancy_file(sorted_vacancies)
            print("Файл с вакансиями успешно перезаписан.")
            break
        elif overwrite_choice == "нет":
            print("Изменения не сохранены.")
            break
        else:
            print("Пожалуйста, введите 'да' или 'нет'.")

# Программа для работы с поиском вакансий
## Описание проекта

Проект, который получает информацию о вакансиях с платформы hh.ru в России, сохраняет их в файл и позволяет удобно работать с ними: добавлять, фильтровать, удалять.

## Установка

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/your-repo/project-name.git
    ```

2. Перейдите в директорию проекта:
    ```bash
    cd project-name
    ```

3. Установите необходимые зависимости:
    ```bash
    # для первичной установки
    poetry install
    # для обновления
    poetry update
    ```
## Использование
В проекте реализованны классы для поиска по api вакансий, также сохранения в
файл.
Также в проекте реализована главная функция для взаимодействия с пользователем:
1. Фильтровать вакансии по ключевым словам
2. Получить вакансии в определенном диапазоне зарплат
3. Сортировать вакансии по зарплате
4. Получить топ N вакансий
5. Печать всех вакансий
6. Изменить поисковый запрос


### Данные которые можно получить используя данную программу
- Информация о вакансиях, полученная с разных платформ, сохраненная в JSON-файл в директории "data/".
- Отфильтрованные и отсортированные вакансии, выводимые пользователю через консоль.

## Запуск программы
Основная логика проекта заложена в модуле "main.py" которая связывает функциональности между собой.
для того чтобы запустить программу либо запустите файл main.py из директории проекта, либо через консоль
```bash
poetry run python main.py
```
# Тестирование
Для тестирования используйте библиотеку pytest. В проекте включены тесты для всех основных функций.

# Запуск тестов
Убедитесь, что у вас установлен pytest

Запустите тесты из корневой директории проекта:
```bash
pytest
```
### Проект покрыт тестами с использованием pytest. Для запуска тестов выполните команду:

```bash
pytest --cov
```
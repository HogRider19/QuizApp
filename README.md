<h2 align="center">QuizApp</h2>


### Описание проекта:
Веб проект для прохождения тестов 

### Инструменты разработки

**Стек:**
- Python = 3.9
- Django = 4.0.6
- Postgresql = 15

## Запуск проекта

##### 1) Клонировать репозиторий

    git clone ссылка_сгенерированная_в_вашем_репозитории

##### 2) Создать виртуальное окружение

    python -m venv venv
    
##### 3) Активировать виртуальное окружение
    
    venv/Scripts/activate

##### 4) Устанавливить зависимости:

    pip install -r requirements.txt

##### 5) Создать .env файл:

    DEBUG=
    DB_PORT=5432
    POSTGRES_USER=
    POSTGRES_DB=
    POSTGRES_PASSWORD=
    DB_HOST=

##### 6) Перейти в папку с проектом

    cd .\QuizApp\
    
##### 7) Выполнить команду для выполнения миграций

    python manage.py migrate
    
##### 8) Создать суперпользователя

    python manage.py createsuperuser
    
##### 9) Запустить сервер

    python manage.py runserver
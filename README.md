# Древовидное меню на Django

Этот проект представляет собой простое приложение для Django, которое реализует древовидное меню согласно требованиям задания.

## Установка

1. Склонируйте репозиторий:
```bash
git clone https://github.com/Pu104ver/tree_menu.git
```

2. Перейдите в корневую директорию проекта (в этой директории расположен manage.py)
```bash
cd tree_menu
```

3. Создайте виртуальное окружение:
```base
virtualenv venv
```

4. Активируйте виртуальное окружение:
Для Linux/macOS
```bash
source venv/bin/activate
```
Для Windows
```bash
venv\Scripts\activate
```

5. Установите зависимости:
```bash
pip install -r requirements.txt
```

6. Создайте файл .env в корневой директории проекта и заполните его данными (если требуется).

7. Создайте и примените миграции:

```bash
python manage.py makemigrations
python manage.py migrate
```

8. Создайте супер-пользователя:
```base
   python manage.py createsuperuser
```

9. Запустите сервер:
```bash
python manage.py runserver
```

## Использование

1. Если у вас нет установленного PostgreSQL, то в файле config/settings.py закомментируйте текущую переменную DATABASES, исопльзующую 'ENGINE': 'django.db.backends.postgresql', и расскоментурйте/вставьте следующий код:
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
После этого примените миграции:
```base
python manage.py migrate
```
2. Создайте меню в админке Django, используя модель `MenuItem` (http://127.0.0.1:8000/admin).
3. Добавьте еще больше меню.
4. Перезапустите страницу (http://127.0.0.1:8000/menu)
5. Вы увидите древовидное меню в соотвествии с указанной иерархией при создании.

## Особенности

- Реализовано через шаблонный тег Django, согласно требованиям задания.
- Поддерживает множество меню на одной странице.
- Активный пункт меню определяется автоматически исходя из URL текущей страницы.
- Пункты меню сортируюся по заголовокам.
- SECRET_KEY для файла .env можно сгенерировать на сайте https://djecrety.ir/ (Пример ключа: _9*t^han!8@5516c3ru-aj7h%*-^2u(*set4etfq0(pe+%w@!p)

## Пример .env файла:
SECRET_KEY=YOUR_DJANGO_SECRET_KEY
DB_NAME=YOUR_DB_NAME
DB_USER=YOUR_DB_USER
DB_PASSWORD=YOUR_DB_PASSWORD

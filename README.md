Проект Тимофеева Илья Вячеславовича для участия в полуфинале олимпиады "Траектория Будущего 2024"
Реализован сайт, где пользователь регистрируется и получает 5000 баланса для игры. Пользователь может увеличивать свой баланс, ставя новый рекорд, что фиксируется на сайте. Если баланс потрачен, он может нажать на кнопку, после чего баланс снова станет 5000. Если пройду в финал, хочу реализовать возможность игры в несколько рук, таблицу лидеров сайта, возможность сплитовать и страховаться. Основные аспекты игры в BlackJack реализованы, а также возможность вернуть ставку и удвоиться.
Для реализации используется REST API архитектура с ООП подходом к игре.
Стек технологий - Django, sqlite3, DRF, Redis + front-end.
Каждый файл содержит комментарии.
Структура проекта: папка blackjack_core отвечает за настройки сайта и его компонентов; blackjack - приложения для отоброжения всех страниц, регистрации, авторизации и тд; game_logic_api - приложение, где реализована вся логика игры, основные файлы с логикой - logic и views; user_app - приложение, отвечающее за кастомную реализцию модели пользователей в БД, templates - html страницы.

Для запуска сайта на локальной машине произведите следующие действия:
1) Откройте терминал в директории проекта, либо откройте терминал в IDE
             Линукс
2) Если вы на линукс, тогда установите виртуальное окружение <virtualenv venv -p python3.10>
3) Активируйте его <source venv/bin/activate>
4) Установите необходимые зависимости <pip install -r requirements.txt>
5) Там же создайте миграции <python manage.py makemigrations>
6) Проведите миграции <python manage.py migrate>
7) Запустите сервер <python manage.py runserver>
8) Пользуйтесь ( http://127.0.0.1:8000/)
             Windows
2) Создайте виртуальное окружение, легче всего в pycharm
3) Пропишите в терминал pycharm (либо в сmd) <pip install -r requirements.txt>
4) Там же создайте миграции <python manage.py makemigrations>
5) Проведите миграции <python manage.py migrate>
6) Пользуйтесь (http://127.0.0.1:8000/)

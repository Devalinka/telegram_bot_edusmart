# telegram_bot_edusmart

EduSmart - это Telegram-бот для онлайн школы, который помогает пользователям выбирать курсы, записываться на них и оставлять отзывы. 

## Основные функции бота:
1. Приветственное сообщение с отправкой стикера.
2. Информация о курсах с возможностью выбора направления и уровня.
3. Отзывы студентов с навигацией.
4. Запись на курсы.
5. Отправка сообщения менеджеру.
6. Показ записей из базы данных.

## Установка

1. Клонируйте репозиторий:
    ```sh
    git clone https://github.com/yourusername/edusmart-telegram-bot.git
    ```

2. Перейдите в директорию проекта:
    ```sh
    cd edusmart-telegram-bot
    ```

3. Создайте виртуальное окружение и активируйте его:
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # Для Windows используйте: .venv\Scripts\activate
    ```

4. Установите зависимости:
    ```sh
    pip install -r requirements.txt
    ```

5. Создайте файл `.env` и добавьте ваш токен Telegram-бота:
    ```sh
    echo TELEGRAM_BOT_TOKEN=your_token_here > .env
    ```

6. Создайте файл базы данных SQLite:
    ```sh
    python -c "import database; database.create_table()"
    ```

## Использование

1. Запустите бота:
    ```sh
    python bot.py
    ```

## Файлы

### bot.py

Главный файл для запуска бота. Содержит настройку бота и диспетчера.

### handlers.py

Файл с обработчиками для команд и сообщений бота.

### text.py

Файл с текстовыми сообщениями, используемыми в боте.

### database.py

Файл для работы с базой данных SQLite. Содержит функции для создания таблиц, добавления и извлечения записей.


## Дополнительная информация

Бот использует библиотеку [aiogram](https://docs.aiogram.dev/en/latest/) для работы с Telegram API.

## Лицензия

Этот проект лицензируется на условиях лицензии MIT. Подробности см. в файле `LICENSE`.


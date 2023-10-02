## Введение
### Телеграм-бот "Holidays"

Данный телеграм-бот предоставляет пользователю информацию о праздниках в разных странах. Пользователь может выбрать страну, категорию праздников и год, после чего получит список всех праздников, удовлетворяющих заданным параметрам. Для получения данных используется API-Ninjas.

## Команды
* /start - начать использование бота и открыть главное меню.

## Главное меню
После вызова команды /start пользователю открывается главное меню, из которого он может выбрать страну, категорию праздников и год.

1. Выбор страны: Пользователь получает список стран и выбирает одну из них.
2. Выбор категории праздников: Пользователю предоставляется список категорий праздников и выбирает одну из них.
3. Ввод года: Пользователь вводит год, который его интересует.

## Получение данных
После того, как пользователь выбрал страну, категорию праздников и год, формируется API-запрос к Holidays by API-Ninjas для получения списка праздников по заданным параметрам. Если по данному запросу ничего не находится, выводится соответствующее сообщение.

Установка и запуск

1. Установите все необходимые зависимости, выполните команду:
         
       pip install python-dotenv
       pip install pyTelegramBotApi
       pip install requests

2. Создайте бота в Telegram и получите токен доступа.

3. Создайте файл .env в корневой директории проекта и добавьте следующие переменные:

   * BOT_TOKEN=ВАШ ТОКЕН ДОСТУПА К БОТУ
   * API_KEY=ВАШ КЛЮЧ К API

4. Создайте файл "feedback.txt"

5. Запустите программу.

Теперь ваш телеграм-бот работает и готов к использованию.
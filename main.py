import telebot
from telebot import types
import requests
from config import BOT_TOKEN, API_KEY
from datetime import datetime

# Основной URL-адрес API
url = "https://holidays-by-api-ninjas.p.rapidapi.com/v1/holidays"


api_host = "holidays-by-api-ninjas.p.rapidapi.com"
api_key = API_KEY
bot = telebot.TeleBot(BOT_TOKEN)

headers = {'X-RapidAPI-Key': api_key, 'X-RapidAPI-Host': api_host}  # Параметры заголовка (API)


holidays_tuple = ('major_holiday', 'public_holiday', 'observance', 'national_holiday', 'federal_holiday', 'season',
                  'state_holiday', 'optional_holiday', 'clock_change_daylight_saving_time', 'local_holiday',
                  'united_nations_observance', 'observance_christian', 'bank_holiday', 'common_local_holiday',
                  'national_holiday_christian', 'christian', 'observance_hebrew', 'jewish_holiday', 'muslim',
                  'hindu_holiday', 'restricted_holiday', 'official_holiday', 'national_holiday_orthodox',
                  'local_observance')  # Кортеж, состоящий из опциональных параметров для API запроса, обозначающих
# категории праздников

holidays_dict = {
                 'btn_major_holiday': 'major_holiday',
                 'btn_public_holiday': 'public_holiday',
                 'btn_observance': 'observance',
                 'btn_national_holiday': 'national_holiday',
                 'btn_season': 'season',
                 'btn_state_holiday': 'state_holiday',
                 'btn_optional_holiday': 'optional_holiday',
                 'btn_clock_change_daylight_saving_time': 'clock_change_daylight_saving_time',
                 'btn_local_holiday': 'local_holiday',
                 'btn_united_nations_observance': 'united_nations_observance',
                 'btn_observance_christian': 'observance_christian',
                 'btn_bank_holiday': 'bank_holiday',
                 'btn_common_local_holiday': 'common_local_holiday',
                 'btn_national_holiday_christian': 'national_holiday_christian',
                 'btn_christian': 'christian',
                 'btn_observance_hebrew': 'observance_hebrew',
                 'btn_jewish_holiday': 'jewish_holiday',
                 'btn_muslim': 'muslim',
                 'btn_hindu_holiday': 'hindu_holiday',
                 'btn_restricted_holiday': 'restricted_holiday',
                 'btn_official_holiday': 'official_holiday',
                 'btn_national_holiday_orthodox': 'national_holiday_orthodox',
                 'btn_local_observance': 'local_observance'
                }  # словарь, где ключи - функции обратного вызова, а значения - опциональные параметры для API запроса,
# обозначающие категории праздников категории праздников


def tool_chunks(lst):
    """
    Функция, служащая вспомогательным инструментом. Разбивает ответ бота на части, чтобы не допустить ошибки 400 в
    связи с избытком символов в одном сообщении
    """
    for i in range(0, len(lst), 100):
        yield lst[i:i + 100]


def tool_callback(callback, holiday_type) -> None:
    """
    Функция, служащая вспомогательным инструментом, чтобы не допускать дублирование кода
    """
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn = types.KeyboardButton(text='MAIN MENU')
    kb.add(btn)
    year = bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text='Enter the year'
                                 ' you are interested in (2010-2023):')
    info_list.append(holiday_type)

    bot.register_next_step_handler(year, review_holidays_search1)


def tool_sort(elem) -> int:
    """
    Функция, служащая вспомогательным инструментом для получения строки формата месяц + число. Впоследствии пригодится
    в создании lambda-функции
    """
    date = elem['date']
    date = date[5:7] + date[8:10]  # Преобразует строку формата гггг-мм-дд в строку формата ммдд. Это позволяет
# сортировать данные от раннего к позднему
    if date[0] == 0:
        date = date[1]
    return int(date)


def tool_exit_text(initial_list, message) -> None:

    """
    Функция, служащая вспомогательным инструментом, которая формирует упорядоченный массив данных формата
    "дата-праздник"
    """

    new_list = sorted(initial_list, key=lambda x: tool_sort(x))
    if len(new_list) > 100:
        for elem in tool_chunks(new_list):

            tool_exit_text(elem, message)

    else:
        final_string = ''
        for elem in new_list:
            final_string += f'{elem["date"]}: {elem["name"]}' + '\n'
        bot.send_message(message.chat.id, final_string)


@bot.message_handler(commands=['start'])
def send_welcome(message) -> None:

    """
    Функция, срабатывающая при первом запуске бота
    """

    bot.reply_to(message, 'The telegram bot you launched is written under the Holidays by API-Ninjas API. With its '
                          'help, you will be able to receive information about the upcoming holidays of your chosen '
                          'country')

    main_menu(message)


@bot.message_handler(func=lambda message: message.text == 'MAIN MENU')
def main_menu(message) -> None:

    """
    Функция, которая служит для перемещения пользователя в главное меню бота. Здесь ему будет предложен выбор страны,
    информацию о праздниках которой он хочет знать
    """

    global info_list
    info_list = []
    global checker_list
    checker_list = []
    checker_list.append('0')
    # bot.send_message(message.chat.id, 'Select the country whose holiday information you want to receive: ')

    country = bot.send_message(message.chat.id, 'Select the country whose holiday information you want to receive:\n'
                                                'Azerbaijan 🇦🇿 - /Azerbaijan \nArmenia 🇦🇲 - /Armenia\nBelarus 🇧🇾- '
                                                '/Belarus\nKazakhstan 🇰🇿 - /Kazakhstan \nKyrgyzstan 🇰🇬 - /Kyrgyzstan\n'
                                                'Moldova 🇲🇩 - /Moldova\nRussia 🇷🇺 - /Russia\nTajikistan - 🇹🇯 /'
                                                'Tajikistan\nUzbekistan 🇺🇿 - /Uzbekistan',
                               reply_markup=types.ReplyKeyboardRemove(), parse_mode='Markdown')

    bot.register_next_step_handler(country, review_holidays_menu)


def review_holidays_menu(message):

    """
    Функция, которая проверяет ответ пользователя. Если его ответ "MAIN MENU", то перемещает его в главное меню,
    иначе - даёт выбор из Inline-кнопок, каждая из которой обозначает какую-то категорию праздников
    """

    if message.text != 'MAIN MENU' and checker_list[-1] != 'review_holidays_menu' and message.text != '/start':
        checker_list.append('review_holidays_menu')
        info_list.append(message.text)
        kb_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        kb = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.KeyboardButton('MAIN MENU')
        buttons = (('All holidays', 'btn_all_holidays'),
                   ('Major holiday', 'btn_major_holiday'),
                   ('Public holiday', 'btn_public_holiday'),
                   ('Observance', 'btn_observance'),
                   ('National holiday', 'btn_national_holiday'),
                   ('Season', 'btn_season'),
                   ('State holiday', 'btn_state_holiday'),
                   ('Optional holiday', 'btn_optional_holiday'),
                   ('Clock change daylight saving time', 'btn_clock_change_daylight_saving_time'),
                   ('Local holiday', 'btn_local_holiday'),
                   ('United nations observance', 'btn_united_nations_observance'),
                   ('Observance christian', 'btn_observance_christian'),
                   ('Bank holiday', 'btn_bank_holiday'),
                   ('Common local holiday', 'btn_common_local_holiday'),
                   ('National holiday christian', 'btn_national_holiday_christian'),
                   ('Christian', 'btn_christian'),
                   ('Observance hebrew', 'btn_observance_hebrew'),
                   ('Jewish holiday', 'btn_jewish_holiday'),
                   ('Muslim', 'btn_muslim'),
                   ('Hindu holiday', 'btn_hindu_holiday'),
                   ('Restricted holiday', 'btn_restricted_holiday'),
                   ('Official holiday', 'btn_official_holiday'),
                   ('National holiday orthodox', 'btn_national_holiday_orthodox'),
                   ('Local observance', 'btn_local_observance')
                   )
        inline_buttons = [types.InlineKeyboardButton(text=text, callback_data=callback) for text, callback, in buttons]
        kb_keyboard.add(btn1)
        kb.add(*inline_buttons)
        bot.send_message(message.chat.id, 'Choose the holiday category: ', reply_markup=kb)
        bot.send_message(message.chat.id, 'If you want to change the country you can do it now.  Just press "MAIN '
                                          'MENU" button.', reply_markup=kb_keyboard)

    elif checker_list[-1] == 'review_holidays_menu':
        pass
    elif message.text == '/start':
        send_welcome(message)
    else:
        main_menu(message)


@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback(callback):

    """
    Функция, которая проверяет, какую кнопку выбрал пользователь
    """

    checker_list.append('0')
    if not callback.data == 'btn_all_holidays':

        tool_callback(callback, holiday_type=holidays_dict[callback.data])
    else:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn = types.KeyboardButton(text='MAIN MENU')
        kb.add(btn)
        year = bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                                     text='Enter the year you are interested in (2010-2023):')

        bot.register_next_step_handler(year, review_holidays_search2)


def review_holidays_search1(message):

    """
    Функция, которая срабатывает если пользователь выбрал любую из кнопок, кроме "All holidays". Отвечает за поиск
    и вывод праздников по заданным параметрам
    """

    if not message.text == 'MAIN MENU':
        bot.send_message(message.chat.id, 'Please, wait...')
        querystring = {"country": info_list[0][1:], "year": message.text, "type": info_list[1]}
        response = requests.get(url, headers=headers, params=querystring)
        if not response.json():
            bot.send_message(message.chat.id, 'Nothing was found for your query')
        else:
            # final_string = tool_exit_text(response.json())
            #
            # bot.send_message(message.chat.id, final_string)
            tool_exit_text(response.json(), message)
        answer = bot.send_message(message.chat.id,
                                  'If you want it, you can leave a /feedback. It will help to make the bot better')
        bot.register_next_step_handler(answer, review_get_feedback)

    else:
        main_menu(message)


def review_holidays_search2(message):

    """
    Функция, которая срабатывает если пользователь выбрал кнопку "All holidays". Отвечает за поиск
    и вывод праздников по заданным параметрам
    """

    if not message.text == 'MAIN MENU':

        bot.send_message(message.chat.id, 'Please, wait...')
        counter = 0
        tempo_list2 = []
        for holiday_category in holidays_tuple:
            counter += 1

            querystring = {"country": info_list[0][1:], "year": message.text, "type": holiday_category}
            response = requests.get(url, headers=headers, params=querystring)
            for elem in response.json():
                elem = {'name': elem['name'], 'date': elem['date']}

                tempo_list2.append(elem)
        if not tempo_list2:
            bot.send_message(message.chat.id, 'Nothing was found for your query')
        else:

            tool_exit_text(tempo_list2, message)

        answer = bot.send_message(message.chat.id,
                                  'If you want it, you can leave a /feedback. It will help to make the bot better')
        bot.register_next_step_handler(answer, review_get_feedback)
    else:

        main_menu(message)


def review_get_feedback(message) -> None:

    """
    Функция, которая проверяет ответ пользователя, и если он выбрал команду "feedback", принимает отзыв пользователя.
    Иначе - отправляет его в главное меню
    """

    if message.text == '/feedback':
        feedback = bot.send_message(message.chat.id, 'Thank you! Please leave your feedback here:')
        bot.register_next_step_handler(feedback, review_save_feedback)
    else:
        main_menu(message)


def review_save_feedback(message):

    """
    Функция, которая записывает отзыв пользователя в файл feedback.txt
    """

    with open('feedback.txt', 'a') as file:
        file.write(str(datetime.now()))
        file.write(message.text)
        file.write('\n')
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn = types.KeyboardButton(text='MAIN MENU')
    kb.add(btn)
    bot.send_message(message.chat.id, 'Thank you one more time! Now you can go to main menu and check some '
                                      'information again', reply_markup=kb)


if __name__ == '__main__':
    bot.polling()


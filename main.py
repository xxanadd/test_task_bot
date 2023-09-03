import telebot
from telebot import types
import requests

bot = telebot.TeleBot('6539976069:AAHoXkiOTr9rr_2gIU0uQVAZSIXKgWXnMXk')

# Глобальные переменные для хранения id и выбранной таблицы
user_id = None
selected_table = None


# Базовый URL для запросов
base_url = "http://localhost:8000/"


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item1 = types.KeyboardButton("Получить данные из собранной таблицы")
    item2 = types.KeyboardButton("Получить данные из родительских таблиц")
    markup.add(item1, item2)

    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Получить данные из собранной таблицы")
def get_data_from_assembled_table(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item1 = types.KeyboardButton("Получить данные по id")
    item2 = types.KeyboardButton("Получить все данные")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Получить данные по id")
def get_data_by_id(message):
    global selected_table
    selected_table = "assembled"  # Выбираем собранную таблицу
    markup = types.ReplyKeyboardRemove()  # Удаляем клавиатуру
    bot.send_message(message.chat.id, "Введите id:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Получить все данные")
def get_all_data(message):
    global selected_table
    selected_table = "assembled"  # Выбираем собранную таблицу
    markup = types.ReplyKeyboardRemove()  # Удаляем клавиатуру
    # Формируем URL для запроса "Получить все данные"
    url = f"{base_url}get-all"

    # Отправляем GET-запрос
    response = requests.get(url)

    # Проверяем код состояния ответа
    if response.status_code == 200:
        data = response.json()
        bot.send_message(message.chat.id, f"Данные из собранной таблицы: {data}", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, f"Ошибка при получении данных: {response.status_code}", reply_markup=markup)

    # Сбрасываем выбранную таблицу
    selected_table = None


@bot.message_handler(func=lambda message: message.text == "Получить данные из родительских таблиц")
def get_data_from_parent_tables(message):
    global selected_table
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item1 = types.KeyboardButton("People")
    item2 = types.KeyboardButton("Microorganisms")
    item3 = types.KeyboardButton("Additives")
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, "Выберите таблицу:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "People")
def get_people_data(message):
    global selected_table
    selected_table = "People"
    markup = types.ReplyKeyboardRemove() # Удаляем клавиатуру
    bot.send_message(message.chat.id, "Введите id:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Microorganisms")
def get_microorganisms_data(message):
    global selected_table
    selected_table = "Microorganisms"
    markup = types.ReplyKeyboardRemove()  # Удаляем клавиатуру
    bot.send_message(message.chat.id, "Введите id:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Additives")
def get_additives_data(message):
    global selected_table
    selected_table = "Additives"
    markup = types.ReplyKeyboardRemove()  # Удаляем клавиатуру
    bot.send_message(message.chat.id, "Введите id:", reply_markup=markup)


@bot.message_handler(func=lambda message: selected_table is not None)
def get_data(message):
    global user_id, selected_table
    user_id = message.text

    # Формируем URL для запроса
    if selected_table == "assembled":
        if user_id is not None:
            url = f"{base_url}get/{user_id}"
        else:
            bot.send_message(message.chat.id, "Ошибка: Неверный ввод для собранной таблицы.")
            selected_table = None
            return
    elif selected_table in ["People", "Microorganisms", "Additives"]:
        url = f"{base_url}{selected_table.lower()}/get/{user_id}"
    else:
        bot.send_message(message.chat.id, "Ошибка: Неверная таблица.")
        selected_table = None
        return

    # Отправляем GET-запрос
    response = requests.get(url)

    # Проверяем код состояния ответа
    if response.status_code == 200:
        data = response.json()
        bot.send_message(message.chat.id, f"Данные из таблицы '{selected_table}': {data}")
    else:
        bot.send_message(message.chat.id, f"Ошибка при получении данных: {response.status_code}")

    # Сбрасываем выбранную таблицу
    selected_table = None


if __name__ == "__main__":
    bot.polling(none_stop=True)

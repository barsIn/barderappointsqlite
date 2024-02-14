import os, time
import telebot
from datetime import datetime, date, timedelta
from telebot import types
from dotenv import load_dotenv
import schedule
import threading

import messegetext
from messegetext import (greatings, admgreatings, usergrbt1, usergrbt2, usergrbt3, usergrbt4, usergrbt5, admgrbt1, admgrbt2,
                         admgrbt3, admgrbt4, admgrbt5, cancel, unknoun, contact_reqest_text, admgrbt6, usergrbt6)
from commands import (chek_next_appoint_adm, chek_todayadmcmd, chek_tomorrowadmcmd, date_check, chek_alldaymcmd, get_weekends_adm, weekdate_check,
                      holyday_check, get_holydays_adm, get_worktime_adm, worktime_check, create_user, update_user, get_next_apoint,
                      make_current_appoint, chek_day_appoit_user, time_check, get_app_times, get_my_appoint,
                      get_user_data, make_change_user_data, check_number, create_user_byadm, get_black_list_all,
                      search_by_telephon, search_by_name, search_by_appoint)
from sqlcommands import (get_adms, set_adms, remove_adms, get_usersid_sql, create_current_appoint, update_current_appoint_type,
                         delete_current, get_current_date, update_current_appoint_time, delete_appoint,
                         get_my_appoint_with_id_sql, delete_appoint_id, remove_from_black_list, add_to_black_list,
                         get_id_from_black_list, clear_current)


# my_user_id = []
my_user_id = get_adms()
load_dotenv()
# my_user_id = eval(os.getenv('MY_USER_ID'))

API_TOKEN = os.getenv('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)
clear_current()
@bot.message_handler(commands=['start'])
def starting(message):
    if message.from_user.id in my_user_id:
        kb1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2, resize_keyboard=True, )
        button1 = types.KeyboardButton(admgrbt1)
        button2 = types.KeyboardButton(admgrbt2)
        button3 = types.KeyboardButton(admgrbt3)
        button4 = types.KeyboardButton(admgrbt4)
        button5 = types.KeyboardButton(admgrbt5)
        button6 = types.KeyboardButton(admgrbt6)
        kb1.add(button1, button2, button3, button4, button5, button6)
        bot.send_message(message.chat.id, admgreatings, reply_markup=kb1)
    else:
        kb1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2, resize_keyboard=True, )
        button1 = types.KeyboardButton(usergrbt1)
        button2 = types.KeyboardButton(usergrbt3)
        button3 = types.KeyboardButton(usergrbt4)
        button4 = types.KeyboardButton(usergrbt5)
        button5 = types.KeyboardButton(usergrbt2)
        button6 = types.KeyboardButton(usergrbt6)
        kb1.add(button1, button2, button3, button4, button5, button6)
        bot.send_message(message.chat.id, greatings, reply_markup=kb1)


# Админ проверка ближайшей записи
@bot.message_handler(func=lambda message: message.text == admgrbt1 and message.from_user.id in my_user_id)
def chek_next_appointadmtg(message):
    text = chek_next_appoint_adm()
    bot.send_message(message.chat.id, text)
    time.sleep(3)
    starting(message)


# Админ проверка записей на даты
@bot.message_handler(func=lambda message: message.text == admgrbt2 and message.from_user.id in my_user_id)
def chek_date_appointadmin(message):
    text = 'Какой день интересует?'
    kb1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2, resize_keyboard=True, )
    button1 = types.KeyboardButton('Сегодня')
    button2 = types.KeyboardButton('Завтра')
    button3 = types.KeyboardButton('Другая дата')
    kb1.add(button1, button2, button3)
    bot.send_message(message.chat.id, text, reply_markup=kb1)


@bot.message_handler(func=lambda message: message.text == 'Сегодня' and message.from_user.id in my_user_id)
def chek_today(message):
    text = chek_todayadmcmd()
    bot.send_message(message.chat.id, text)
    time.sleep(3)
    starting(message)


@bot.message_handler(func=lambda message: message.text == 'Завтра' and message.from_user.id in my_user_id)
def chek_tomorrowadm(message):
    text = chek_tomorrowadmcmd()
    bot.send_message(message.chat.id, text)
    time.sleep(3)
    starting(message)


# ввод даты после которого последует проверка корректности
@bot.message_handler(func=lambda message: message.text == 'Другая дата' and message.from_user.id in my_user_id)
def chek_anydayadm_input(message):
    text = 'Введи дату в формате дд.мм.гггг.'
    msg = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(msg, chek_anydayadm)


# Проверка записей на конкретную дату
def chek_anydayadm(message):
    text = message.text
    answer = date_check(text)
    if  answer == False:
        if text in cancel:
            starting(message)
        else:
            bot.reply_to(message, 'Неверный формат даты, попробуй еще раз. Введи дату в формате дд.мм.гггг')
            chek_anydayadm_input(message)
    else:
        text = chek_alldaymcmd(answer)
        bot.reply_to(message, text)
        time.sleep(2)
        starting(message)


# Установить рабочие дни недели
@bot.message_handler(func=lambda message: message.text == admgrbt3 and message.from_user.id in my_user_id)
def chek_weekday_input(message):
    weekenddaystext = get_weekends_adm()
    text = f'{weekenddaystext}\nВведи день недели для добавления/удаления дня недели к выходным.'
    msg = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(msg, chek_weekday)


def chek_weekday(message):
    text = message.text.title()
    answer = weekdate_check(text)
    if answer == False:
        if text in cancel:
            starting(message)
        else:
            bot.reply_to(message, 'Неверно указан день недели')
            chek_weekday_input(message)
    else:
        bot.reply_to(message, answer)
        time.sleep(1)
        starting(message)


# Устанавливаем доп выходные после проверки
@bot.message_handler(func=lambda message: message.text == admgrbt4 and message.from_user.id in my_user_id)
def chek_holyday_input(message):
    holydays = get_holydays_adm()
    text = f'{holydays} \nВведи день для добавления/удаления к выходным в формате дд.мм.гггг.'
    msg = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(msg, chek_holyday)


def chek_holyday(message):
    text = message.text
    answer = holyday_check(text)
    if answer == False:
        if text in cancel:
            starting(message)
        else:
            bot.reply_to(message, 'Неверно указан день, попробуй еще раз. Введи дату в формате дд.мм.гггг')
            chek_holyday_input(message)
    else:
        bot.reply_to(message, answer)
        time.sleep(1)
        starting(message)


# Устанавливаем рабочее время после проверки
@bot.message_handler(func=lambda message: message.text == admgrbt5 and message.from_user.id in my_user_id)
def chek_worktime_input(message):
    worktime = get_worktime_adm()
    text = f'{worktime} \nВведи время начала и окончания рабооты через пробел \nКак пример 09:00 19:00.'
    msg = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(msg, chek_worktime)

def chek_worktime(message):
    text = message.text
    answer = worktime_check(text)
    if answer == False:
        if text in cancel:
            starting(message)
        else:
            text = 'Проблема с форматом времени, попробуйте еще раз. \nКак пример 09:00 19:00.'
            bot.reply_to(message, text)
            chek_worktime_input(message)
    else:
        bot.reply_to(message, answer)
        time.sleep(1)
        starting(message)


# Записать клиента
@bot.message_handler(func=lambda message: message.text == admgrbt6 and message.from_user.id in my_user_id)
def client_appoint_byadm(message):
    text = f'Введи имя клиента и номер телефона'
    msg = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(msg, client_date)


def client_date(message):
    text = message.text
    text = text.split()
    try:
        name, telephone = text[0], text[1]
        user_id = create_user_byadm(name, telephone)
        kb1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2, resize_keyboard=True, )
        button1 = types.KeyboardButton('Сегодня')
        button2 = types.KeyboardButton('Завтра')
        button3 = types.KeyboardButton('Другая дата')
        kb1.add(button1, button2, button3)
        text1 = f'На какую дату осуществить запись?'
        msg = bot.send_message(message.chat.id, text1, reply_markup=kb1)
        bot.register_next_step_handler(msg, check_client_day, user_id)
    except:
        bot.send_message(message.chat.id, 'Введи через пробел имя и телефон')
        client_appoint_byadm(message)


def check_client_day(message, user_id):
    text = message.text
    if text == 'Сегодня':
        date1 = date.today()
        day2 = date1.strftime('%d.%m.%Y')
        start_appoint_adm(message, date1, day2, user_id)
    elif text == 'Завтра':
        date1 = date.today() + timedelta(days=1)
        day2 = date1.strftime('%d.%m.%Y')
        start_appoint_adm(message, date1, day2, user_id)
    else:
        text = 'Введи дату в формате дд.мм.гггг.'
        msg = bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(msg, check_day_adm, user_id)


def check_day_input_adm(message, user_id):
    text = 'Введи дату в формате дд.мм.гггг.'
    msg = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(msg, check_day_adm, user_id)


def check_day_adm(message, user_id):
    text = message.text
    date1 = date_check(text)
    if date1 == False:
        if text in cancel:
            starting(message)
        else:
            bot.reply_to(message, 'Неверный формат даты, попробуй еще раз. Введи дату в формате дд.мм.гггг')
            check_day_input_adm(message, user_id)
    else:
        day2 = date1.strftime('%d.%m.%Y')
        if date1.date() > date.today():
            start_appoint_adm(message, date1, day2, user_id)
        else:
            text = 'Указана дата из прошлого, попробуте другую дату'
            bot.reply_to(message, text)
            check_day_input_adm(message)


def start_appoint_adm(message, date1, daytext, user_id):
    text = message.text
    daytext = daytext
    day2 = date1.strftime('%d.%m.%Y')
    is_work, workday, days = chek_day_appoit_user(user_id, date1)
    workdaystr = workday.strftime('%d.%m.%Y')
    times = get_app_times(workday)
    kb1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2, resize_keyboard=True, )
    button1 = types.KeyboardButton('Выбрать другой день')
    button2 = types.KeyboardButton('Отмена')
    kb1.add(button1, button2)
    if is_work:
        if len(times) == 0:
            text = f'На {daytext} нет свободного времени'
        else:
            text = f'На {daytext} свободно следующее время:\n'
            for i in times:
                text = text + f'{i}\n'
            text = text + 'Записаться на свободное время, введи его в формате ЧЧ:ММ\nЛибо введи отмена'
    else:
        if len(times) == 0:
            text = f'{day2} выходной, следующий рабочий день {workdaystr} но к сожалению свободного времени на эту дату нет'
        else:
            text = f'{day2} выходной, можно записаться на {workdaystr} свободно следующее время:\n'
            for i in times:
                text = text + f'{i}\n'
            text = text + 'Записаться на свободное время, введи его в формате ЧЧ:ММ\nЛибо введи отмена'
    msg = bot.send_message(message.chat.id, text, reply_markup=kb1)
    bot.register_next_step_handler(msg, check_time_adm, user_id)


def check_time_adm(message, user_id):
    text = message.text
    answer = time_check(text)
    date1 = get_current_date(user_id)[0]
    if text == 'Выбрать другой день':
        delete_current(user_id)
        client_date(message)
    else:
        if answer == False:
            if text in cancel:
                delete_current(user_id)
                starting(message)
            else:
                msg = bot.reply_to(message, 'Неверно указано время, попробуй еще раз. Введи время в формате ЧЧ:ММ')
                bot.register_next_step_handler(msg, check_time_adm)
        else:
            times = get_app_times(date1)
            answer = f'{answer}:00'
            if answer in times:
                update_current_appoint_time(user_id, answer)
                kb1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2, resize_keyboard=True, )
                button1 = types.KeyboardButton('Стрижка')
                button2 = types.KeyboardButton('Борода')
                button3 = types.KeyboardButton('Комплекс')
                kb1.add(button1, button2, button3)
                text = f'Укажи тип стрижки'
                msg = bot.send_message(message.chat.id, text, reply_markup=kb1)
                bot.register_next_step_handler(msg, finish_current_appont_adm, user_id)
            else:
                msg = bot.reply_to(message, 'Указанное время занято или не рабочее')
                bot.register_next_step_handler(msg, check_time_adm, user_id)


def finish_current_appont_adm(message, user_id):
    answer = message.text
    update_current_appoint_type(user_id, answer)
    text = make_current_appoint(user_id)
    bot.send_message(message.chat.id, text)
    time.sleep(2)
    starting(message)


# Запрос Контакта нового пользователя
@bot.message_handler(func=lambda message: message.from_user.id not in get_usersid_sql())
def new_user(message):
    text = f'{unknoun} \n {contact_reqest_text}'
    kb1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1, resize_keyboard=True, )
    button1 = types.KeyboardButton('Передать телефон 📞', request_contact=True)
    button2 = types.KeyboardButton('Отмена', request_contact=True)
    kb1.add(button1, button2)
    msg = bot.send_message(message.chat.id, text, reply_markup=kb1)
    bot.register_next_step_handler(msg, contact_reqest)


def contact_reqest(message):
    if message.content_type == 'contact':
        telephone = message.contact.phone_number
        user_id = message.contact.user_id
        name = message.contact.first_name
        last_name = message.contact.last_name
        if name:
            if last_name:
                user_name = f'{name} {last_name}'
            else:
                user_name = name
        elif last_name:
            user_name = last_name
        else:
            user_name = None
        create_user(user_id, telephone, user_name)
        if user_name:
            text = f'Добро пожаловать {user_name}, теперь для тебя открыт весь функционал'
            bot.send_message(message.chat.id, text)
            time.sleep(1)
            starting(message)
        else:
            text = 'К сожалению у вас не установлено имя пользователя, сообщите нам пожалуйста, для удобства комуникаций'
            msg = bot.send_message(message.chat.id, text)
            bot.register_next_step_handler(msg, name_reqest)
    else:
        if message.text == 'Отмена':
            starting(message)
        else:
            kb1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1, resize_keyboard=True, )
            button1 = types.KeyboardButton('Отмена', request_contact=True)
            kb1.add(button1)
            user_id = message.from_user.id
            telephone = message.text
            create_user(user_id, telephone)
            text = 'Осталось ввести Ваше имя для окончания знакомства'
            msg = bot.send_message(message.chat.id, text, reply_markup=kb1)
            bot.register_next_step_handler(msg, name_reqest)


def name_reqest(message):
    if message.text == 'Отмена':
        starting(message)
    else:
        name = message.text
        id = message.from_user.id
        update_user(id, name)
        text = f'Добро пожаловать {name}, теперь для тебя открыт весь функционал'
        bot.send_message(message.chat.id, text)
        time.sleep(1)
        starting(message)


@bot.message_handler(func=lambda message: message.text == usergrbt1)
def get_next_apoint_user(message):
    if message.chat.id in get_id_from_black_list():
        text = 'Вы в черном списке, обратитесь к администратору'
        bot.reply_to(message, text)
        starting(message)
    else:
        user_id = message.from_user.id
        next_time = get_next_apoint(user_id)
        print(f'Следующая возможная запись {next_time}')
        if len(get_my_appoint_with_id_sql(message.from_user.id)) >= 2:
            answer = 'Нельзя осуществлять больше двух записей, сперва удалите одну'
            bot.send_message(message.chat.id, answer)
            starting(message)
        else:
            kb1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2, resize_keyboard=True, )
            button1 = types.KeyboardButton('Да')
            button2 = types.KeyboardButton('Нет')
            kb1.add(button1, button2)
            create_current_appoint(user_id, next_time[0], next_time[1])
            apdate = next_time[0].strftime('%d.%m.%Y')
            aptime = datetime.strptime(next_time[1], '%H:%M:%S').strftime('%H:%M')
            text = f'Следующая свободная дата для записи {apdate}, в {next_time[1]}\nОсуществить запись?'
            msg = bot.send_message(message.chat.id, text, reply_markup=kb1)
            bot.register_next_step_handler(msg, answer_current_appont)


def answer_current_appont(message):
    answer = message.text
    user_id = message.from_user.id
    if answer == 'Да':
        kb1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2, resize_keyboard=True, )
        button1 = types.KeyboardButton('Стрижка')
        button2 = types.KeyboardButton('Борода')
        button3 = types.KeyboardButton('Комплекс')
        kb1.add(button1, button2, button3)
        text = f'Укажи тип стрижки'
        msg = bot.send_message(message.chat.id, text, reply_markup=kb1)
        bot.register_next_step_handler(msg, finish_current_appont)
    else:
        delete_current(user_id)
        text = 'Запись отменена'
        bot.send_message(message.chat.id, text)
        time.sleep(1)
        starting(message)


def finish_current_appont(message):
    if len(get_my_appoint_with_id_sql(message.from_user.id)) >= 2:
        answer = 'Нельзя осуществлять больше двух записей, сперва удалите одну'
        bot.send_message(message.chat.id, answer)
        starting(message)
    else:
        answer = message.text
        user_id = message.from_user.id
        update_current_appoint_type(user_id, answer)
        text = make_current_appoint(user_id)
        bot.send_message(message.chat.id, text)
        time.sleep(2)
        starting(message)


@bot.message_handler(func=lambda message: message.text == usergrbt6)
def make_apoint_user(message):
    # Вывод прайса
    user_id = message.from_user.id
    text = messegetext.price_text
    bot.send_message(message.chat.id, text)
    time.sleep(2)
    starting(message)

@bot.message_handler(func=lambda message: message.text == usergrbt3)
def make_apoint_user(message):
    if message.chat.id in get_id_from_black_list():
        text = 'Вы в черном списке, обратитесь к администратору'
        bot.reply_to(message, text)
        starting(message)
    else:
        user_id = message.from_user.id
        text = 'Какой день интересует?'
        kb1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2, resize_keyboard=True, )
        button1 = types.KeyboardButton('Сегодня')
        button2 = types.KeyboardButton('Завтра')
        button3 = types.KeyboardButton('Другая дата')
        kb1.add(button1, button2, button3)
        bot.send_message(message.chat.id, text, reply_markup=kb1)


@bot.message_handler(func=lambda message: message.text == 'Сегодня')
def chek_today_user(message):
    if message.chat.id in get_id_from_black_list():
        text = 'Вы в черном списке, обратитесь к администратору'
        bot.reply_to(message, text)
        starting(message)
    else:
        user_id = message.from_user.id
        date1 = date.today()
        day2 = date1.strftime('%d.%m.%Y')
        start_appoint(message, date1, day2)


def check_time_user(message):
    user_id = message.from_user.id
    text = message.text
    answer = time_check(text)
    date1 = get_current_date(user_id)[0]
    if text == 'Выбрать другой день':
        delete_current(user_id)
        make_apoint_user(message)
    else:
        if answer == False:
            if text in cancel:
                delete_current(user_id)
                starting(message)
            else:
                msg = bot.reply_to(message, 'Неверно указано время, попробуй еще раз. Введи время в формате ЧЧ:ММ')
                bot.register_next_step_handler(msg, check_time_user)
        else:
            times = get_app_times(date1)
            answer = f'{answer}:00'
            if answer in times:
                update_current_appoint_time(user_id, answer)
                kb1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2, resize_keyboard=True, )
                button1 = types.KeyboardButton('Стрижка')
                button2 = types.KeyboardButton('Борода')
                button3 = types.KeyboardButton('Комплекс')
                kb1.add(button1, button2, button3)
                text = f'Укажи тип стрижки'
                msg = bot.send_message(message.chat.id, text, reply_markup=kb1)
                bot.register_next_step_handler(msg, finish_current_appont)
            else:
                msg = bot.reply_to(message, 'Указанное время занято или не рабочее')
                bot.register_next_step_handler(msg, check_time_user)

def continue_appoint(message):
    user_id = message.from_user.id
    date1 = get_current_date(user_id)[0]
    day2 = date1
    day2 = datetime.strptime(day2, '%Y-%m-%d')
    day2 = day2.strftime('%d.%m.%Y')
    if date1:
        times = chek_day_appoit_user(user_id, date1)
        text = f'У Вас осталась не законеная запись на {day2}\n'
        for i in times:
            text = text + f'{i}\n'
        text = text + 'Записаться на свободное время, введи его в формате ЧЧ:ММ\nЛибо введи отмена'
        kb1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2, resize_keyboard=True, )
        button1 = types.KeyboardButton('Отмена')
        kb1.add(button1)
        msg = bot.send_message(message.chat.id, text, reply_markup=kb1)
        bot.register_next_step_handler(msg, check_time_user)
    else:
        starting(message)


@bot.message_handler(func=lambda message: message.text == 'Завтра')
def chek_tomorrow_user(message):
    if message.chat.id in get_id_from_black_list():
        text = 'Вы в черном списке, обратитесь к администратору'
        bot.reply_to(message, text)
        starting(message)
    else:
        user_id = message.from_user.id
        date1 = date.today() + timedelta(days=1)
        day2 = date1.strftime('%d.%m.%Y')
        start_appoint(message, date1, day2)


@bot.message_handler(func=lambda message: message.text == 'Другая дата')
# ввод даты после которого последует проверка корректности
def check_day_input_user(message):
    if message.chat.id in get_id_from_black_list():
        text = 'Вы в черном списке, обратитесь к администратору'
        bot.reply_to(message, text)
        starting(message)
    else:
        text = 'Введи дату в формате дд.мм.гггг.'
        msg = bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(msg, check_day_user)

def check_day_user(message):
    text = message.text
    date1 = date_check(text)
    if date1 == False:
        if text in cancel:
            starting(message)
        else:
            bot.reply_to(message, 'Неверный формат даты, попробуй еще раз. Введи дату в формате дд.мм.гггг')
            check_day_input_user(message)
    else:
        day2 = date1.strftime('%d.%m.%Y')
        if date1.date() > date.today():
            start_appoint(message, date1, day2)
        else:
            text = 'Указана дата из прошлого, попробуте другую дату'
            bot.reply_to(message, text)
            check_day_input_user(message)



def start_appoint(message, date1, daytext):
    if len(get_my_appoint_with_id_sql(message.from_user.id)) >= 2:
        answer = 'Нельзя осуществлять больше двух записей, сперва удалите одну'
        bot.send_message(message.chat.id, answer)
        starting(message)
    else:
        user_id = message.from_user.id
        text = message.text
        daytext = daytext
        day2 = date1.strftime('%d.%m.%Y')
        is_work, workday, days = chek_day_appoit_user(user_id, date1)
        workdaystr = workday.strftime('%d.%m.%Y')
        times = get_app_times(workday)
        kb1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2, resize_keyboard=True, )
        button1 = types.KeyboardButton('Выбрать другой день')
        button2 = types.KeyboardButton('Отмена')
        kb1.add(button1, button2)
        if is_work:
            if len(times) == 0:
                text = f'На {daytext} нет свободного времени'
            else:
                text = f'На {daytext} свободно следующее время:\n'
                for i in times:
                    text = text + f'{i}\n'
                text = text + 'Записаться на свободное время, введи его в формате ЧЧ:ММ\nЛибо введи отмена'
        else:
            if len(times) == 0:
                text = f'{day2} выходной, следующий рабочий день {workdaystr} но к сожалению свободного времени на эту дату нет'
            else:
                text = f'{day2} выходной, можно записаться на {workdaystr} свободно следующее время:\n'
                for i in times:
                    text = text + f'{i}\n'
                text = text + 'Записаться на свободное время, введи его в формате ЧЧ:ММ\nЛибо введи отмена'
        msg = bot.send_message(message.chat.id, text, reply_markup=kb1)
        bot.register_next_step_handler(msg, check_time_user)


@bot.message_handler(func=lambda message: message.text == usergrbt4)
def get_apoint_user(message):
    if message.chat.id in get_id_from_black_list():
        text = 'Вы в черном списке, обратитесь к администратору'
        bot.reply_to(message, text)
        starting(message)
    else:
        user_id = message.from_user.id
        appoint = get_my_appoint(user_id)
        if appoint:
            day = datetime.strptime(appoint[0], '%Y-%m-%d').strftime('%d.%m.%Y')
            time1 = appoint[1][0:5]
            text = f'Ближайшая запись на {day} в {time1}'
        else:
            text = 'Нет записей'
        bot.reply_to(message, text)
        time.sleep(2)
        starting(message)


def confirm_deleted(message):
    text = message.text
    user_id = message.from_user.id
    if text == 'Да':
        delete_appoint(user_id)
        bot.send_message(message.chat.id, 'Ваша запись успешно удалена')
        starting(message)
    else:
        starting(message)


@bot.message_handler(func=lambda message: message.text == usergrbt2)
def ask_change_user_data(message):
    if message.chat.id in get_id_from_black_list():
        text = 'Вы в черном списке, обратитесь к администратору'
        bot.reply_to(message, text)
        starting(message)
    else:
        user_id = message.from_user.id
        user = get_user_data(user_id)
        if user:
            telephone = user[0]
            name = user[1]
            text = f'Сейчас вы зарегистрированы под именем\n {name}\n номер телефона:\n {telephone}\nНадо что-то поменять?'
            kb1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2, resize_keyboard=True, )
            button1 = types.KeyboardButton('Да')
            button2 = types.KeyboardButton('Нет')
            kb1.add(button1, button2)
            msg = bot.reply_to(message, text, reply_markup=kb1)
            bot.register_next_step_handler(msg, confirm_userchange)
        else:
            text = 'Вы у нас не зарегистрированы'
            bot.send_message(user_id, text)
            time.sleep(1)
            starting(message)


def confirm_userchange(message):
    text = message.text
    user_id = message.from_user.id
    if text == 'Да':
        msg = bot.send_message(message.chat.id, 'Введи новое имя или номер телефона')
        bot.register_next_step_handler(msg, change_user_data)
    else:
        starting(message)


def change_user_data(message):
    user_id = message.from_user.id
    text = message.text
    user = make_change_user_data(user_id, text)
    telephone = user[0]
    name = user[1]
    text1 = f'Теперь вы зарегистрированы под именем\n {name}\n номер телефона:\n{telephone}'
    bot.send_message(message.chat.id, text1)
    time.sleep(2)
    starting(message)


@bot.message_handler(commands=['admin'])
def admin(message):
    global my_user_id
    if message.from_user.id not in my_user_id:
        adms = set_adms(message.from_user.id, my_user_id)
        my_user_id = adms
        bot.send_message(message.chat.id, 'Вы добавлены в список администраторов')


@bot.message_handler(commands=['user'])
def user(message):
    global my_user_id
    if message.from_user.id in my_user_id:
        adms = remove_adms(message.from_user.id)
        # my_user_id.remove(message.from_user)
        bot.send_message(message.chat.id, 'Вы удалены из администраторов')



@bot.message_handler(func=lambda message: message.text == usergrbt5)
def delete_apoint_user(message):
    user_id = message.from_user.id
    appoints = get_my_appoint_with_id_sql(user_id)
    if len(appoints) > 1:
        kb1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1, resize_keyboard=True, )
        button1 = types.KeyboardButton('Отмена')
        kb1.add(button1)
        text = f'У вас сейчас {len(appoints)} записей'
        count = 1
        for appoint in appoints:
            day = datetime.strptime(appoint[1], '%Y-%m-%d').strftime('%d.%m.%Y')
            time1 = appoint[2][0:5]
            text = f'{text} \n{count} На {day} в {time1}'
            count += 1
        text = text + '\nДля удаления введите порядковый номер записи'
        msg = bot.reply_to(message, text, reply_markup=kb1)
        bot.register_next_step_handler(msg,  choose_deleted, appoints)

    elif len(appoints) == 1:
        appoint = appoints[0]
        text = f'У вас сейчас {len(appoints)} запись'
        day = datetime.strptime(appoint[1], '%Y-%m-%d').strftime('%d.%m.%Y')
        time1 = appoint[2][0:5]
        text = f'{text} \nНа {day} в {time1}\nУдалить запись'
        kb1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2, resize_keyboard=True, )
        button1 = types.KeyboardButton('Да')
        button2 = types.KeyboardButton('Нет')
        kb1.add(button1, button2)
        msg = bot.reply_to(message, text, reply_markup=kb1)
        bot.register_next_step_handler(msg, confirm_deleted)

    else:
        text = 'Нет записей'
        bot.send_message(message.chat.id, text)
        time.sleep(1)
        starting(message)

def choose_deleted(message, appoints):
    user_id = message.from_user.id
    text = message.text
    num = check_number(text, len(appoints))
    if text in cancel:
        starting(message)
    else:
        if num:
            delete_appoint_id(appoints[num-1][0])
            bot.send_message(message.chat.id, 'Запись успешно удалена')
            starting(message)
        else:
            bot.send_message(message.chat.id, 'Некорректно указан номер записи')
            delete_apoint_user(message)


@bot.message_handler(commands=['help'])
def help(message):
    if message.from_user.id in my_user_id:
        text = ('Команда /start служит для входа в главное меню \nКоманда /admin служит для добавления в список админов '
            '\nКоманда /black_list для работы с блэк листом')
    else:
        text = 'Все команды доступны с главного экрана, для перехода к нему нажмите /start, из любого меню можно выйти введя текст "Отмена или "Выход"'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['black_list'])
def black_list_start(message):
    if message.from_user.id in my_user_id:
        text = f'Что хочешь сделать? \nДобавить в черный список\nПосмотреть черный список\nУдалить из черного списка'
        kb1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2, resize_keyboard=True, )
        button1 = types.KeyboardButton('Добавить')
        button3 = types.KeyboardButton('Посмотеть')
        button2 = types.KeyboardButton('Изменить')
        kb1.add(button1, button2, button3)
        msg = bot.reply_to(message, text, reply_markup=kb1)
        bot.register_next_step_handler(msg, black_list_second)


def black_list_second(message):
    text = message.text
    if text in cancel:
        starting(message)
    elif text == 'Добавить':
        kb1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2, resize_keyboard=True, )
        button1 = types.KeyboardButton('Да')
        button2 = types.KeyboardButton('Нет')
        kb1.add(button1, button2)
        text = 'Есть id? Если есть, то сразу вводи'
        msg = bot.reply_to(message, text, reply_markup=kb1)
        bot.register_next_step_handler(msg, add_to_black_list_first)
    elif text == 'Посмотеть':
        text = get_black_list_all()
        bot.send_message(message.chat.id, text)
        black_list_start(message)
    elif text == 'Изменить':
        text = 'Введи id кого хочешь убрать из черного списка'
        msg = bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(msg, delete_from_black_list)
    else:
        text = 'Неверная команда'
        msg = bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(msg, black_list_start)


def delete_from_black_list(message):
    text = message.text
    if text in cancel:
        starting(message)
    else:
        try:
            id = int(text)
            remove_from_black_list(id)
            text = 'Сделаноб этого id больше нет в Черном списке'
            bot.send_message(message.chat.id, text)
            starting(message)
        except Exception:
            text = 'Неверный номер id'
            msg = bot.send_message(message.chat.id, text)
            bot.register_next_step_handler(msg, delete_from_black_list)


def add_to_black_list_first(message):
    text = message.text
    if text in cancel:
        print('HOW!!!')
        starting(message)
    else:
        if text.isdigit():
            if add_to_black_list(int(text)):
                answer = f'Пользователь c id: {text} успешно добавлен в черный список'
                bot.send_message(message.chat.id, answer)
                black_list_start(message)
            else:
                answer = f'Пользователь с id: {text} не значится в нашей базе'
                bot.send_message(message.chat.id, answer)
        elif text == 'Да':
            answer = f'Введи id'
            msg = bot.send_message(message.chat.id, answer)
            bot.register_next_step_handler(msg, add_to_black_list_first)
        else:
            text = f'Как будем искать id'
            kb1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2, resize_keyboard=True, )
            button1 = types.KeyboardButton('По номеру телефона')
            button3 = types.KeyboardButton('По имени')
            button2 = types.KeyboardButton('По записи')
            kb1.add(button1, button2, button3)
            msg = bot.reply_to(message, text, reply_markup=kb1)
            bot.register_next_step_handler(msg, add_to_black_list_second)


def add_to_black_list_second(message):
    text = message.text
    if text in cancel:
        starting(message)
    else:
        if text.isdigit():
            add_to_black_list_first(message)
        elif text == 'По номеру телефона':
            answer = 'Введи номер телефона'
            msg = bot.reply_to(message, answer)
            bot.register_next_step_handler(msg, user_search_by_telephon)
        elif text == 'По имени':
            answer = 'Введи имя'
            msg = bot.reply_to(message, answer)
            bot.register_next_step_handler(msg, user_search_by_name)
        elif text == 'По записи':
            answer = 'Введи дату'
            msg = bot.reply_to(message, answer)
            bot.register_next_step_handler(msg, user_search_by_appoint_second)


def user_search_by_telephon(message):
    text = message.text
    if text in cancel:
        black_list_start(message)
    else:
        answertext = search_by_telephon(text)
        if answertext:
            bot.reply_to(message, answertext)
            black_list_start(message)
        else:
            answer = 'Неверный номер телефона, введи другой'
            msg = bot.reply_to(message, answertext)
            bot.register_next_step_handler(msg, user_search_by_telephon)


def user_search_by_name(message):
    text = message.text
    if text in cancel:
        black_list_start(message)
    else:
        answertext = search_by_name(text)
        if answertext:
            bot.reply_to(message, answertext)
            black_list_start(message)
        else:
            answer = 'Нет пользователей с таким именем'
            msg = bot.reply_to(message, answer)
            bot.register_next_step_handler(msg, user_search_by_telephon)


def user_search_by_appoint(message):
    text = message.text
    if text in cancel:
        black_list_start(message)
    else:
        answer = 'Введи дату за которую хочешь посмотреть клиентов'
        msg = bot.reply_to(message, answer)
        bot.register_next_step_handler(msg, user_search_by_appoint_second)



def user_search_by_appoint_second(message):
    text = message.text
    if text in cancel:
        black_list_start(message)
    else:
        answer = search_by_appoint(text)
        if answer:
            bot.reply_to(message, answer)
            black_list_start(message)
        else:
            answer = 'Неверный формат датыб либо в эту дату ни кто не записался'
            bot.reply_to(message, answer)
            user_search_by_appoint(message)


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    global my_user_id
    if message.from_user.id in my_user_id:
        text = 'Неверная команда попробуйте еще раз или введите команду /start \n/user\n/help'
    else:
        text = 'Неверная команда попробуйте еще раз или введите команду /start \n/admin\n/help'

    bot.reply_to(message, text)



def todayapoits_auto():
    usrer = my_user_id[0]
    text = chek_todayadmcmd()
    bot.send_message(usrer, text)


def my_schedule1():
    schedule.every().day.at('07:00').do(todayapoits_auto)
    schedule.every().day.at('07:00').do(clear_current)
    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            print(e)


def my_bot():
    while True:
        try:
            bot.polling()
            print('Hi there')
        except Exception as e:
            print(e)


def main():
    th1 = threading.Thread(target=my_bot)
    th2 = threading.Thread(target=my_schedule1)
    th1.start()
    th2.start()

if __name__ == "__main__":
    main()


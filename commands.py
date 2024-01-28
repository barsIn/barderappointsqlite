import re
from datetime import date, time, datetime, timedelta
import random
from sqlcommands import (get_next_appoint, get_date_appoint, remuve_weekday, add_weekday, get_weekendssql, get_holydays_sql,
                         add_holyday_sql, dalete_holyday_sql, get_worktime_sql, set_worktime, update_worktime, add_user,
                         update_user_sql, create_current_appoint, add_appoint, get_current_appoint, delete_current,
                         get_my_appoint_sql, get_user_data_sql, chenge_user_data_sql, chenge_user_telephone_sql,
                         delete_erliiest)

weekdays = {
    'Mon': 'Понедельник',
    'Tue': 'Вторник',
    'Wed': 'Среда',
    'Thu': 'Четверг',
    'Fri': 'Пятница',
    'Sat': 'Суббота',
    'Sun': 'Воскресение'
}
engweekdays = {
    'Понедельник': 'Mon',
    'Вторник': 'Tue',
    'Среда': 'Wed',
    'Четверг': 'Thu',
    'Пятница': 'Fri',
    'Суббота': 'Sat',
    'Воскресение': 'Sun'
}
months = {
    'January': 'Января',
    'February': 'Вевраля',
    'March': 'Марта',
    'April': 'Апреля',
    'May': 'Мая',
    'June': 'Июня',
    'July': 'Июля',
    'August': 'Августа',
    'September': 'Сентября',
    'October': 'Октября',
    'November': 'Ноября',
    'December': 'Декабря'
}


def date_check(datestr):
    try:
        thisday = datetime.strptime(datestr, '%d.%m.%Y')
        return thisday
    except:
        # days = datestr.split('/', '.', ',',':',';',' ')
        days = re.split("[.,:;]", datestr)
        print(f'days {days}')
        print(len(days))
        if len(days) == 2:
            try:
                thisday = int(days[0])
                thismonth = int(days[1])
                thisyear = datetime.today().year
                thisdate = datetime(thisyear, thismonth, thisday)
                print(thisdate)
                return thisdate
            except:
                return False
        elif len(days) == 3:
            try:
                thisday = int(days[0])
                thismonth = int(days[1])
                thisyear = int(days[2])
                thisdate = datetime(thisyear, thismonth, thisday)
                return thisdate
            except:
                return False
        else:
            return False


def chek_next_appoint_adm():
    delete_erliiest()
    appoint = get_next_appoint()
    if appoint:
        date1 = datetime.strptime(appoint[0], '%Y-%m-%d')
        time1 = datetime.strptime(appoint[1], '%H:%M:%S')
        strtime = time1.strftime('%H:%M')
        strdate = date1.strftime('%d')
        weekday = date1.strftime('%a')
        month = date1.strftime('%B')
        ruweekday = weekdays[weekday]
        rumonth = months[month]
        name = appoint[2]
        telephone = appoint[3]
        text = f'Следующая запись {ruweekday} {strdate} {rumonth} в {strtime}, Должен придти {name}, телефон для связи {telephone}'

    else:
        text = "Записей нет"
    return text


def check_appoint_adm(datestr):
    delete_erliiest()
    result = get_date_appoint(datestr)
    # Должен выдать список [Время, имя, телефон либо None
    return result


def chek_todayadmcmd():
    date1 = date.today()
    delete_erliiest()
    appoints = check_appoint_adm(date1.strftime('%Y-%m-%d'))
    if appoints == None:
        return 'Нет записей на сегодня'
    else:
        count = len(appoints)
        weekday = weekdays[date1.strftime('%a')]
        day = date1.strftime('%d.%m')
        text = f'На сегодня {weekday} {day} есть {count} записей\n'
        for ap in appoints:
            text2 = f'{ap[0]} должен придти в {ap[1]}, телефон для связи {ap[2]}\n'
            text = text + text2
        return text


def chek_tomorrowadmcmd():
    date1 = date.today() + timedelta(days=1)
    appoints = check_appoint_adm(date1.strftime('%Y-%m-%d'))
    if appoints == None:
        return 'Нет записей на завтра'
    else:
        count = len(appoints)
        weekday = weekdays[date1.strftime('%a')]
        day = date1.strftime('%d.%m')
        text = f'На завтра {weekday} {day} есть {count} записей\n'
        for ap in appoints:
            text2 = f'{ap[0]} должен придти {ap[1]}, телефон для связи {ap[2]}\n'
            text = text + text2
        return text


def chek_alldaymcmd(date1):
    appoints = check_appoint_adm(date1.strftime('%Y-%m-%d'))
    if appoints == None:
        date1 = date1.strftime('%d.%m.%Y')
        return f'Нет записей на {date1}'
    else:
        count = len(appoints)
        weekday = weekdays[date1.strftime('%a')]
        day = date1.strftime('%d.%m')
        text = f'На {weekday} {day} есть {count} записей\n'
        for ap in appoints:
            text2 = f'{ap[0]} должен придти {ap[1]}, телефон для связи {ap[2]}\n'
            text = text + text2
        return text


# Получим текущие нерабочие дни
def get_weekends():
    weekend = get_weekendssql()
    if weekend == None:
        return None
    else:
        return weekend


# Должен выдать список выходных дней формата %a или None


# Возвращаем текст текущих выходных
def get_weekends_adm():
    weekends = get_weekends()
    if weekends == None:
        text = 'Сейчас выходных дней не установлено'
    else:
        text = 'Текущие выходные дни: '
        for day in weekends:
            text1 = f'{weekdays[day]} '
            text = text + text1
    return text


def weekdate_check(day):
    if day in weekdays.values():
        mach = make_weekday(day)
        return f'День успешно {mach}'
    else:
        return False


# Добавляет день к выходным
def make_weekday(day):
    weekends = get_weekends()
    enday = engweekdays[day]
    if enday in weekends:
        result = remuve_weekday(enday)
        return 'Удален'
    else:
        result = add_weekday(enday)
        return 'Добавлен'

def get_holydays():
    holydays = get_holydays_sql()
    return holydays
    #     Возвращает список выходных дней


def get_holydays_adm():
    holydays = get_holydays()
    if holydays:
        text = 'Сейчас установлены выходные дни: '
        for hol in holydays:
            hol1 = datetime.strptime(hol, '%Y-%m-%d').strftime('%d.%m.%Y')
            text = f'{text} \n{hol1}'
    else:
        text = 'Сейчас выходных не установлено'
    return text


def holyday_check(day):
    day = date_check(day)
    if day:
        day2 = day.strftime('%Y-%m-%d')
        if day2:
            holydays = get_holydays()
            if day2 in holydays:
                delete_holyday(day2)
                return 'День успешно удален'
            else:
                add_holyday(day2)
                return 'День успешно добавлен'
    else:
        return False


def add_holyday(day):
        add_holyday_sql(day)


def delete_holyday(day):
        dalete_holyday_sql(day)


def get_worktime_adm():
    worktime = get_worktime_sql()
    if worktime:
        text = f'Установлено рабочее время с {worktime[0]} до {worktime[1]}'
    else:
        text = 'Рабочее время еще не установлено'
    return text


def time_check(t):
    try:
        t1 = datetime.strptime(t, '%H:%M')
        return t1.strftime('%H:%M')
    except:
        if len(t) != 5:
            return False
        else:
            try:
                time1 = time(int(t[0:2]), int(t[3:]))
                return time1.strftime('%H:%M')
            except:
                return False



def worktime_check(text):
    t1 = time_check(text[0:5])
    t2 = time_check(text[6:])
    if t1 and t2:
        make_worktime(t1, t2)
        text = f'Рабочее время установлено с {t1} до {t2}'
        return text
    else:
        return False
        # text = 'Проблема с форматом времени, попробуйте еще раз. \nКак пример 09:00 19:00.'


def make_worktime(t1, t2):
    if get_worktime_sql():
        update_worktime(t1, t2)
    else:
        set_worktime(t1, t2)


# Создаем юзера от админа
def create_user_byadm(name, telephone):
    id = random.randint(1000000000, 9999999999)
    add_user(id, telephone, name)
    return id
# Дальше пошли команды для юзера
def create_user(user_id, telephone, user_name=None):
    add_user(user_id, telephone, user_name)


def update_user(user_id, user_name):
        update_user_sql(user_id, user_name)


def get_next_workday(now):
    if now == date.today() and datetime.now().strftime('%H:%M:%S') > get_worktime_sql()[1]:
        now = now + timedelta(days=1)
    if (now.strftime('%a') in get_weekendssql()) or (now.strftime('%Y-%m-%d') in get_holydays_sql()):
        while True:
            now = now + timedelta(days=1)
            if (now.strftime('%a') not in get_weekendssql()) and (now.strftime('%Y-%m-%d') not in get_holydays_sql()):
                break
    return now

# Возвращает список занятого времени на конкретную дату
def get_busy_times(appoints):
    times = []
    for apoint in appoints:
        times.append(datetime.strptime(apoint[0], '%H:%M:%S').strftime('%H:%M:%S'))
    return times


def get_free_times(appoints):
    starttime = int(get_worktime_sql()[0][0:2])
    endtime = int(get_worktime_sql()[1][0:2])
    if appoints:
        busytime = get_busy_times(appoints)
    else:
        busytime = []
    freetimes = []
    for i in range(starttime, endtime):
        ftime = time(i, 0, 0)
        freetimes.append(ftime.strftime('%H:%M:%S'))
    for i in busytime:
        if i in freetimes:
            freetimes.remove(i)
    return freetimes




def get_next_apoint(user_id):
    now = date.today()
    workday = get_next_workday(now)
    appoints = get_date_appoint(workday.strftime('%Y-%m-%d'))
    nowtime = datetime.strptime(datetime.now().strftime('%H:%M:%S'), '%H:%M:%S')
    aptime = nowtime
    starttime = get_worktime_sql()[0]
    endtime = get_worktime_sql()[1]
    if not appoints and now != workday:
        aptime = starttime
    elif not appoints and now == workday:
        if nowtime < datetime.strptime(starttime, '%H:%M:%S'):
            aptime = starttime
        else:
            nowhour = int(nowtime.strftime('%H'))
            aptime = f'{nowhour+1}:00:00'
    else:
        aptime1 = get_free_times(appoints)
        if now != workday:
            aptime = aptime1[0]
        else:
            nowtime = datetime.now().hour
            for t in aptime1:
                if int(t[0:2]) > nowtime:
                    aptime = t
                    break
    return [workday, aptime]



def make_current_appoint(user_id):
    current = get_current_appoint(user_id)
    add_appoint(current)
    delete_current(user_id)
    start_date = datetime.strptime(current[1],'%Y-%m-%d').strftime('%d.%m.%Y')
    start_time = datetime.strptime(current[2],'%H:%M:%S').strftime('%H:%M')
    text = f'Запись успешно осуществлена на {start_date} в {start_time}'
    return text

# проверка, рабочий ли сегодня день

def anyday_is_work_day(user_id, date1):
    now = date1
    workday = get_next_workday(now)
    if now == workday:
        create_current_appoint(user_id, workday.strftime('%Y-%m-%d'))
        return True, workday
    else:
        create_current_appoint(user_id, workday.strftime('%Y-%m-%d'))
        return False, workday

def chek_day_appoit_user(user_id, day1):
    is_work, workday = anyday_is_work_day(user_id, day1)
    appoints = get_date_appoint(workday)
    aptime = get_free_times(appoints)
    if day1 == date.today():
        aptime2 = []
        hour = int(datetime.now().strftime('%H'))
        for i in aptime:
            if int(i[0:2]) > hour:
                aptime2.append(i)
        aptime = aptime2
    return is_work, workday, aptime


def get_app_times(day1):
    appoints = get_date_appoint(day1)
    aptime = get_free_times(appoints)
    return aptime


def get_my_appoint(user_id):
    app = get_my_appoint_sql(user_id)
    if app:
        return app[0], app[1]
    else:
        return False


def get_user_data(user_id):
    user = get_user_data_sql(user_id)
    if user:
        telephone = user[1]
        name = user[2]
        return [telephone, name]
    else:
        return False


def make_change_user_data(user_id, text):
    text2 = text.split(' ')
    if len(text2) == 2:
        chenge_user_data_sql(user_id, text2[0], text2[1])
    else:
        try:
            int(text[1:4])
            chenge_user_telephone_sql(user_id, text)
        except:
            update_user_sql(user_id, text)
    return get_user_data(user_id)

def check_number(number, max):
    try:
        intnumber = int(number)
        if intnumber < 1 or intnumber > max:
            return False
        else:
            return intnumber
    except:
        return False



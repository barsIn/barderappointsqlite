import datetime
import sqlite3 as sq
import datetime as dt
from datetime import timedelta

# from main import my_user_id

db_name = 'main_barber.db'
weekdays = {
    'Mon': 1,
    'Tue': 2,
    'Wed': 3,
    'Thu': 4,
    'Fri': 5,
    'Sat': 6,
    'Sun': 7
}
def create_appoints():
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS appoints (
            appoint_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            finish_time TEXT NOT NULL,
            barber_type TEXT
        )""")


def create_current_appoints():
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS current_appoints (
            appoint_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT,
            start_time TEXT,
            finish_time TEXT,
            barber_type TEXT
        )""")


def create_holydays():
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS holydays (
            holyday TEXT NOT NULL UNIQUE
        )""")


def create_worktime():
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS worktime (
            wid INTEGER DEFAULT 1,
            start TEXT NOT NULL UNIQUE,
            end TEXT NOT NULL UNIQUE
        )""")


def create_weekdays():
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS weekdays (
            number INTEGER NOT NULL UNIQUE,
            weekday TEXT NOT NULL UNIQUE
        )""")
def create_users():
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            telephone TEXT NOT NULL DEFAULT 'Heve not telephone',
            user_name TEXT
        )""")
def get_next_appoint():
    create_appoints()
    create_users()
    date1 = dt.date.today().strftime('%Y-%m-%d')
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute(f"""SELECT date, start_time, user_name, telephone FROM appoints
                            JOIN users ON appoints.user_id=users.user_id
                            WHERE appoints.date >= date('{date1}') ORDER BY appoints.date, start_time""")
        result = cur.fetchone()
    if len(result) > 0:
        return result
    else:
        return False


def get_date_appoint(strdate):
    create_appoints()
    create_users()
    delete_erliiest()
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute(f"""SELECT start_time, user_name, telephone FROM appoints 
                            JOIN users ON appoints.user_id=users.user_id 
                            WHERE appoints.date = date('{strdate}') ORDER BY appoints.date, start_time""")
        result = cur.fetchall()
    if len(result) > 0:
        return result
    else:
        return None


def get_weekendssql():
    create_weekdays()
    weekdays = []
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute("""SELECT * FROM weekdays
                        ORDER BY number""")
        result = cur.fetchall()
    if result:
        for day in result:
            weekdays.append(day[1])
        return weekdays
    else:
        return None
def remuve_weekday(day):
    with sq.connect(db_name) as con:
        cur = con.cursor()
        try:
            cur.execute(f"DELETE FROM weekdays WHERE weekday =='{day}'")
            return True
        except:
            return False

def add_weekday(day):
    with sq.connect(db_name) as con:
        cur = con.cursor()
        try:
            cur.execute(f"INSERT INTO weekdays VALUES({weekdays[day]},'{day}')")

            return True
        except:
            return False

def delet_erlist():
    day1 = dt.date.today().strftime('%Y-%m-%d')
    with sq.connect(db_name) as con:
        cur = con.cursor()
        try:
            cur.execute(f"""DELETE FROM holydays WHERE holyday < date('{day1}')""")
            return True
        except Exception as e:
            print(e)
            return False

def get_holydays_sql():
    create_holydays()
    delet_erlist()
    holydays = []
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute("""SELECT * FROM holydays
                        ORDER BY holyday""")
        result = cur.fetchall()
    if result:
        for res in result:
            holydays.append(res[0])
        return holydays
    else:
        return False


def add_holyday_sql(day):
    with sq.connect(db_name) as con:
        cur = con.cursor()
        try:
            cur.execute(f"INSERT INTO holydays VALUES(date('{day}'))")

            return True
        except Exception as e:
            print(e)
            return False


def dalete_holyday_sql(day):
    with sq.connect(db_name) as con:
        cur = con.cursor()
        try:
            cur.execute(f"DELETE FROM holydays WHERE holyday == date('{day}')")
            return True
        except Exception as e:
            print(e)
            return False


def get_worktime_sql():
    create_worktime()
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute("""SELECT start, end FROM worktime""")
        result = cur.fetchone()
    if result:
        return [result[0], result[1]]
    else:
        return False


def set_worktime(t1, t2):
    with sq.connect(db_name) as con:
        cur = con.cursor()
        try:
            cur.execute(f"""INSERT INTO worktime VALUES(1, time('{t1}'), time('{t2}'))""")
            result = cur.fetchone()
            return result
        except:
            pass

def update_worktime(t1, t2):
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute(f"""UPDATE worktime SET start = time('{t1}'), end = time('{t2}') WHERE wid ==1""")
        result = cur.fetchone()
        return result


# Дальше идут команды для взаимодействия с Юзером
def get_usersid_sql():
    create_users()
    id = []
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute("""SELECT user_id FROM users""")
        result = cur.fetchall()
    if result:
        for i in result:
            id.append(i[0])
    return id

def add_user(user_id, telephone, user_name):
    create_users()
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute(f"""INSERT INTO users VALUES('{user_id}', '{telephone}', '{user_name}')""")


def create_current_appoint(user_id, date, start_time=None, finish_time=None, barber_type=None):
    create_current_appoints()
    if start_time:
        finish_time = f'{start_time[0:2]}:59:00'
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute(f"""INSERT INTO current_appoints (user_id, date, start_time, finish_time, barber_type) 
                        VALUES('{user_id}', date('{date}'), time('{start_time}'), time('{finish_time}'), '{barber_type}')""")


def update_current_appoint_type(user_id, type):
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute(f"""UPDATE current_appoints SET barber_type = '{type}' WHERE user_id == {user_id}""")


def update_current_appoint_time(user_id, time1):
    create_current_appoints()
    stat_time = datetime.datetime.strptime(time1, '%H:%M:%S')
    finish_time = stat_time + datetime.timedelta(minutes=59)
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute(f"""UPDATE current_appoints SET start_time = time('{stat_time}'), finish_time =  time('{finish_time}')
                        WHERE user_id == {user_id}""")

# create_current_appoint(3, '2024-01-20')
# update_current_appoint_time(3, '12:00')
        # cur.execute(f"DELETE FROM holydays WHERE holyday == date('{day}')")

        # cur.execute(f"""INSERT INTO current_appoints (user_id, date, start_time, finish_time, barber_type)
        #                 VALUES('{user_id}', date('{date}'), time('{start_time}'), time('{finish_time}'), '{barber_type}')""")
# create_current_appoint(1, '2024-01-16', '11:00:00', 'Борода')
# add_user(1, '923', 'Igor')
# add_user(2, '963', 'test')
# add_user(3, '915', 'Pasha')

def get_current_appoint(user_id):
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute(f"""SELECT user_id, date, start_time, finish_time, barber_type 
                        FROM current_appoints WHERE user_id == {user_id}""")
    result = cur.fetchone()
    return result


def delete_current(user_id):
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute(f"DELETE FROM current_appoints WHERE user_id == {user_id}")

def update_user_sql(user_id, user_name):
    create_users()
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute(f"""UPDATE users SET user_name = '{user_name}' WHERE user_id == '{user_id}'""")


def add_appoint(appoint):
    create_appoints()
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute(f"""INSERT INTO appoints (user_id, date, start_time, finish_time, barber_type) 
                        VALUES('{appoint[0]}', date('{appoint[1]}'), time('{appoint[2]}'), time('{appoint[3]}'), '{appoint[4]}')""")

# add_appoint([2,'2024-01-22', '10:00:00', '10:59:00', 'boroda'])
def get_current_date(user_id):
    create_appoints()
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute(f"""SELECT date FROM current_appoints WHERE user_id == {user_id}""")
        result = cur.fetchone()
    return result


def get_some():
    with sq.connect(db_name) as con:
        cur = con.cursor()
        date1 = dt.date.today().strftime('%Y-%m-%d')
        cur.execute(f"""SELECT date, start_time, user_name, telephone FROM appoints 
                    JOIN users ON appoints.user_id=users.user_id 
                    WHERE appoints.date >= date('{date1}') ORDER BY appoints.date, start_time""")
        result = cur.fetchall()
        return result


def create_adms():
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS adms (
            id INTEGER NOT NULL UNIQUE
        )""")


def get_adms():
    create_adms()
    res1 = []
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute("""SELECT * FROM adms""")
        result = cur.fetchall()
        for res in result:
            res1.append(res[0])
        return res1


def get_my_appoint_sql(user_id):
    create_appoints()
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute(f"""SELECT date, start_time FROM appoints WHERE user_id == {user_id}""")
        result = cur.fetchone()
        return result


def get_my_appoint_with_id_sql(user_id):
    create_appoints()
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute(f"""SELECT appoint_id, date, start_time FROM appoints WHERE user_id == {user_id}""")
        result = cur.fetchall()
        return result


def delete_appoint(user_id):
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute(f"DELETE FROM appoints WHERE user_id == {user_id}")


def delete_appoint_id(appoint_id):
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute(f"DELETE FROM appoints WHERE appoint_id == '{appoint_id}'")

def get_user_data_sql(user_id):
    create_users()
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute(f"""SELECT * FROM users WHERE user_id == {user_id}""")
        result = cur.fetchone()
        return result


def chenge_user_data_sql(user_id, name, telephon):
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute(f"""UPDATE users SET user_name = '{name}', telephone = '{telephon}' WHERE user_id == '{user_id}'""")


def chenge_user_telephone_sql(user_id, telephon):
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute(f"""UPDATE users SET telephone = '{telephon}' WHERE user_id == '{user_id}'""")


def delete_erliiest():
    now = dt.datetime.now()
    with sq.connect(db_name) as con:
        cur = con.cursor()
        date1 = dt.date.today().strftime('%Y-%m-%d')
        cur.execute(f"""DELETE FROM appoints 
                    WHERE appoints.date <= date('{now}')""")
        result = cur.fetchall()
        return result




def set_adms(id, my_user_id):
    create_adms()
    with sq.connect(db_name) as con:
        cur = con.cursor()
        try:
            cur.execute(f"""INSERT INTO adms VALUES({id})""")
            my_user_id.append(id)
            return my_user_id
        except Exception as e:
            print(e)

def remove_adms(user_id):
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute(f"DELETE FROM adms WHERE id == {user_id}")


def deletesometh():
    with sq.connect(db_name) as con:
        cur = con.cursor()
        # cur.execute("DROP TABLE weekdays")
        # cur.execute("DROP TABLE holydays")
        # cur.execute("DROP TABLE worktime")
        # cur.execute("DROP TABLE adms")
        cur.execute("DROP TABLE users")
        cur.execute("DROP TABLE appoints")
        cur.execute("DROP TABLE current_appoints")

# deletesometh()

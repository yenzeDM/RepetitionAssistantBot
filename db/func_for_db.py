import sqlite3 as sq
import datetime
from additional_func import check_text_to_repeat
from datetime import date


base = sq.connect('bot.db', check_same_thread=False)
cur = base.cursor()


# bot.py
def db_start():
    base.execute(
        'CREATE TABLE IF NOT EXISTS users(user_tg_id INTEGER PRIMARY KEY, last_activity TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS material(user_tg_id INTEGER, text_to_repeat TEXT, help_text TEXT, date_of_addition TEXT, days_before_repetition INTEGER, FOREIGN KEY (user_tg_id) REFERENCES users (user_tg_id))')
    base.commit()


# bot.py
async def get_users_activity():
    list = cur.execute(
        'SELECT user_tg_id, last_activity from users').fetchall()
    return list


# bot.py
async def delete_all_user_data(user_id):
    cur.execute('DELETE FROM material WHERE user_tg_id == ?', (user_id,))
    cur.execute('DELETE FROM users WHERE user_tg_id == ?', (user_id,))
    base.commit()


# bot.py
async def get_users_id():
    list = cur.execute('SELECT user_tg_id from users').fetchall()
    return list


# add.py
async def add_data(data):
    cur.execute('INSERT INTO material VALUES (?, ?, ?, ?, ?)',
                (data['user_tg_id'], data['text_to_repeat'], data['help_text'], data['date_of_addition'], data['days_before_repetition'],))
    base.commit()


# delete.py
async def delete_one(message):
    cur.execute('DELETE FROM material WHERE text_to_repeat == ? and user_tg_id == ?',
                (message.text.lower(), message.from_user.id,))
    base.commit()


# delete.py
async def delete_several(list, message):
    while list:
        cur.execute('DELETE FROM material WHERE text_to_repeat == ? and user_tg_id == ?',
                    (list[0], message.from_user.id,))
        list = list[1::]
    base.commit()


# delete.py
async def delete_all(id):
    cur.execute('DELETE FROM material WHERE user_tg_id == ?', (id,))
    base.commit()


# change_days.py, delete.py, other.py
async def show_all_added_material(message):
    list = cur.execute('SELECT text_to_repeat, help_text, date_of_addition, days_before_repetition FROM material WHERE user_tg_id == ?',
                       (message.from_user.id,)).fetchall()
    return list


# learn.py bot.py
async def show_finished_text_to_repeat(id):
    list = cur.execute('SELECT text_to_repeat, help_text, date_of_addition, days_before_repetition FROM material WHERE user_tg_id == ?',
                       (id,)).fetchall()
    result = await check_text_to_repeat(list)
    return result


# learn.py
async def change_date(data, message):
    cur.execute('UPDATE material SET date_of_addition == ? WHERE text_to_repeat == ? and user_tg_id == ?',
                (str(datetime.date.today()), data[0], message.from_user.id,))
    base.commit()


# add.py, cancel.py, changed_days.py, delete.py, learn.py, other.py
async def update_last_activity(message):
    cur.execute('UPDATE users SET last_activity == ? WHERE user_tg_id == ?',
                (str(datetime.date.today()), message.from_user.id,))
    base.commit()


# change_days.py
async def change_days_before_repetition(data, message):
    list = [help_text[0] for help_text in cur.execute(
        'SELECT help_text FROM material WHERE user_tg_id == ?', (message.from_user.id,)).fetchall()]
    if data['help_text'] in list:
        cur.execute('UPDATE material SET days_before_repetition = ? WHERE help_text = ?',
                    (data['days_before_repetition'], data['help_text'],))
        base.commit()
    else:
        raise ValueError


# other.py
async def add_user_id(message):
    cur.execute(
        'INSERT INTO users VALUES(?, ?)', (message.from_user.id, str(date.today()),))
    base.commit()

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
    tmp = cur.execute(
        'SELECT user_tg_id, last_activity from users').fetchall()
    return tmp


# bot.py
async def delete_all_user_data(user_id):
    cur.execute('DELETE FROM material WHERE user_tg_id == ?', (user_id,))
    cur.execute('DELETE FROM users WHERE user_tg_id == ?', (user_id,))
    base.commit()


# bot.py
async def get_users_id():
    tmp = cur.execute('SELECT user_tg_id from users').fetchall()
    return tmp


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
async def delete_several(text_to_repeat, message):
    cur.execute('DELETE FROM material WHERE text_to_repeat == ? and user_tg_id == ?',
                (text_to_repeat, message.from_user.id,))
    base.commit()


# delete.py
async def delete_all(id):
    cur.execute('DELETE FROM material WHERE user_tg_id == ?', (id,))
    base.commit()


# learn.py
async def change_date(data, message):
    cur.execute('UPDATE material SET date_of_addition == ? WHERE text_to_repeat == ? and user_tg_id == ?',
                (str(datetime.date.today()), data[0], message.from_user.id,))
    base.commit()


# change_days.py, delete.py, other.py
async def show_all_added_material(message):
    tmp = cur.execute('SELECT text_to_repeat, help_text, date_of_addition, days_before_repetition FROM material WHERE user_tg_id == ?',
                      (message.from_user.id,)).fetchall()
    return tmp


# learn.py bot.py
async def show_finished_text_to_repeat(id):
    tmp = cur.execute('SELECT text_to_repeat, help_text, date_of_addition, days_before_repetition FROM material WHERE user_tg_id == ?',
                      (id,)).fetchall()
    result = await check_text_to_repeat(tmp)
    return result


# add.py, cancel.py, changed_days.py, delete.py, learn.py, other.py
async def update_last_activity(message):
    cur.execute('UPDATE users SET last_activity == ? WHERE user_tg_id == ?',
                (str(datetime.date.today()), message.from_user.id,))
    base.commit()


# change_days.py delete.py
async def get_text_to_repeat(message):
    tmp = cur.execute(
        'SELECT text_to_repeat FROM material WHERE user_tg_id == ?', (message.from_user.id,))
    return tmp


# change_days.py
async def change_one(data, message):
    tmp = [text_to_repeat[0] for text_to_repeat in cur.execute(
        'SELECT text_to_repeat FROM material WHERE user_tg_id == ?', (message.from_user.id,)).fetchall()]
    if data['text_to_repeat'] in tmp:
        cur.execute('UPDATE material SET days_before_repetition == ? WHERE text_to_repeat == ? and user_tg_id == ?',
                    (data['new_days'], data['text_to_repeat'], message.from_user.id,))
        base.commit()
    else:
        raise ValueError('Invalid text to change')


# change_days.py
async def change_by_days(data, message):
    cur.execute('UPDATE material SET days_before_repetition == ? WHERE days_before_repetition == ? and user_tg_id == ?',
                (data['new_days'], data['old_days'], message.from_user.id,))
    base.commit()


# change_days.py
async def change_several(new_days, text_to_repeat, message):
    cur.execute(
        'UPDATE material SET days_before_repetition == ? WHERE text_to_repeat == ? and user_tg_id ==?', (new_days, text_to_repeat, message.from_user.id,))
    base.commit()


# change_days.py
async def get_days_before_repetition(message):
    tmp = cur.execute(
        'SELECT days_before_repetition FROM material where user_tg_id ==?', (message.from_user.id,))
    return tmp


# other.py
async def add_user_id(message):
    cur.execute(
        'INSERT INTO users VALUES(?, ?)', (message.from_user.id, str(date.today()),))
    base.commit()

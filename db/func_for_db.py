import sqlite3 as sq
import datetime
from additional_func import check_text_to_repeat
from datetime import date


# bot.py
def db_start():
    global base, cur
    base = sq.connect('bot.db')
    base.execute(
        'CREATE TABLE IF NOT EXISTS users(user_tg_id INTEGER PRIMARY KEY, last_activity TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS phrases(user_tg_id INTEGER, phrase TEXT, translation TEXT, date_of_addition TEXT, days_before_repetition INTEGER, FOREIGN KEY (user_tg_id) REFERENCES users (user_tg_id))')
    base.commit()
    cur = base.cursor()


# bot.py
def db_finish():
    base.close()


# add.py
async def add_data(data):
    cur.execute('INSERT INTO phrases VALUES (?, ?, ?, ?, ?)',
                (data['user_tg_id'], data['phrase'], data['translation'], data['date_of_addition'], data['days_before_repetition'],))
    base.commit()


# delete.py
async def delete_one(message):
    cur.execute('DELETE FROM phrases WHERE phrase == ? and user_tg_id == ?',
                (message.text.lower(), message.from_user.id,))
    base.commit()


# delete.py
async def delete_several(list, message):
    while list:
        cur.execute('DELETE FROM phrases WHERE phrase == ? and user_tg_id == ?',
                    (list[0], message.from_user.id,))
        list = list[1::]
    base.commit()


# delete.py
async def delete_all_data_from_phrases(id):
    cur.execute('DELETE FROM phrases WHERE user_tg_id == ?', (id,))
    base.commit()


# changed_days.py, delete.py, other.py
async def show_list_of_phrases(message):
    list = cur.execute('SELECT phrase, translation, date_of_addition, days_before_repetition FROM phrases WHERE user_tg_id == ?',
                       (message.from_user.id,)).fetchall()
    return list


# learn.py bot.py
async def show_phrase_for_learn(id):
    list = cur.execute('SELECT phrase, translation, date_of_addition, days_before_repetition FROM phrases WHERE user_tg_id == ?',
                       (id,)).fetchall()
    result = await check_text_to_repeat(list)
    return result


# learn.py
async def change_date_for_phrase(data, message):
    cur.execute('UPDATE phrases SET date_of_addition == ? WHERE phrase == ? and user_tg_id == ?',
                (str(datetime.date.today()), data[0], message.from_user.id,))
    base.commit()


# add.py, cancel.py, changed_days.py, delete.py, learn.py, other.py
async def update_last_activity(message):
    cur.execute('UPDATE users SET last_activity == ? WHERE user_tg_id == ?',
                (str(datetime.date.today()), message.from_user.id,))
    base.commit()


# bot.py
async def get_users_activity():
    list = cur.execute(
        'SELECT user_tg_id, last_activity from users').fetchall()
    return list


# bot.py
async def delete_all_user_data(user_id):
    cur.execute('DELETE FROM phrases WHERE user_tg_id == ?', (user_id,))
    cur.execute('DELETE FROM users WHERE user_tg_id == ?', (user_id,))
    base.commit()


# changed_days.py
async def change_days_before_repetition(data, message):
    list = [translation[0] for translation in cur.execute(
        'SELECT translation FROM phrases WHERE user_tg_id == ?', (message.from_user.id,)).fetchall()]
    if data['translation'] in list:
        cur.execute('UPDATE phrases SET days_before_repetition = ? WHERE translation = ?',
                    (data['days_before_repetition'], data['translation'],))
        base.commit()
    else:
        raise ValueError


# other.py
async def add_user_id_in_db(message):
    cur.execute(
        'INSERT INTO users VALUES(?, ?)', (message.from_user.id, str(date.today())))
    base.commit()

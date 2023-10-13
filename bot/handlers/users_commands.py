from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime
import asyncio
import random

from filters import OnlyCommand
from CONFIG import easy_sql
from utils.find_id import find_id
from utils.create_link_user import link_user
from utils.check_admin import check_on_admin
from utils.text_profile import text_profile


async def help_user(message: types.Message):
    if message.from_user.id != message.chat.id:
        return
    await message.answer('''
<b>Команды для пользователя:</b>

1) <code>Бонус</code> - выдает 🦎, работает раз в 24 часа;
2) <code>Подарить</code> - позволяет отправить ящерок🦎;
3) <code>Профиль</code> - показывает ваш профиль;
4) <code>Магазин</code> - вызывает меню с магазином.
''')


async def bonus(message: types.Message):
    rand = random.choice([0,0,0,0,0,0,0,0,0,1])
    rand_money = 5 if rand == 1 else 1
    hours = 24
    check_bonus = easy_sql.check_value(f'SELECT * FROM bonus WHERE id = {message.from_user.id}')
    if check_bonus is False:
        easy_sql.insert_into(f'INSERT INTO bonus VALUES ({message.from_user.id}, "0")')
    else:
        time_bonus = easy_sql.select(f'SELECT time FROM bonus WHERE id = {message.from_user.id}')[0]
        date_time_object_bonus = datetime.datetime.strptime(time_bonus, '%Y-%m-%d %H:%M:%S.%f')
        if (date_time_object_bonus) > datetime.datetime.now():
            await_date = str(date_time_object_bonus - datetime.datetime.now()).split('.')[0]
            return await message.answer(f'Вам осталось ждать <b>{await_date}</b>')
    easy_sql.update(f'UPDATE bonus SET time = "{datetime.datetime.now() + datetime.timedelta(hours=hours)}" WHERE id = {message.from_user.id}')
    easy_sql.update(f'UPDATE wallet SET balance = balance + {rand_money} WHERE id = {message.from_user.id}')
    await message.answer(f'Вы получили {rand_money} 🦎')


async def give_money(message: types.Message):
    user_id = await find_id(message)
    if user_id is False:
        return await message.answer('Пользователя не существует или он указан неверно!')
    money = int(message.text.split()[1])
    balance = easy_sql.select(f'SELECT balance FROM wallet WHERE id = {message.from_user.id}')[0]
    if money < 1:
        return await message.answer('Нельзя столько выдать!')
    if balance < money:
        return await message.answer('У вас недостаточно 🦎 на балансе!')
    easy_sql.update(f'UPDATE wallet SET balance = balance - {money} WHERE id = {message.from_user.id}')
    easy_sql.update(f'UPDATE wallet SET balance = balance + {money} WHERE id = {user_id}')
    user_give_link = await link_user(message.from_user.id, message.from_user.first_name)
    user_take_link = await link_user(user_id, easy_sql.select(f'SELECT first_name FROM users WHERE id = {user_id}')[0])
    await message.answer(f'{user_give_link} подарил <b>{money}</b> 🦎 {user_take_link}')


async def profile(message: types.Message):
    if (await check_on_admin(message.from_user.id)) is True:
        user_id = await find_id(message)
        if user_id is False:
            user_id = message.from_user.id
    else:
        user_id = message.from_user.id
    text = await text_profile(user_id)
    button = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Гайд', url='https://telegra.ph/𝕾𝖊𝖗𝖕𝖊𝖓𝖙𝖊-𝖘𝖍𝖔𝖕-03-20'))
    await message.answer(text, reply_markup=button)


async def marry(message: types.Message):
    a = await message.answer('Агу-агу\n\nP.s. Это вторая пасхалка :)')
    await asyncio.sleep(0.3)
    await a.delete()

array_user = []
async def baby(message: types.Message):
    global array_user
    if message.from_user.id in array_user:
        return
    array_user.append(message.from_user.id)
    a = await message.answer('Мама, я беременна...\n\nP.s. Это третья и последняя пасхалка!!! Держи приз 50 ящерок')
    easy_sql.update(f'UPDATE wallet SET balance = balance + 50 WHERE id = {message.from_user.id}')
    await asyncio.sleep(0.3)
    await a.delete()


def users_commands(dp: Dispatcher):
    dp.register_message_handler(bonus, OnlyCommand(only_cmd=['на охоту']))
    dp.register_message_handler(help_user, OnlyCommand(only_cmd=['помощь']))
    dp.register_message_handler(give_money, OnlyCommand(only_cmd=['перевести']))
    dp.register_message_handler(profile, OnlyCommand(only_cmd=['профиль']))
    dp.register_message_handler(marry, OnlyCommand(only_cmd=['брак']))
    dp.register_message_handler(baby, OnlyCommand(only_cmd=['ребенок']))
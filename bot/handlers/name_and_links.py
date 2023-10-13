from aiogram import types, Dispatcher
import aiogram.utils.markdown as fmt

from CONFIG import easy_sql
from filters import OnlyCommand


async def add_name(message: types.Message):
    users_check = easy_sql.check_value(f'SELECT id FROM nick WHERE id = {message.from_user.id}')
    if users_check is False:
        easy_sql.insert_into(f'INSERT INTO nick VALUES ({message.from_user.id}, "{message.text.split(maxsplit=1)[1]}")')
        return await message.answer('Вы сохранили свое имя!')
    easy_sql.update(f'UPDATE nick SET name = "{message.text.split(maxsplit=1)[1]}" WHERE id = {message.from_user.id}')
    await message.answer('Вы обновили свое имя!')


async def send_name(message: types.Message):
    if message.reply_to_message:
        users_check = easy_sql.check_value(f'SELECT id FROM nick WHERE id = {message.reply_to_message.from_user.id}')
        if users_check is False:
            return await message.answer(fmt.quote_html(message.reply_to_message.from_user.first_name))
        name_user = easy_sql.select(f'SELECT name FROM nick WHERE id = {message.reply_to_message.from_user.id}')[0]
    else:
        users_check = easy_sql.check_value(f'SELECT id FROM nick WHERE id = {message.from_user.id}')
        if users_check is False:
            return await message.answer(fmt.quote_html(message.from_user.first_name))
        name_user = easy_sql.select(f'SELECT name FROM nick WHERE id = {message.from_user.id}')[0]

    await message.answer(fmt.quote_html(name_user))


async def add_link(message: types.Message):
    users_check = easy_sql.check_value(f'SELECT id FROM links WHERE id = {message.from_user.id}')
    if users_check is False:
        easy_sql.insert_into(f'INSERT INTO links VALUES ({message.from_user.id}, "{message.text.split(maxsplit=1)[1]}")')
        return await message.answer('Вы сохранили свою ссылку!')
    easy_sql.update(f'UPDATE links SET link = "{message.text.split(maxsplit=1)[1]}" WHERE id = {message.from_user.id}')
    await message.answer('Вы обновили свою ссылку!')


async def send_link(message: types.Message):
    if message.reply_to_message:
        users_check = easy_sql.check_value(f'SELECT id FROM links WHERE id = {message.reply_to_message.from_user.id}')
        if users_check is False:
            return await message.answer('Пользователь не добавил свою ссылку!')
        link_user = easy_sql.select(f'SELECT link FROM links WHERE id = {message.reply_to_message.from_user.id}')[0]
    else:
        users_check = easy_sql.check_value(f'SELECT id FROM links WHERE id = {message.from_user.id}')
        if users_check is False:
            return await message.answer('Вы не добавили свою ссылку!')
        link_user = easy_sql.select(f'SELECT link FROM links WHERE id = {message.from_user.id}')[0]

    await message.answer(fmt.quote_html(link_user))


def name_and_links(dp: Dispatcher):
    dp.register_message_handler(send_name, OnlyCommand(only_cmd=['ник']))
    dp.register_message_handler(add_name, OnlyCommand(only_cmd=['+ник']))
    dp.register_message_handler(send_link, OnlyCommand(only_cmd=['сс']))
    dp.register_message_handler(add_link, OnlyCommand(only_cmd=['+сс']))
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from CONFIG import chats, easy_sql, bot

class CheckUser(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        if message.chat.id not in chats and message.chat.id != message.from_user.id:
            await message.answer(f'Бот в вашем чате работать не будет! Айди чата: <code>{message.chat.id}</code>')
            raise CancelHandler()
        check_user = easy_sql.check_value(f'SELECT * FROM users WHERE id = {message.from_user.id}')
        if check_user is False:
            easy_sql.insert_into(f'INSERT INTO count_sms VALUES ({message.from_user.id}, 0)')
            easy_sql.insert_into(f'INSERT INTO wallet VALUES({message.from_user.id}, 0)')
            return easy_sql.insert_into(f'INSERT INTO users VALUES ({message.from_user.id},\
                                                                   "{message.from_user.first_name}", \
                                                                   "{message.from_user.username.lower() if message.from_user.username is not None else None}")')
        easy_sql.update(f'UPDATE users SET first_name = "{message.from_user.first_name}", \
                                           username = "{message.from_user.username.lower() if message.from_user.username is not None else None}" WHERE id = {message.from_user.id}')
        easy_sql.update(f'UPDATE count_sms SET sms = sms + 1 WHERE id = {message.from_user.id}')

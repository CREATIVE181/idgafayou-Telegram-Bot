from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command

from utils.find_id import find_id
from utils.create_link_user import link_user
from CONFIG import easy_sql


async def act_rp(message: types.Message):
    user_id = await find_id(message)
    msg = message.text.split('\n', maxsplit=1)
    action = " ".join(msg[0].split()[1:])
    if len(msg) == 1:
        n = ''
    else:
        n = f'Со словами: {msg[1]}'
    user_send = await link_user(message.from_user.id, message.from_user.first_name)
    user_to = await link_user(user_id, easy_sql.select(f'SELECT first_name FROM users WHERE id = {user_id}')[0])
    text = f'{user_send} {action} {user_to}\n{n}'
    await message.answer(text)
     

def rp_commands(dp: Dispatcher):
    dp.register_message_handler(act_rp, Command(['gm'], prefixes='!/.', ignore_case=True))

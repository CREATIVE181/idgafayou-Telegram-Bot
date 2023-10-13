from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command, IDFilter
import aiogram.utils.markdown as fmt

from CONFIG import owners, easy_sql, chats, bot
from utils.find_id import find_id
from utils.create_link_user import link_user


async def help_owner(message: types.Message):
    await message.answer('''
<b>Команды для владельца:</b>

1) /up_admin | /down_admin - добавить/удалить админа;
2) /list_admin - список админов;
3) /накрутить | /обнулить - действия с балансом (лимит 100.000);
4) /id - если ничего не указывать, то покажет айди чата;
5) /declare - создает объявление во всех чатах;
''')


async def up_admin(message: types.Message):
    user_id = await find_id(message)
    if user_id is False:
        return await message.answer('Пользователя не существует или он указан неверно!')
    check_admin = easy_sql.check_value(f'SELECT * from admins WHERE id = {user_id}')
    if check_admin is not False:
        return await message.answer('Этот пользователь уже является админом!')
    easy_sql.insert_into(f'INSERT INTO admins VALUES ({user_id})')
    return await message.answer('Админ добавлен!')


async def down_admin(message: types.Message):
    user_id = await find_id(message)
    if user_id is False:
        return await message.answer('Пользователя не существует или он указан неверно!')
    check_admin = easy_sql.check_value(f'SELECT * from admins WHERE id = {user_id}')
    if check_admin is False:
        return await message.answer('Этот пользователь не является админом!')
    easy_sql.delete(f'DELETE FROM admins WHERE id = {user_id}')
    return await message.answer('Этот пользователь больше не админ!')
    

async def list_admin(message: types.Message):
    id_admins = [
        admin[0]
        for admin in easy_sql.select('SELECT * FROM admins', fetch='all')
    ]
    name_and_id_admins = [(easy_sql.select(f'SELECT first_name FROM users WHERE id = {id_admin}')[0], id_admin) for id_admin in id_admins]
    msg_with_admins = '<b>Список админов:</b>\n\n'
    numb = 1
    for name, adm_id in name_and_id_admins:
        admin = f'{numb}) {await link_user(adm_id, name)} - <code>{adm_id}</code>\n'
        msg_with_admins += admin
        numb += 1
    return await message.answer(msg_with_admins)


async def wind_up_owner(message: types.Message):
    user_id = await find_id(message)
    if user_id is False:
        user_id = message.from_user.id
    money = int(message.text.split()[1])
    if money > 100_000:
        return await message.answer('Лимит превышен!')
    easy_sql.update(f'UPDATE wallet SET balance = balance + {money} WHERE id = {user_id}')
    return await message.answer(f'Баланс пополнен на <b>{money}</b>🦎!')


async def wind_down_owner(message: types.Message):
    user_id = await find_id(message)
    if user_id is False:
        user_id = message.from_user.id
    easy_sql.update(f'UPDATE wallet SET balance = 0 WHERE id = {user_id}')
    return await message.answer('Баланс обнулен!')


async def id_user_or_chat(message: types.Message):
    user_id = await find_id(message)
    if len(message.text.split()) == 1 and user_id is False:
        return await message.answer(f'Айди чата: <code>{message.chat.id}</code>')
    elif user_id is False:
        return await message.answer('Пользователя не существует или он указан неверно!')
    else:
         return await message.answer(f'Айди пользователя: <code>{user_id}</code>')
    

async def declare(message: types.Message):
    msg = message.text.split('\n', maxsplit=1)[1]
    owner_link = f'<b>{await link_user(message.from_user.id, message.from_user.first_name)} ОБЪЯВЛЯЕТ:\n\n</b>'
    for chat in chats:
        try:    
            await bot.send_message(chat, text=owner_link + fmt.quote_html(msg))
            await message.answer(f'Сообщение отправлено✅ | <b>{chat}</b>')
        except Exception:
            await message.answer(f'Сообщение не отправлено❌ | <b>{chat}</b>')


async def amnesty(message: types.Message):
    easy_sql.delete('DELETE FROM warns')
    await message.answer('Все варны пользователей удалены!')


def owner_commands(dp: Dispatcher):
    dp.register_message_handler(help_owner, Command(['владелец'], prefixes='!/.', ignore_case=True), IDFilter(user_id=owners)) # +
    dp.register_message_handler(up_admin, Command(['up_admin'], prefixes='!/.', ignore_case=True), IDFilter(user_id=owners)) # +
    dp.register_message_handler(down_admin, Command(['down_admin'], prefixes='!/.', ignore_case=True), IDFilter(user_id=owners)) # +
    dp.register_message_handler(list_admin, Command(['list_admin'], prefixes='!/.', ignore_case=True), IDFilter(user_id=owners)) # +
    dp.register_message_handler(wind_up_owner, Command(['накрутить'], prefixes='!/.', ignore_case=True), IDFilter(user_id=owners)) # +
    dp.register_message_handler(wind_down_owner, Command(['обнулить'], prefixes='!/.', ignore_case=True), IDFilter(user_id=owners)) # +
    dp.register_message_handler(id_user_or_chat, Command(['id'], prefixes='!/.', ignore_case=True), IDFilter(user_id=owners)) # +
    dp.register_message_handler(declare, Command(['declare'], prefixes='!/.', ignore_case=True), IDFilter(user_id=owners)) # +
    # dp.register_message_handler(amnesty, Command(['амнистия'], prefixes='!/.', ignore_case=True), IDFilter(user_id=owners)) # +
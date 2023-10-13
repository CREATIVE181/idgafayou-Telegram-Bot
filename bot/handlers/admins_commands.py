from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types.chat_permissions import ChatPermissions
import aiogram.utils.markdown as fmt
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text

from CONFIG import easy_sql, bot
from utils.find_id import find_id
from utils.create_link_user import link_user
from utils.send_spare import send_spare
from utils.check_admin import check_on_admin
from utils.time_to_unix import time_to_timedelta
from filters import OnlyCommand


PERMISSIONS = None


async def default_code(message, user_id):
    full_message = message.text.split('\n', maxsplit=1)
    if len(full_message) == 2:
        cause = fmt.quote_html(full_message[1])
    else:
        cause = 'Не указана'
    user_first_name = easy_sql.select(f'SELECT first_name FROM users WHERE id = {user_id}')[0]
    user_link = await link_user(user_id, user_first_name)
    admin_link = await link_user(message.from_user.id, message.from_user.first_name)
    return user_link, admin_link, cause


async def help_admin(message: types.Message):
    if (await check_on_admin(message.from_user.id)) is False:
        return
    await message.answer('''
<b>Команды для админа:</b>

1) /warn | /unwarn - выдает/забирает варн;
2) /warn_list - список варнов пользователей;
3) /ban | /unban - блокирует/разблокирует пользователя;
4) /mute | /unmute - запрщает/разрешает говорить польхзователь;
5) /kick - исключает пользователя;
6) /give - выдаёт валюту (лимит 2000);
7) /top_balance - показывает список богачей.
''')


async def warn(message: types.Message):
    if (await check_on_admin(message.from_user.id)) is False:
        return
    user_id = await find_id(message)
    if user_id is False:
        return await message.answer('Пользователя не существует или он указан неверно!')
    user_link, admin_link, cause = await default_code(message, user_id)
    check_warns = easy_sql.check_value(f'SELECT * FROM warns WHERE id = {user_id}')
    if check_warns is False:
        easy_sql.insert_into(f'INSERT INTO warns VALUES ({user_id}, 1)')
    else:
        easy_sql.update(f'UPDATE warns SET count_warns = count_warns + 1 WHERE id = {user_id}')
    await send_spare('warn', message.from_user.id, user_id, (message.chat.title, message.chat.id), cause,  message.message_id)
    if easy_sql.select(f'SELECT count_warns FROM warns WHERE id = {user_id}')[0] == 5:
        await bot.kick_chat_member(chat_id=message.chat.id, user_id=user_id)
        await message.answer(f'{user_link} был заблокирован по достижению 5-ти варнов!')
        await send_spare('ban', message.from_user.id, user_id, (message.chat.title, message.chat.id), 'Достижение 5-ти варнов', message.message_id)
        easy_sql.delete(f'DELETE FROM warns WHERE id = {user_id}')
    return await message.answer(f'{admin_link} выдал варн {user_link}\nПричина: {cause}')


async def unwarn(message: types.Message):
    if (await check_on_admin(message.from_user.id)) is False:
        return
    user_id = await find_id(message)
    if user_id is False:
        return await message.answer('Пользователя не существует или он указан неверно!')
    user_link, admin_link, cause = await default_code(message, user_id)
    check_warns = easy_sql.check_value(f'SELECT * FROM warns WHERE id = {user_id}')
    if check_warns is False:
        return await message.answer('У этого пользователя и так нет варнов!')
    easy_sql.update(f'UPDATE warns SET count_warns = count_warns - 1 WHERE id = {user_id}')
    if easy_sql.select(f'SELECT count_warns FROM warns WHERE id = {user_id}')[0] == 0:
        easy_sql.delete(f'DELETE FROM warns WHERE id = {user_id}')
    await send_spare('unwarn', message.from_user.id, user_id, (message.chat.title, message.chat.id), cause,  message.message_id)
    return await message.answer(f'{admin_link} снял варн {user_link}\nПричина: {cause}')
    

async def warn_list(message: types.Message):
    if (await check_on_admin(message.from_user.id)) is False:
        return
    warns = easy_sql.select('SELECT * FROM warns', fetch='all')
    id_name_warns = [(await link_user(user_id, easy_sql.select(f'SELECT first_name FROM users WHERE id = {user_id}')[0]), warn) for user_id, warn in warns][:30]
    sorted_list_with_warns = sorted(id_name_warns, reverse=True, key=lambda x: x[1])
    result_msg = f'<b>Список варнов:</b>\n\n'
    for user, warn in sorted_list_with_warns:
        result_msg += f'• {user} - {warn}\n'
    await message.answer(result_msg)


async def ban(message: types.Message):
    if (await check_on_admin(message.from_user.id)) is False:
        return
    user_id = await find_id(message)
    if user_id is False:
        return await message.answer('Пользователя не существует или он указан неверно!')
    user_link, admin_link, cause = await default_code(message, user_id)
    try:
        await bot.ban_chat_member(chat_id=message.chat.id, user_id=user_id)
    except Exception:
        return await message.answer('Мне не удалось это сделать!')
    await message.answer(f'{admin_link} выдал бан {user_link}\nПричина: {cause}')
    return await send_spare('ban', message.from_user.id, user_id, (message.chat.title, message.chat.id), cause, message.message_id)


async def unban(message: types.Message):
    if (await check_on_admin(message.from_user.id)) is False:
        return
    user_id = await find_id(message)
    if user_id is False:
        return await message.answer('Пользователя не существует или он указан неверно!')
    user_link, admin_link, cause = await default_code(message, user_id)
    try:
        await bot.unban_chat_member(chat_id=message.chat.id, user_id=user_id)
    except Exception:
        return await message.answer('Мне не удалось это сделать!')
    await message.answer(f'{admin_link} снял бан {user_link}\nПричина: {cause}')
    return await send_spare('unban', message.from_user.id, user_id, (message.chat.title, message.chat.id), cause, message.message_id)


async def kick(message: types.Message):
    if (await check_on_admin(message.from_user.id)) is False:
        return
    user_id = await find_id(message)
    if user_id is False:
        return await message.answer('Пользователя не существует или он указан неверно!')
    user_link, admin_link, cause = await default_code(message, user_id)
    try:
        await bot.kick_chat_member(chat_id=message.chat.id, user_id=user_id)
    except Exception:
        return await message.answer('Мне не удалось это сделать!')
    await message.answer(f'{admin_link} выгнал {user_link}\nПричина: {cause}')
    return await send_spare('kick', message.from_user.id, user_id, (message.chat.title, message.chat.id), cause, message.message_id)


async def mute(message: types.Message):
    if (await check_on_admin(message.from_user.id)) is False:
        return
    user_id = await find_id(message)
    if user_id is False:
        return await message.answer('Пользователя не существует или он указан неверно!')
    user_link, admin_link, cause = await default_code(message, user_id)
    global PERMISSIONS
    PERMISSIONS = (await bot.get_chat(message.chat.id)).permissions
    try:
        unix_time = await time_to_timedelta(message.text.split()[1])
    except Exception:
        unix_time = await time_to_timedelta('1ч')
    try:
        await bot.restrict_chat_member(chat_id=message.chat.id, user_id=user_id, permissions=ChatPermissions(can_send_messages=False), until_date=unix_time)
    except Exception:
        return await message.answer('Мне не удалось это сделать!')
    await message.answer(f'{admin_link} запретил говорить {user_link}\nПричина: {cause}')
    return await send_spare('mute', message.from_user.id, user_id, (message.chat.title, message.chat.id), cause, message.message_id)


async def unmute(message: types.Message):
    if (await check_on_admin(message.from_user.id)) is False:
        return
    user_id = await find_id(message)
    if user_id is False:
        return await message.answer('Пользователя не существует или он указан неверно!')
    user_link, admin_link, cause = await default_code(message, user_id)
    try:
        await bot.restrict_chat_member(chat_id=message.chat.id, user_id=user_id, permissions=PERMISSIONS)
    except Exception:
        return await message.answer('Мне не удалось это сделать!')
    await message.answer(f'{admin_link} разрешил говорить {user_link}\nПричина: {cause}')
    return await send_spare('unmute', message.from_user.id, user_id, (message.chat.title, message.chat.id), cause, message.message_id)


async def wind_up_admin(message: types.Message):
    if (await check_on_admin(message.from_user.id)) is False:
        return
    user_id = await find_id(message)
    if user_id is False:
        return await message.answer('Пользователя не существует или он указан неверно!')
    user_link, admin_link, cause = await default_code(message, user_id)
    money = int(message.text.split()[1])
    cause += f' (Выдано {money} 🦎)'
    if money > 2_000 or money < 1:
        return await message.answer('Нельзя столько выдать!')
    easy_sql.update(f'UPDATE wallet SET balance = balance + {money} WHERE id = {user_id}')
    await message.answer(f'{admin_link} выдал 🦎 {user_link}\nПричина: {cause}')
    return await send_spare('give', message.from_user.id, user_id, (message.chat.title, message.chat.id), cause, message.message_id)


async def top_balance(message: types.Message):
    if (await check_on_admin(message.from_user.id)) is False:
        return
    wallets = easy_sql.select('SELECT * FROM wallet', fetch='all')
    id_name_balance = [(await link_user(user_id, easy_sql.select(f'SELECT first_name FROM users WHERE id = {user_id}')[0]), balance) for user_id, balance in wallets][:30]
    sorted_list_with_balance = sorted(id_name_balance, reverse=True, key=lambda x: x[1])
    result_msg = f'<b>Топ богачей:</b>\n\n'
    for user, balance in sorted_list_with_balance:
        if balance == 0:
            continue
        result_msg += f'• {user} - {balance}🦎\n'
    await message.answer(result_msg)


async def top_sms(message: types.Message):
    if (await check_on_admin(message.from_user.id)) is False:
        return
    sms_count = easy_sql.select('SELECT * FROM count_sms', fetch='all')
    id_name_sms = [(await link_user(user_id, easy_sql.select(f'SELECT first_name FROM users WHERE id = {user_id}')[0]), sms) for user_id, sms in sms_count][:30]
    sorted_list_with_sms = sorted(id_name_sms, reverse=True, key=lambda x: x[1])
    result_msg = f'<b>Топ сообщений:</b>\n\n'
    for user, balance in sorted_list_with_sms:
        if balance == 0:
            continue
        result_msg += f'• {user} - {balance}🦎\n'
    await message.answer(result_msg)


async def ruffle_game(message: types.Message):
    if (await check_on_admin(message.from_user.id)) is False:
        return
    amount = int(message.text.split()[1])
    button = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='ХАЛЯВА', callback_data=f'raffle:{amount}'))
    await message.answer('Нажимай на кнопку, чтобы получать ящерок!', reply_markup=button)


ruffle_array = []
async def ruffle_button(callback: types.CallbackQuery):
    amount = int(callback.data.split(':')[1])
    global ruffle_array
    if len(ruffle_array) + 1 == amount:
        ruffle_array = []
        await callback.message.edit_text('Конец! Все призы закончились(')
    if callback.from_user.id not in ruffle_array:
        ruffle_array.append(callback.from_user.id)
        easy_sql.update(f'UPDATE wallet SET balance = balance + 1 WHERE id = {callback.from_user.id}')
        return await callback.answer('Вы получили 1 змейку!')
    await callback.answer('Вы уже получили свою награду!')


def admins_commands(dp: Dispatcher):
    dp.register_message_handler(help_admin, Command(['админ'], prefixes='!/.', ignore_case=True)) # +
    dp.register_message_handler(warn, Command(['warn'], prefixes='!/.', ignore_case=True)) # +
    dp.register_message_handler(unwarn, Command(['unwarn'], prefixes='!/.', ignore_case=True)) # +
    # dp.register_message_handler(ban, Command(['ban'], prefixes='!/.', ignore_case=True)) # +
    # dp.register_message_handler(unban, Command(['unban'], prefixes='!/.', ignore_case=True)) # +
    # dp.register_message_handler(kick, Command(['kick'], prefixes='!/.', ignore_case=True)) # +
    # dp.register_message_handler(mute, Command(['mute'], prefixes='!/.', ignore_case=True)) # +
    # dp.register_message_handler(unmute, Command(['unmute'], prefixes='!/.', ignore_case=True)) # +
    dp.register_message_handler(wind_up_admin, Command(['give'], prefixes='!/.', ignore_case=True)) # +
    dp.register_message_handler(warn_list, Command(['warn_list'], prefixes='!/.', ignore_case=True)) # +
    dp.register_message_handler(top_balance, Command(['top_balance'], prefixes='!/.', ignore_case=True)) # +
    dp.register_message_handler(top_sms, Command(['top_sms'], prefixes='!/.', ignore_case=True)) # +
    dp.register_message_handler(ruffle_game, OnlyCommand(only_cmd=['розыгрыш'])) # +
    dp.register_callback_query_handler(ruffle_button, Text(startswith='raffle')) # +


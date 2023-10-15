from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text

from filters import OnlyCommand
from CONFIG import easy_sql
from utils.find_id import find_id
from utils.create_link_user import link_user


async def request(message: types.Message):
    user_1 = message.from_user.id
    user_2 = await find_id(message)
    if user_2 is False:
        return
    elif user_1 == user_2:
        return await message.answer('Вы не можете предложить выйти за самого себя')
    check_user_1 = easy_sql.select(f'SELECT id_1, id_2 FROM marriage WHERE id_1 == {user_1} OR id_2 == {user_1}')
    if check_user_1 is not None and user_1 in check_user_1:
        return await message.answer('У вас уже есть брак')
    
    check_user_2 = easy_sql.select(f'SELECT id_1, id_2 FROM marriage WHERE id_1 == {user_2} OR id_2 == {user_2}')
    if check_user_2 is not None and user_2 in check_user_2:
            return await message.answer('У этого человека уже есть брак')
    
    check_ring = easy_sql.check_value(f'SELECT ring FROM rings WHERE id == {user_1}')
    if check_ring is False:
        return await message.answer('У вас нет кольца')
    
    username_1 = await link_user(user_1, message.from_user.first_name)
    username_2 = await link_user(user_2, 'Вам')
    buttons = buttons = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Согласиться', callback_data=f'act_mar:{user_1}:{user_2}:1'), InlineKeyboardButton(text='Отказаться', callback_data=f'act_mar:{user_1}:{user_2}:0'))
    await message.answer(f'<b>Внимание!</b>\n{username_1} сделал {username_2} предложение 💕', reply_markup=buttons)
    
    
async def send_answer(callback: types.CallbackQuery):
    user_id_1, user_id_2, var = callback.data.split(':')[1:]
    if callback.from_user.id != int(user_id_2):
        return await callback.answer('Это не ваша кнопка!')
    if var == '0':
        return await callback.message.edit_text('Вы отказались играть свадьбу')
    easy_sql.insert_into(f'INSERT INTO marriage VALUES ({user_id_1}, {user_id_2})')
    easy_sql.delete(f'DELETE FROM rings WHERE id == {user_id_1}')
    await callback.message.edit_text('Зарегистрирован новый брак 💕')
    
    
async def dissolve_marriage(message: types.Message):
    check_user = easy_sql.check_value(f'SELECT id_1, id_2 FROM marriage WHERE id_1 == {message.from_user.id} OR id_2 == {message.from_user.id}')
    if check_user is False:
        return await message.answer('У вас нет брака')
    easy_sql.delete(f'DELETE FROM marriage WHERE id_1 == {message.from_user.id} OR id_2 == {message.from_user.id}')
    await message.answer('Брак расторгнут 🥺')
    
    
async def give_ring(message: types.Message):
    check_user_1 = easy_sql.check_value(f'SELECT id FROM rings WHERE id == {message.from_user.id}')
    if check_user_1 is False:
        return await message.answer('У вас нет кольца!')
    user_2 = await find_id(message)
    check_user_2 = easy_sql.check_value(f'SELECT id FROM rings WHERE id == {user_2}')
    if check_user_2 is True:
        return await message.answer('У этого пользователя уже есть кольцо!')
    easy_sql.delete(f'DELETE FROM rings WHERE id == {message.from_user.id}')
    easy_sql.insert_into(f'INSERT INTO rings VALUES ({user_2}, 1)')
    await message.answer('Кольцо передано 💍')
    

def marriage(dp: Dispatcher):
    dp.register_message_handler(request, OnlyCommand(only_cmd=['брак']))
    dp.register_callback_query_handler(send_answer, Text(startswith='act_mar'))
    dp.register_message_handler(dissolve_marriage, OnlyCommand(only_cmd=['развод']))
    dp.register_message_handler(give_ring, OnlyCommand(only_cmd=['подарить кольцо']))
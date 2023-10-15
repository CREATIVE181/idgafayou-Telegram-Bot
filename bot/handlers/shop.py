from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from filters import OnlyCommand
from CONFIG import easy_sql
from utils.create_buttons_shop import ButtonsShop
from utils.create_link_user import link_user


bs = ButtonsShop()
async def create_shop(message: types.Message):
    if message.chat.id != message.from_user.id:
        return
    buttons = await bs.category()
    user = await link_user(message.from_user.id, message.from_user.first_name)
    await message.answer(f'''
Привет, {user} , добро пожаловать в змеиный маркет

Тут ты сможешь воспользоваться услугами нашего магазина 🖤''', reply_markup=buttons)


async def react_shop(callback: types.CallbackQuery):
    category_products = callback.data.split(':')[1]
    await callback.message.edit_text('Выберите продукт', reply_markup=(await bs.goods_cat(category_products)))


async def var_product(callback: types.CallbackQuery):
    data_product = callback.data.split(':')[1:]
    await callback.message.edit_text('Выберите продукт', reply_markup=(await bs.variation_good(data_product[0])))


async def prod(callback: types.CallbackQuery):
    data_product = callback.data.split(':')[1:]
    result = await bs.what_good(data_product, callback.from_user.id)
    await callback.message.edit_text(result[0], reply_markup=result[1])


async def buy_product(callback: types.CallbackQuery):
    data_product = callback.data.split(':')[1:]
    balance = easy_sql.select(f'SELECT balance FROM wallet WHERE id = {callback.from_user.id}')[0]
    button = InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text='Назад', callback_data='cancel')
    )
    if int(data_product[-1]) > balance:
        return await callback.message.edit_text('У вас недостаточно средств на баласе!', reply_markup=button)
    easy_sql.update(f'UPDATE wallet SET balance = balance - {int(data_product[-1])} WHERE id = {callback.from_user.id}')
    await bs.action(data_product[:-1], callback.from_user.id, callback)
    await callback.message.edit_text('Покупка произведена успешно!', reply_markup=button)


async def cancel(callback: types.CallbackQuery):
    await callback.message.edit_text('Выбирете категорию:', reply_markup=(await bs.category()))


def shop(dp: Dispatcher):
    dp.register_message_handler(create_shop, OnlyCommand(only_cmd=['магазин']))
    dp.register_callback_query_handler(react_shop, Text(startswith='goods'))
    dp.register_callback_query_handler(var_product, Text(startswith='var'))
    dp.register_callback_query_handler(prod, Text(startswith='prod'))
    dp.register_callback_query_handler(buy_product, Text(startswith='buy'))
    dp.register_callback_query_handler(cancel, Text(startswith='cancel'))

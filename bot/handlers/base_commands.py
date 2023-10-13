from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.create_link_user import link_user


async def command_start(message: types.Message):
    user = await link_user(message.from_user.id, message.from_user.first_name)
    await message.answer(f'''
Привет, {user}, Добро пожаловать в наш змеиный маркет 🦎

<code>Тут ты сможешь воспользоваться услугами нашего магазина 🖤</code>

• Для начала работы с ботом - напиши команду «профиль» в этом чате

• Если у тебя есть какие-либо вопросы напиши команду /help''')


async def command_help(message: types.Message):
    buttons = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Тех. поддержка', url='https://t.me/SerpentoHelpbot'),
                                                    InlineKeyboardButton(text='Главный администратор', url='https://t.me/idgafayou'))
    await message.answer('Для начала работы с ботом, напишите «профиль» в этом чате.\n\nПо другим вопросам можно обратиться в поддержку', reply_markup=buttons)


def base_commands(dp: Dispatcher):
    dp.register_message_handler(command_start, Command(['start'], prefixes='!/.', ignore_case=True))
    dp.register_message_handler(command_help, Command(['help'], prefixes='!/.', ignore_case=True))
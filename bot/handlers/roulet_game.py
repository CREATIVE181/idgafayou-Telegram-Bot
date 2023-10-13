from aiogram import types, Dispatcher
import random

from filters import OnlyCommand


async def roul_game(message: types.Message):
    rand = random.choice([1,1,1,2,2])
    if rand == 1:
        return await message.answer('Вы проиграли(')
    else:
        await message.answer('Вы выиграли!')


def roulet_game(dp: Dispatcher):
    dp.register_message_handler(roul_game, OnlyCommand(only_cmd=['рулетка']))
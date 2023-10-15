from aiogram import types, Dispatcher
import random

from filters import OnlyCommand


async def rand_g(message: types.Message):
    msg = message.text.split()
    numb1 = int(msg[1])
    numb2 = int(msg[2])
    await message.answer(f'Твоё случайное число: <b>{random.randint(numb1, numb2)}</b>')


def marriage(dp: Dispatcher):
    dp.register_message_handler(rand_g, OnlyCommand(only_cmd=['брак']))
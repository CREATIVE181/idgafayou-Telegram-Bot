from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text

from filters import OnlyCommand
from CONFIG import owners, dp, easy_sql


array = []


async def ruffle_game(message: types.Message):
    msg = message.text.split()[1:]
    
    


def raffle(dsp: Dispatcher):
    dsp.register_message_handler(ruffle_game, OnlyCommand(only_cmd=['розыгрыш']))

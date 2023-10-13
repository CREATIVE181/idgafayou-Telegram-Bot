from aiogram import Dispatcher


async def reg_user(message):
    pass


def register_users(dp: Dispatcher):
    dp.register_message_handler(reg_user)

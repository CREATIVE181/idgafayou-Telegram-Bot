from aiogram import Dispatcher

from .OnlyCMD import OnlyCommand


def setup(dp: Dispatcher):
    dp.filters_factory.bind(OnlyCommand)

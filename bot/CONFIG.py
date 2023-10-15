from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from easy_sqlite3 import EasySQLite3

easy_sql = EasySQLite3()
easy_sql.connect(path='db/database.db')

easy_sql.create_table('''CREATE TABLE
IF
	NOT EXISTS rings (
	id INTEGER PRIMARY KEY,
	ring INTEGER)''')

easy_sql.create_table('''CREATE TABLE
IF
	NOT EXISTS marriage (
	id_1 INTEGER,
	id_2 INTEGER)''')

token = '6444073394:AAGH-76THPLgmM3OvdHDaDBFQ3h0I3vmzS8'
owners = [754834498, 497281548]
chats = [-1001871430811,
         -1001953022077,
         -1001921515371,
         -1001863605735,
         -1001871128276]
spare_chat = -1001734897208
shop_chat = -1001863605735
default_chat = -1001921515371


bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

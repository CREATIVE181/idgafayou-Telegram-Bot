from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.utils.exceptions import BadRequest
from asyncio import sleep

from CONFIG import easy_sql, default_chat, bot, dp, shop_chat
from states.state_prefix import State_Prefix
from utils.create_link_user import link_user


class ButtonsShop():

    async def category(self):
        category_goods = {
            i[0] for i in easy_sql.select('SELECT type FROM goods', fetch='all')
        }
        buttons = InlineKeyboardMarkup(row_width=2)
        for name in category_goods:
            buttons.insert(InlineKeyboardButton(text=name, callback_data=f'goods:{name}'))
        buttons.add(InlineKeyboardButton(text='Купить валюту', url='https://t.me/idgafayou'))
        return buttons
    

    async def goods_cat(self, category_good):
        goods = list(
            easy_sql.select(
                f'SELECT id, name, variations FROM goods WHERE type = "{category_good}"',
                fetch='all',
            )
        )
        buttons = InlineKeyboardMarkup(row_width=1)
        for id_good, name, var in goods:
            if var == 1:
                buttons.insert(InlineKeyboardButton(text=name, callback_data=f'var:{id_good}'))
            else:
                buttons.insert(InlineKeyboardButton(text=name, callback_data=f'prod:{id_good}'))
        buttons.add(InlineKeyboardButton(text='Назад', callback_data='cancel'))
        return buttons
    

    async def variation_good(self, id_good):
        variations_goods = list(
            easy_sql.select(
                f'SELECT id_var, name FROM variations_goods WHERE id = {id_good}',
                fetch='all',
            )
        )
        buttons = InlineKeyboardMarkup(row_width=1)
        for id_good_var, name in variations_goods:
            buttons.insert(InlineKeyboardButton(text=name, callback_data=f'prod:{id_good}:{id_good_var}'))
        buttons.add(InlineKeyboardButton(text='Назад', callback_data='cancel'))
        return buttons


    async def what_good(self, all_id):
        if len(all_id) == 1:
            name, price = easy_sql.select(f'SELECT name, price FROM goods WHERE id = {all_id[0]}')
        else:
            name, price = easy_sql.select(f'SELECT name, price FROM variations_goods WHERE id = {all_id[0]} AND id_var = {all_id[1]}')
        buttons = InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton(
                text='Купить', callback_data=f'buy:{":".join(all_id)}:{price}'
            ),
            InlineKeyboardButton(text='Отмена', callback_data='cancel'),
        )
        text = f'''
Купить <b>{name}</b> за <b>{price}</b>?'''
        return text, buttons
    

    async def action(self, id_good, user_id, callback):
        id_good = list(map(int, id_good))
        if len(id_good) == 1:
            if id_good[0] == 1:
                try:
                    warns = easy_sql.select(f'SELECT count_warns FROM warns WHERE id = {user_id}')[0]
                    if warns == 0:
                        return
                    else:
                        easy_sql.update(f'UPDATE warns SET count_warns = count_warns - 1 WHERE id = {user_id}')
                except Exception:
                    return
            elif id_good[0] == 2:
                await bot.unban_chat_member(chat_id=default_chat, user_id=user_id)
        else:
            name = f"{easy_sql.select(f'SELECT name FROM goods WHERE id = {id_good[0]}')[0]} {easy_sql.select(f'SELECT name FROM variations_goods WHERE id = {id_good[0]} AND id_var = {id_good[1]}')[0]}"
            user_link = await link_user(user_id, callback.from_user.first_name)
            await bot.send_message(shop_chat, f'{user_link} [{f"<code>{callback.from_user.id}</code>" if callback.from_user.username is None else f"@{callback.from_user.username}"}] купил {name}\n\n1) tg://openmessage?user_id={callback.from_user.id}\n2) tg://user?id={callback.from_user.id}')
            await bot.send_message(497281548, f'{user_link} [{f"<code>{callback.from_user.id}</code>" if callback.from_user.username is None else f"@{callback.from_user.username}"}] купил {name}\n\n1) tg://openmessage?user_id={callback.from_user.id}\n2) tg://user?id={callback.from_user.id}')
            if id_good[0] in [4, 5]:
                await bot.send_message(user_id, 'Введите префикс')
                await State_Prefix.Q1.set()


@dp.message_handler(state=State_Prefix.Q1)
async def setup_prefix(message: types.Message, state: FSMContext):
    prefix_text = message.text
    await state.finish()
    try:
        await bot.promote_chat_member(chat_id=default_chat, user_id=message.from_id, can_manage_voice_chats=True)
    except BadRequest:
        return await message.answer('У бота недостаточно прав. Обратитесь за помощью к администрации или выдайте возможность "Выбор администраторов"')
    await sleep(1)
    await bot.set_chat_administrator_custom_title(chat_id=default_chat, user_id=message.from_id, custom_title=prefix_text)
    await message.answer('Префикс выдан!')

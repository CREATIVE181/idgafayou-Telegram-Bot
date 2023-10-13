import aiogram.utils.markdown as fmt

from CONFIG import easy_sql, owners
from utils.check_admin import check_on_admin


async def text_profile(user_id):
    first_name = easy_sql.select(f'SELECT first_name FROM users WHERE id = {user_id}')[0]
    balance = easy_sql.select(f'SELECT balance FROM wallet WHERE id = {user_id}')[0]
    sms = easy_sql.select(f'SELECT sms FROM count_sms WHERE id = {user_id}')[0]
    try:
        warns = easy_sql.select(f'SELECT count_warns FROM warns WHERE id = {user_id}')[0]
    except Exception:
        warns = 0
    if user_id == 754834498:
        status = 'Разраб'
    elif user_id in owners:
        status = 'Владелец'
    elif (await check_on_admin(user_id)) is True:
        status = 'Админ'
    else:
        status = 'Участник'
    text = f'''
🖲Ник: <code>{fmt.quote_html(first_name)}</code>
💼Статус: <code>{status}</code>
🦎Баланс: <code>{balance}</code>
🚫Варны: <code>{warns}/5</code>
💌Сообщений: <code>{sms}</code>
'''
    return text

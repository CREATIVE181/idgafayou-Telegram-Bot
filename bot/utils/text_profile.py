import aiogram.utils.markdown as fmt

from CONFIG import easy_sql, owners
from utils.check_admin import check_on_admin
from utils.create_link_user import link_user


async def text_profile(user_id):
    first_name = easy_sql.select(f'SELECT first_name FROM users WHERE id = {user_id}')[0]
    balance = easy_sql.select(f'SELECT balance FROM wallet WHERE id = {user_id}')[0]
    sms = easy_sql.select(f'SELECT sms FROM count_sms WHERE id = {user_id}')[0]
    check_marriage = easy_sql.select(f'SELECT id_1, id_2 FROM marriage WHERE id_1 == {user_id} OR id_2 == {user_id}')
    if check_marriage is not None:
        if check_marriage[0] == user_id:
            first_name_2 = easy_sql.select(f'SELECT first_name FROM users WHERE id = {check_marriage[1]}')[0]
            username = await link_user(check_marriage[1], first_name_2)
        else:
            first_name_2 = easy_sql.select(f'SELECT first_name FROM users WHERE id = {check_marriage[0]}')[0]
            username = await link_user(check_marriage[0], first_name_2)
        marriage = f'👩‍❤️‍👨Брак: {username}'
    else:
        marriage = ''
    ring = 'Есть' if easy_sql.check_value(f'SELECT ring FROM rings WHERE id == {user_id}') else 'Нет'
    if user_id == 754834498:
        status = 'Разраб'
    elif user_id in owners:
        status = 'Владелец'
    elif (await check_on_admin(user_id)) is True:
        status = 'Админ'
    else:
        status = 'Участник'
    return f'''
🖲Ник: <code>{fmt.quote_html(first_name)}</code>
💼Статус: <code>{status}</code>
🦎Баланс: <code>{balance}</code>
💌Сообщений: <code>{sms}</code>
💍Кольцо: <code>{ring}</code>
{marriage}
'''

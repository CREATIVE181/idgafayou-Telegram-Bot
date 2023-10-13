from CONFIG import bot, spare_chat, easy_sql
from utils.create_link_user import link_user


async def send_spare(action, admin_id, user_id, group, cause, message_id):
    admin_link = await link_user(admin_id, easy_sql.select(f'SELECT first_name FROM users WHERE id = {admin_id}')[0])
    user_link = await link_user(user_id, easy_sql.select(f'SELECT first_name FROM users WHERE id = {user_id}')[0])
    if_warn = ''
    if action in ['warn', 'unwarn']:
        try:
            if_warn = f'\n• Предупреждения: {easy_sql.select(f"SELECT count_warns FROM warns WHERE id = {user_id}")[0]}/6'
        except Exception:
            if_warn = f'\n• Предупреждения: 0/6'
    await bot.send_message(spare_chat, text=f'''
❕ #{action.upper()} ➕
• Кто: {admin_link} [<code>{admin_id}</code>] 
• Кому: {user_link} [<code>{user_id}</code>]
• Группа: {group[0]} [<code>{group[1]}</code>]
• Причина: {cause} {if_warn}
• 👀 Посмотреть сообщения (https://t.me/c/{str(group[1])[4:]}/{message_id})
#id{user_id}
''')
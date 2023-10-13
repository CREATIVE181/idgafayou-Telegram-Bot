from CONFIG import bot, spare_chat, easy_sql
from utils.create_link_user import link_user


async def send_spare(action, admin_id, user_id, group, cause, message_id):
    admin_link = await link_user(admin_id, easy_sql.select(f'SELECT first_name FROM users WHERE id = {admin_id}')[0])
    user_link = await link_user(user_id, easy_sql.select(f'SELECT first_name FROM users WHERE id = {user_id}')[0])
    await bot.send_message(spare_chat, text=f'''
❕ #{action.upper()} ➕
• Кто: {admin_link} [<code>{admin_id}</code>] 
• Кому: {user_link} [<code>{user_id}</code>]
• Группа: {group[0]} [<code>{group[1]}</code>]

• 👀 Посмотреть сообщения (https://t.me/c/{str(group[1])[4:]}/{message_id})
#id{user_id}
''')
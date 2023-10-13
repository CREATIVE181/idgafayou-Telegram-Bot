import aiogram.utils.markdown as fmt

async def link_user(user_id, first_name):
    return f'<a href="tg://openmessage?user_id={user_id}">{fmt.quote_html(first_name)}</a>'
from CONFIG import easy_sql


async def check_on_admin(user_id):
    list_admins = [
        admin_id[0]
        for admin_id in easy_sql.select('SELECT id FROM admins', fetch='all')
    ]
    if user_id in list_admins:
        return True
    else:
        return False
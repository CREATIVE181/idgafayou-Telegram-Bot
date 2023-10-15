from aiogram.utils import executor

from CONFIG import dp
from middlewares.check_user import CheckUser
from handlers import base_commands, register_users, owner_commands, admins_commands, users_commands, shop, open_close, \
                     name_and_links, roulet_game, random_game, rp_commands, marriage


base_commands.base_commands(dp)
owner_commands.owner_commands(dp)
admins_commands.admins_commands(dp)
users_commands.users_commands(dp)
shop.shop(dp)
open_close.open_close(dp)
name_and_links.name_and_links(dp)
roulet_game.roulet_game(dp)
random_game.random_game(dp)
rp_commands.rp_commands(dp)
marriage.marriage(dp)


register_users.register_users(dp) # в конце!






if __name__ == '__main__':
    dp.middleware.setup(CheckUser())
    executor.start_polling(dp, skip_updates=True)

from aiogram import types, Dispatcher
from aiogram.types.chat_permissions import ChatPermissions

from filters import OnlyCommand
from utils.check_admin import check_on_admin
from CONFIG import bot


async def open_close_chat(message: types.Message):
    if (await check_on_admin(message.from_user.id)) is False:
        return
    msg = message.text.lower()
    if msg == '.закрыть':
        await bot.set_chat_permissions(message.chat.id, (ChatPermissions(can_send_messages=False)))
        await message.answer('Чат закрыт!')
    elif msg == '.открыть':
        await bot.set_chat_permissions(message.chat.id, (ChatPermissions(can_send_messages=True,
                                                                         can_send_audios=False,
                                                                         can_send_documents=False,
                                                                         can_send_photos=False,
                                                                         can_send_videos=False,
                                                                         can_send_polls=False,
                                                                         can_change_info=False,
                                                                         can_invite_users=False,
                                                                         can_pin_messages=False,
                                                                         can_send_video_notes=False,
                                                                         can_send_voice_notes=False,
                                                                         can_send_other_messages=True,
                                                                         can_add_web_page_previews=False,
                                                                         can_manage_topics=False)))
        await message.answer('Чат открыт!')



def open_close(dsp: Dispatcher):
    dsp.register_message_handler(open_close_chat, OnlyCommand(only_cmd=['.открыть', '.закрыть']))

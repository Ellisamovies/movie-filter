"""Get info about the replied user
Syntax: .whois"""

import os
import time
from datetime import datetime
from pyrogram import Client, filters, enums
from pyrogram.errors import UserNotParticipant
from info import COMMAND_HAND_LER
from plugins.helper_functions.extract_user import extract_user
from plugins.helper_functions.cust_p_filters import f_onw_fliter
from plugins.helper_functions.last_online_hlpr import last_online


@Client.on_message(
    filters.command(["whois", "info"], COMMAND_HAND_LER) &
    f_onw_fliter
)
async def who_is(client, message):
    """ extract user information """
    status_message = await message.reply_text(
        "Wait Bro Let Me Check π"
    )
    from_user = None
    from_user_id, _ = extract_user(message)
    try:
        from_user = await client.get_users(from_user_id)
    except Exception as error:
        await status_message.edit(str(error))
        return
    if from_user is None:
        await status_message.edit("no valid user_id / message specified")
        return
    
    first_name = from_user.first_name or ""
    last_name = from_user.last_name or ""
    username = from_user.username or ""
    
    message_out_str = (
        "<b>αβΊ π½π°πΌπ΄ :</b> "
        f"<a href='tg://user?id={from_user.id}'>{first_name}</a>\n"
        f"<b>αβΊ πππ΅π΅πΈπ :</b> {last_name}\n"
        f"<b>αβΊ πππ΄ππ½π°πΌπ΄ :</b> @{username}\n"
        f"<b>αβΊ πππ΄π πΈπ³ :</b> <code>{from_user.id}</code>\n"
        f"<b>αβΊ πππ΄π π»πΈπ½πΊ :</b> {from_user.mention}\n" if from_user.username else ""
        f"<b>αβΊ πΈπ π°π²π²πΎππ½π π³π΄π»π΄ππ΄π³ :</b> True\n" if from_user.is_deleted else ""
        f"<b>αβΊ πΈπ ππ΄ππΈπ΅πΈπ΄π³ :</b> True" if from_user.is_verified else ""
        f"<b>αβΊ πΈπ ππ²π°πΌ :</b> True" if from_user.is_scam else ""
        # f"<b>Is Fake:</b> True" if from_user.is_fake else ""
        f"<b>αβΊ π»π°ππ ππ΄π΄π½ :</b> <code>{last_online(from_user)}</code>\n\n"
    )

    if message.chat.type in [enums.ChatType.SUPERGROUP, enums.ChatType.CHANNEL]:
        try:
            chat_member_p = await message.chat.get_member(from_user.id)
            joined_date = datetime.fromtimestamp(
                chat_member_p.joined_date or time.time()
            ).strftime("%Y.%m.%d %H:%M:%S")
            message_out_str += (
                "<b>Joined on:</b> <code>"
                f"{joined_date}"
                "</code>\n"
            )
        except UserNotParticipant:
            pass
    chat_photo = from_user.photo
    if chat_photo:
        local_user_photo = await client.download_media(
            message=chat_photo.big_file_id
        )
        await message.reply_photo(
            photo=local_user_photo,
            quote=True,
            caption=message_out_str,
            disable_notification=True
        )
        os.remove(local_user_photo)
    else:
        await message.reply_text(
            text=message_out_str,
            quote=True,
            disable_notification=True
        )
    await status_message.delete()

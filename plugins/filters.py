#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @trojanzhex


import re
import pyrogram

from pyrogram import (
    filters,
    Client
)

from pyrogram.types import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    Message,
    CallbackQuery,
)

from bot import Bot
from script import script
from database.mdb import searchquery
from plugins.channel import deleteallfilters
from config import AUTH_USERS

BUTTONS = {}

@Client.on_message(filters.group & filters.text)
async def filter(client: Bot, message: Message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return

    if 2 < len(message.text) < 50:    
        btn = []

        group_id = message.chat.id
        name = message.text

        filenames, links = await searchquery(group_id, name)
        if filenames and links:
            for filename, link in zip(filenames, links):
                btn.append(
                    [InlineKeyboardButton(text=f"๐น {filename}",url=f"{link}")]
            )
           
        else:
            return

        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"๐น {message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="๐ฐ Pages 1/1 ๐ฐ",callback_data="pages")]
            )
            buttons.append(
                [InlineKeyboardButton("โ ๏ธแแแบแแแแแบแแฎแแญแฏแแพแญแแบแแผแฎแธ Link Join แแซโ ๏ธ", url="https://t.me/Movie_By_KP/90")]
            )
            buttons.append(
                [InlineKeyboardButton("โฃ๏ธ VIP All Series โฃ๏ธ", url="https://t.me/Kpautoreply_bot")]
            )
            await message.reply_text(
                f"<b> Hello {message.from_user.mention}</b>\n\n<b>แแแบแแพแฌแแฌ ๐๐ป {message.text} ๐๐ป  แ แแปแแฑแฌแบแแพแฌแแฝแฑแทแแฌแแผแแฑแธแแฌแธแแซแแแบแแแบแแปแฌ โบ๏ธ ......</b>\n\n<b>Request by :{message.from_user.mention}</b>\n\n<b>Join Main Channel \nK-Series๐๐ป @MKSVIPLINK \n  Movie  ๐๐ป@KPMOVIELIST</b>",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="NEXT โฉ",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"๐ฐ Pages 1/{data['total']} ๐ฐ",callback_data="pages")]
        )
        buttons.append(
            [InlineKeyboardButton("โ ๏ธแแแบแแแแแบแแฎแแญแฏแแพแญแแบแแผแฎแธ Link Join แแซโ ๏ธ", url="https://t.me/Movie_By_KP/90")]
        )
        buttons.append(
            [InlineKeyboardButton("โฃ๏ธ VIP All Series โฃ๏ธ", url="https://t.me/Kpautoreply_bot")]
        )

        await message.reply_text(
                f"<b>Hello {message.from_user.mention}</b>\n\n<b>แแแบแแพแฌแแฌ ๐๐ป {message.text} ๐๐ป  แ แแปแแฑแฌแบแแพแฌแแฝแฑแทแแฌแแผแแฑแธแแฌแธแแซแแแบแแแบแแปแฌ โบ๏ธ ......</b>\n\n<b>Request by :{message.from_user.mention}</b>\n\n<b>Join Main Channel \nK-Series๐๐ป @MKSVIPLINK \n  Movie  ๐๐ป@KPMOVIELIST</b>",
                reply_markup=InlineKeyboardMarkup(buttons)
            )    


@Client.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    clicked = query.from_user.id
    typed = query.message.reply_to_message.from_user.id

    if (clicked == typed) or (clicked in AUTH_USERS):

        if query.data.startswith("next"):
            await query.answer()
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("แแแบแแแบ แแปแฝแแบแฏแแบแ แแแบแแฑแทแแปแบแแฑแฌแแบแธแแปแฌแธแแฒแแพ แแแบแแฏแกแแฝแแบ แแแบแธแแญแฏ แกแแฏแถแธแแผแฏแแฑแแแบแ แแปแฑแธแแฐแธแแผแฏแ แแฑแฌแแบแธแแญแฏแแปแแบแแญแฏ แแแบแแถแแฑแธแแญแฏแทแแซแ",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("โช BACK", callback_data=f"back_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"๐ฐ Pages {int(index)+2}/{data['total']} ๐ฐ", callback_data="pages")]
                )
                buttons.append(
                    [InlineKeyboardButton("โ ๏ธแแแบแแแแแบแแฎแแญแฏแแพแญแแบแแผแฎแธ Link Join แแซโ ๏ธ", url="https://t.me/Movie_By_KP/90")]
                )
                buttons.append(
                    [InlineKeyboardButton("โฃ๏ธ VIP All Series โฃ๏ธ", url="https://t.me/Kpautoreply_bot")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("โช BACK", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("NEXT โฉ", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"๐ฐ Pages {int(index)+2}/{data['total']} ๐ฐ", callback_data="pages")]
                )
                buttons.append(
                    [InlineKeyboardButton("โ ๏ธแแแบแแแแแบแแฎแแญแฏแแพแญแแบแแผแฎแธ Link Join แแซโ ๏ธ", url="https://t.me/Movie_By_KP/90")]
                )
                buttons.append(
                    [InlineKeyboardButton("โฃ๏ธ VIP All Series โฃ๏ธ", url="https://t.me/Kpautoreply_bot")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("back"):
            await query.answer()
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("แแแบแแแบ แแปแฝแแบแฏแแบแ แแแบแแฑแทแแปแบแแฑแฌแแบแธแแปแฌแธแแฒแแพ แแแบแแฏแกแแฝแแบ แแแบแธแแญแฏ แกแแฏแถแธแแผแฏแแฑแแแบแ แแปแฑแธแแฐแธแแผแฏแ แแฑแฌแแบแธแแญแฏแแปแแบแแญแฏ แแแบแแถแแฑแธแแญแฏแทแแซแ.",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("NEXT โฉ", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"๐ฐ Pages {int(index)}/{data['total']} ๐ฐ", callback_data="pages")]
                )
                buttons.append(
                    [InlineKeyboardButton("โ ๏ธแแแบแแแแแบแแฎแแญแฏแแพแญแแบแแผแฎแธ Link Join แแซโ ๏ธ", url="https://t.me/Movie_By_KP/90")]
                )
                buttons.append(
                    [InlineKeyboardButton("โฃ๏ธ VIP All Series โฃ๏ธ", url="https://t.me/Kpautoreply_bot")]
                )
  
                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("โช BACK", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("NEXT โฉ", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"๐ฐ Pages {int(index)}/{data['total']} ๐ฐ", callback_data="pages")]
                )
                buttons.append(
                    [InlineKeyboardButton("โ ๏ธแแแบแแแแแบแแฎแแญแฏแแพแญแแบแแผแฎแธ Link Join แแซโ ๏ธ", url="https://t.me/Movie_By_KP/90")]
                )
                buttons.append(
                    [InlineKeyboardButton("โฃ๏ธ VIP All Series โฃ๏ธ", url="https://t.me/Kpautoreply_bot")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data == "pages":
            await query.answer()


        elif query.data == "start_data":
            await query.answer()
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("HELP", callback_data="help_data"),
                    InlineKeyboardButton("ABOUT", callback_data="about_data")],
                [InlineKeyboardButton("โฃ๏ธ JOIN MAIN CHANNEL โฃ๏ธ ", url="https://t.me/MKSVIPLINK")]
            ])

            await query.message.edit_text(
                script.START_MSG.format(query.from_user.mention),
                reply_markup=keyboard,
                disable_web_page_preview=True
            )


        elif query.data == "help_data":
            await query.answer()
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("BACK", callback_data="start_data"),
                    InlineKeyboardButton("ABOUT ", callback_data="about_data")],
                [InlineKeyboardButton("โฃ๏ธ SUPPORT โฃ๏ธ", url="https://t.me/MKS_RequestGroup")]
            ])

            await query.message.edit_text(
                script.HELP_MSG,
                reply_markup=keyboard,
                disable_web_page_preview=True
            )


        elif query.data == "about_data":
            await query.answer()
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("BACK", callback_data="help_data"),
                    InlineKeyboardButton("START", callback_data="start_data")],
                [InlineKeyboardButton(" โฃ๏ธ SOURCE CODE โฃ๏ธ", url="https://t.me/kopaing15")]
            ])

            await query.message.edit_text(
                script.ABOUT_MSG,
                reply_markup=keyboard,
                disable_web_page_preview=True
            )


        elif query.data == "delallconfirm":
            await query.message.delete()
            await deleteallfilters(client, query.message)
        
        elif query.data == "delallcancel":
            await query.message.reply_to_message.delete()
            await query.message.delete()

    else:
        await query.answer("แกแฒแแซ แแแบแธแกแแฝแแบแแแฏแแบแแฐแธแ!!",show_alert=True)


def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]  

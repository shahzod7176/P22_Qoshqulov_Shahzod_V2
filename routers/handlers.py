from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.types import Message

from config.config import database

main_router = Router()


def write_to_db(message, username):
    messages_ = database["messages"]
    messages_.append(message)
    database["messages"] = messages_
    users = database['users']
    if not users.get(username):
        users[username] = []
    users[username].append(message)
    database['users'] = users



@main_router.message(Command(commands='msg'))
async def len_msg(message: Message):
    msg = f'Gruppada yozilgan xabarlar soni: {len(database["messages"])}'
    await message.answer(msg)
    if message.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
        write_to_db(message.text, message.from_user.username)
        write_to_db(msg, "P22_Qo'shqulov_Shahzod bot")


@main_router.message(F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}))
async def messages(message: Message):
    msg = message.text.split(' @')
    if len(msg) == 2 and msg[0] == 'user msg' and database["users"].get(msg[1]):
        msg = f'@{msg[1]} ga tegishli xabarlar soni {len(database["users"][msg[-1]])}'
        await message.answer(msg)
        write_to_db(msg, "P22_Qo'shqulov_Shahzod bot")
    write_to_db(message.text, message.from_user.username)

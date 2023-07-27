from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram import Router

from app.services.db_service import new_sub, del_sub, get_subs




base_handler = Router()


@base_handler.message(Command('start'))
async def start(message: Message):
	await message.answer('Привет, чтобы видеть уведомления в чате введи `/sub`\nА чтобы больше ничего не видеть `/unsub`', parse_mode='markdown')


@base_handler.message(Command('sub'))
async def sub(message: Message):
	id_ = str(message.chat.id)
	if id_ not in get_subs():
		new_sub(id_)
		await message.answer('Теперь в этот чат будут приходить уведомления.')

	else:
		await message.answer('В этот чат уже приходят уведомления.')


@base_handler.message(Command('unsub'))
async def unsub(message: Message):
	id_ = str(message.chat.id)
	if id_ in get_subs():
		del_sub(str(message.chat.id))
		await message.answer('В этот чат больше не будут приходить уведомления.')

	else:
		await message.answer('В этот чат и до этого ничего не приходило.')
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram import Router

from app.services.db_service import Repo_interface




base_handler = Router()


@base_handler.message(Command('start'))
async def start(message: Message, repo: Repo_interface):
	await message.answer('Привет, чтобы видеть уведомления в чате введи `/sub`\nА чтобы больше ничего не видеть `/unsub`', parse_mode='markdown')


@base_handler.message(Command('sub'))
async def sub(message: Message, repo: Repo_interface):
	id_ = str(message.chat.id)

	if not await repo.has_sub(id_):
		await repo.new_sub(id_)
		await message.answer('Теперь в этот чат будут приходить уведомления.')

	else:
		await message.answer('В этот чат уже приходят уведомления.')


@base_handler.message(Command('unsub'))
async def unsub(message: Message, repo: Repo_interface):
	id_ = str(message.chat.id)

	if await repo.has_sub(id_):
		await repo.del_sub(str(message.chat.id))
		await message.answer('В этот чат больше не будут приходить уведомления.')

	else:
		await message.answer('В этот чат и до этого ничего не приходили уведомления.')
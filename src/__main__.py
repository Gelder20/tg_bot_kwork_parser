from asyncio import run, TaskGroup, get_event_loop
from aiogram import Dispatcher

from config import load_config
from kwork_parser import KworkParser
from cli import cli
from main_router import router
from scheduler import scheduler
from bot import Bot




@cli
async def main():
	#TODO перенести создание бота отсюда
	config = load_config("config.ini")
	bot = Bot(token=config.bot.token)
	dp = Dispatcher()
	dp.include_router(router)
	parser = KworkParser.create()
	
	try:
		async with TaskGroup() as tg:
			tg.create_task(dp.start_polling(bot))
			tg.create_task(scheduler(bot, parser))

	finally:
		await dp.storage.close()
		await bot.session.close()
		await parser.close()


if __name__ == '__main__':
	run(main())
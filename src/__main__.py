from asyncio import run, TaskGroup, get_event_loop
from aiogram import Dispatcher

from kwork_parser import KworkParser
from cli import cli
from main_router import router
from scheduler import scheduler
from bot import Bot




@cli
async def main():
	bot = Bot(token='TOKEN')
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
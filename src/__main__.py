from asyncio import run, TaskGroup, get_event_loop

from app.config import load_config
from app.services.kwork_parser_service import KworkParser
from app.cli import cli
from app.scheduler import scheduler
from app.tgbot import Bot, Dispatcher




@cli
async def main():
	config = load_config("config.ini")
	bot = Bot(token=config.bot.token)
	dp = Dispatcher.create()
	parser = KworkParser.create()
	
	try:
		async with TaskGroup() as tg:
			tg.create_task(dp.start_polling(bot))
			tg.create_task(scheduler(bot, parser))
			pass

	finally:
		await dp.storage.close()
		await bot.session.close()
		await parser.close()


if __name__ == '__main__':
	run(main())
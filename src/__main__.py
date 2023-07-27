from asyncio import run, TaskGroup, get_event_loop
from asyncpg import connect
from dataclasses import asdict

from app.config import load_config
from app.services.kwork_parser_service import KworkParser
from app.services.db_service import Repo_psql
from app.cli import cli
from app.scheduler import scheduler
from app.tgbot import Bot, Dispatcher




@cli
async def main():
	config = load_config("config.ini")
	bot = Bot(token=config.bot.token)
	repo = Repo_psql(await connect(**asdict(config.db)))
	dp = Dispatcher.create(repo=repo)
	parser = KworkParser.create(repo)
	
	try:
		async with TaskGroup() as tg:
			tg.create_task(dp.start_polling(bot))
			tg.create_task(scheduler(bot, parser, repo))
			pass

	finally:
		await dp.storage.close()
		await bot.session.close()
		await parser.close()
		await repo.conn.close()


if __name__ == '__main__':
	run(main())
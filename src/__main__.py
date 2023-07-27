from asyncio import run, TaskGroup, get_event_loop
from asyncpg import create_pool
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
	pool = await create_pool(
		min_size=3,
		max_size=10,
		user=config.db.user,
		password=config.db.password,
		database=config.db.database,
		host=config.db.host,
	)
	bot = Bot(token=config.bot.token)
	dp = Dispatcher.create(pool)
	parser = KworkParser.create(Repo_psql(await pool.acquire()))
	scheduler_repo = Repo_psql(await pool.acquire())
	try:
		async with TaskGroup() as tg:
			tg.create_task(dp.start_polling(bot))
			tg.create_task(scheduler(bot, parser, scheduler_repo))
			pass

	finally:
		await dp.storage.close()
		await bot.session.close()
		await parser.close()
		await pool.release(parser.repo.conn)
		await pool.release(scheduler_repo.conn)
		await pool.close()


if __name__ == '__main__':
	run(main())
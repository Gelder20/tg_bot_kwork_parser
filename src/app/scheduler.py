from asyncio import sleep, timeout
from aiogram.exceptions import TelegramRetryAfter, TelegramBadRequest
from app.services.db_service import Repo_interface


async def scheduler(bot, parser, repo: Repo_interface, delay: int | float = 10):
	while True:
		try:
			async with timeout(60) as cm:
				views = await parser.parse()

		except TimeoutError:
			print('TimeoutError in scheduler when get views')

			await parser.close()
			print('Parser closed')

			parser = parser.create()
			print('New parser created')

			continue

		while views: # it is assumed that views is much smaller than get_subs()
			# the mailing list may be delayed if there are a lot of chats,
			# so after each order, new subs are received
			for chat_id in map(lambda record: record['id'], await repo.get_subs()):
				try:
					await bot.send_order(chat_id, views[0])

				except TelegramRetryAfter as e:
					await sleep(e.retry_after)

				except TelegramBadRequest as e:
					if e.message == 'Bad Request: chat not found':
						pass

					else:
						print(f'Error in mailing (1):\n{repr(e)}\n{e}')

				except Exception as e:
					print(f'Error in mailing (2):\n{repr(e)}\n{e}')

			del views[0]

			await sleep(0.8)
		await sleep(delay)

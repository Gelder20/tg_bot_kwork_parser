from .scheduler import scheduler
from .services.interfaces import IOrdersParser, IOrdersSendingRepo, IUIForOrdersSending
from .services.data_objects import Order


class NewOrdersSending:
	parser: IOrdersParser
	repo: IOrdersSendingRepo
	UI: IUIForOrdersSending

	def __init__(self, parser: IOrdersParser, repo: IOrdersSendingRepo, UI: IUIForOrdersSending):
		self.parser = parser
		self.repo = repo
		self.UI = UI

	@scheduler(10)
	async def send_orders():
		try:
			async with timeout(60) as cm:
				orders = await self.parser.get_new_orders_ids()

		except TimeoutError:
			print('Can not get orders')


		for i in orders: 
			if await self.repo.has_order(i):
				continue
			else:
				await self.repo.new_order(i)

			for chat_id in await self.repo.get_subs():
				try:
					await self.UI.send_order(chat_id, views[0])

				except TelegramRetryAfter as e:
					await sleep(e.retry_after)

				except TelegramBadRequest as e:
					if e.message == 'Bad Request: chat not found':
						pass

					else:
						print(f'Error in mailing (1):\n{repr(e)}\n{e}')

				except Exception as e:
					print(f'Error in mailing (2):\n{repr(e)}\n{e}')

			await sleep(0.8)

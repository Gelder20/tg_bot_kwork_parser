from aiohttp import ClientSession
from aiohttp.web import HTTPError

from asyncio import run
from json import loads
from concurrent.futures import ThreadPoolExecutor
from collections import namedtuple


import warnings # no idea why this class is not recommended to inherit
# the github says something like "there is no full backward compatibility", but I don't override the parent methods...
warnings.filterwarnings('ignore', message='Inheritance class KworkParser from ClientSession is discouraged')


from services.db_service import get_orders, new_order




OrderView = namedtuple('OrderView', 'message, url')


class KworkParser(ClientSession):
	executor: ThreadPoolExecutor = None


	@classmethod
	def create(cls, base_url='https://kwork.ru', *args, **kwargs):
		self = cls(base_url, *args, **kwargs)
		self.executor = ThreadPoolExecutor(max_workers=2)
		return self


	async def parse(self):
		async with self.get('/projects?c=41&attr=3587') as response:
			if response.status != 200:
				raise HTTPError("Request attempt to '/projects?c=41&attr=3587' failed")

			html = await response.text()

		# I think there is nothing wrong with _, because this class is the heir
		payload = await self.connector._loop.run_in_executor(self.executor, self.get_payload, html)
		
		old_orders = get_orders()

		views = []
		for order in payload:
			if order['id'] not in old_orders:
				new_order(order['id'])
				views.append(await self.connector._loop.run_in_executor(self.executor, self.get_order_view, order))

		return views

	@staticmethod
	def get_payload(html: str):
		return loads(
			html.split('\n')[39].split('window.stateData=')[1].split('</script>')[0][:-1]
		)['wantsListData']['pagination']['data']


	@staticmethod
	def get_order_view(order: dict):
		view = []

		view.append(f"{order['name']}")

		price = int(float(order['price_limit']))
		if order['allow_higher_price']:
			view.append(f'Желаемый бюджет: до {price}')
			view.append(f'Допустимый: до {price*3}')
		else:
			view.append(f'Цена: до {price}')

		view.append(f'Откликов на момент поста: {order["kwork_count"]}\n')

		view.append(order['desc'])

		return OrderView(('\n').join(view), f"https://kwork.ru/projects/{order['id']}/view")


	# here I slightly redefined the parent method, but I didn't change its logic a bit
	def close(self, *args, **kwargs):
		response = super().close(*args, **kwargs)
		self.executor.shutdown()
		return response


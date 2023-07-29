import warnings
warnings.simplefilter('default')


from aiohttp import ClientSession
from aiohttp.web import HTTPError
from bs4 import BeautifulSoup

from json import loads
from concurrent.futures import Executor
from asyncio import get_event_loop, AbstractEventLoop


from ..data_objects import Order
from ..interfaces import IOrdersParser




class _KworkParserBase:
	session: ClientSession = None
	executor: Executor = None
	loop: AbstractEventLoop = None


	def __init__(self, *, _session: ClientSession = None, loop: AbstractEventLoop = None, executor: Executor = None) -> None:
		if not executor:
			warnings.warn('\nIt is recommended to pass executor for more control and guarantee resource consumption', ResourceWarning)
		self.executor = executor

		self.loop = loop if loop else get_event_loop()

		# Important: you should initialize session last, that in case of an initialization error,
		# the created session does not remain incomplete
		if _session is not None and _session._base_url != 'https://kwork.ru':
			raise ValueError("base_url in ClientSession must be 'https://kwork.ru'")

		else:
			_session = ClientSession('https://kwork.ru')

		self.session = _session

	async def close(self, *args, **kwargs) -> None:
		if self.executor:
			self.executor.shutdown()

		await self.session.close(*args, **kwargs)


class KworkParserGetOrders(_KworkParserBase):
	async def get_order_by_id(self, id_) -> Order:
		async with self.session.get(f'/projects/{id_}/view') as response:
			html = await response.text()

		payload = (await self.loop.run_in_executor(self.executor, self.get_order_data, html))['want']

		return Order(
			id_=id_,
			name=payload['name'],
			allow_higher_price=payload['allow_higher_price'],
			price_limit=payload['price_limit'],
			responces_count=payload['kwork_count'],
			desc=payload['desc'],
		)


	@staticmethod
	def get_order_data(html) -> dict:
		soup = BeautifulSoup(html, 'lxml')
		data = soup.find_all('script')[49].text

		return loads(data[16:data.rfind(';window.usersPortfolioCategories')])


class KworkParserNewOrders(_KworkParserBase):
	async def get_new_orders_ids(self) -> tuple[int, ...]:
		async with self.session.get('/projects?c=41&attr=3587') as response:
			if response.status != 200:
				raise HTTPError("Request attempt to '/projects?c=41&attr=3587' failed")

			html = await response.text()

		data = await self.loop.run_in_executor(self.executor, self.get_new_orders_data, html)
		return tuple(map(lambda x: x['id'], data))


	@staticmethod
	def get_new_orders_data(html: str) -> dict:
		data = BeautifulSoup(html, 'lxml').find_all('script')[11].text
		return loads(
			data[data.find('window.stateData=') + 17:-1]
		)['wantsListData']['pagination']['data']


class KworkCategories(_KworkParserBase):
	async def get_categories(self):
		async with self.session.get('/projects') as response:
			html = await response.text()

		data = await self.loop.run_in_executor(self.executor, self.get_categories_data, html)
		
		for category in data.values():
			print(category['CATID'], category['name'])
			for cat in category['cats']:
				print('---', cat['CATID'], cat['name'])
				attributes = cat.get('attributes')
				if attributes:
					for attr in attributes.values():
						print('   ', '-', attr['id'], attr['title'])


	@staticmethod
	def get_categories_data(html):
		data = BeautifulSoup(html, 'lxml').find_all('script')[11].text
		return loads(
			data[data.find('window.stateData=') + 17:-1]
		)['categoriesWithFavoritesList']



class KworkParser(
	KworkParserGetOrders,
	KworkParserNewOrders,
	IOrdersParser,
): pass



if __name__ == '__main__':
	from asyncio import run


	async def main():
		parser = KworkCategories()
		try:
			# ids = await parser.parse()
			# for id in ids:
				# print(await parser.render(id))
			# print(await parser.render(2132309))
			# print(await parser.get_categories())
			pass
		finally:
			await parser.close()


	run(main())
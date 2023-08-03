from json import loads
from concurrent.futures import Executor
from asyncio import get_event_loop, AbstractEventLoop, timeout

from aiohttp import ClientSession
from aiohttp.web import HTTPError
from bs4 import BeautifulSoup

from ..data_objects import Order
from ..interfaces import IOrdersParser




class _KworkParserBase:
	session: ClientSession = None
	executor: Executor = None
	loop: AbstractEventLoop = None


	def __init__(self, session: ClientSession, loop: AbstractEventLoop = None, executor: Executor = None) -> None:
		self.session = session
		self.executor = executor
		self.loop = loop if loop else get_event_loop()


	async def close(self, *args, **kwargs) -> None:
		response = self.session.close(*args, **kwargs)
		if self.executor:
			self.executor.shutdown()

		await response


class KworkParserGetOrders(_KworkParserBase):
	async def get_order_by_id(self, id_) -> Order:
		order = None
		try:
			async with timeout(60) as cm:
				async with self.session.get(f'/projects/{id_}/view') as response:
					html = await response.text()
		
				payload = (await self.loop.run_in_executor(self.executor, self.get_order_data, html))['want']

			order = Order(
				id_=id_,
				name=payload['name'],
				allow_higher_price=payload['allow_higher_price'],
				price_limit=payload['price_limit'],
				responces_count=payload['kwork_count'],
				desc=payload['desc'],
			)

		except Exception as e:
			print(f'Can not get order by ID: {e}')

		return order



	@staticmethod
	def get_order_data(html) -> dict:
		soup = BeautifulSoup(html, 'lxml')
		data = soup.find_all('script')[49].text

		return loads(data[16:data.rfind(';window.usersPortfolioCategories')])


class KworkParserNewOrders(_KworkParserBase):
	async def get_new_orders_ids(self) -> tuple[int, ...]:
		orders_ids = tuple()
		
		try:
			async with timeout(60) as cm:
				async with self.session.get('/projects?c=41&attr=3587') as response:
					if response.status != 200:
						raise HTTPError("Request attempt to '/projects?c=41&attr=3587' failed")

					html = await response.text()

				data = await self.loop.run_in_executor(self.executor, self.get_new_orders_data, html)
				orders_ids = tuple(map(lambda x: x['id'], data))


		except Exception as e:
			print(f'Can not get orders: {e}')

		return orders_ids


	@staticmethod
	def get_new_orders_data(html: str) -> dict:
		data = BeautifulSoup(html, 'lxml').find_all('script')[11].text
		return loads(
			data[data.find('window.stateData=') + 17:-1]
		)['wantsListData']['pagination']['data']


class KworkParser(
	KworkParserGetOrders,
	KworkParserNewOrders,
	IOrdersParser,
): pass



if __name__ == '__main__':
	from asyncio import run


	async def main():
		parser = KworkParser(ClientSession('https://kwork.ru'))
		try:
			# ids = await parser.parse()
			# for id in ids:
				# print(await parser.render(id))
			print(await parser.render(2132309))

		finally:
			await parser.close()


	run(main())
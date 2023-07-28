from aiohttp import ClientSession
from aiohttp.web import HTTPError
from bs4 import BeautifulSoup
from jinja2 import Environment

from json import loads
from concurrent.futures import Executor
from asyncio import get_event_loop, AbstractEventLoop




__env = Environment(enable_async=True)
_template = __env.from_string(
"""{{ name }}{% if allow_higher_price %}
Желаемая цена: до {{ to_int(price_limit) }}
Допустимый бюджет: до {{ to_int(price_limit) * 3 }}{% else %}
Цена: до {{ to_int(price_limit) }}{% endif %}
Откликов на данный момент: {{ kwork_count }}

{{ desc }}
"""
)


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
	template = None


	def __init__(self, *args, template=None, **kwargs) -> None:
		super().__init__(*args, **kwargs)
		self.template = template if template else _template


	async def render(self, id_) -> tuple[str, str]:
		async with self.session.get(f'/projects/{id_}/view') as response:
			html = await response.text()

		payload = await self.loop.run_in_executor(self.executor, self.get_order_data, html)
		return await _template.render_async(**payload['want'], to_int=lambda x: int(float(x)))


	@staticmethod
	def get_order_data(html) -> dict:
		soup = BeautifulSoup(html, 'lxml')
		data = soup.find_all('script')[49].text

		return loads(data[16:data.rfind(';window.usersPortfolioCategories')])


class KworkParserNewOrders(_KworkParserBase):
	async def parse(self) -> tuple[int, ...]:
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

	@staticmethod
	def get_categories_data(html):
		data = BeautifulSoup(html, 'lxml').find_all('script')[11].text
		return loads(
			data[data.find('window.stateData=') + 17:-1]
		)['categoriesWithFavoritesList']



class KworkParser(
	KworkParserGetOrders,
	KworkParserNewOrders,
): pass



if __name__ == '__main__':
	from asyncio import run


	async def main():
		parser = KworkCategories(ClientSession('https://kwork.ru'))
		try:
			# ids = await parser.parse()
			# for id in ids:
				# print(await parser.render(id))
			# print(await parser.render(2132309))
			print(await parser.get_categories())

		finally:
			await parser.close()


	run(main())
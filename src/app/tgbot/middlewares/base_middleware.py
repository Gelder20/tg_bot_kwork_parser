from abc import abstractmethod
from aiogram import BaseMiddleware




class MyMiddleware(BaseMiddleware):
	async def __call__(self, /, handler, event, data):
		response = await self.pre_process(handler, event, data)

		if response is None: return

		result = await handler(event, data)
		await self.post_process(handler, event, data, result)

		return result


	@abstractmethod
	async def pre_process(self, /, handler, event, data): pass

	@abstractmethod
	async def post_process(self, /, handler, event, data, result): pass
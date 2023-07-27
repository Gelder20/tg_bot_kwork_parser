from aiogram import Dispatcher as _Dispatcher

from .middlewares import DbMiddleware
from .handlers import routers




class Dispatcher(_Dispatcher):
	@classmethod
	def create(cls, pool, *args, **kwargs):
		self = cls(*args, **kwargs)
		self.message.middleware(DbMiddleware(pool))
		self.include_routers(*routers)

		return self


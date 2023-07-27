from aiogram import Dispatcher as _Dispatcher

from .handlers import routers




class Dispatcher(_Dispatcher):
	@classmethod
	def create(cls, *args, **kwargs):
		self = cls(*args, **kwargs)
		self.include_routers(*routers)

		return self



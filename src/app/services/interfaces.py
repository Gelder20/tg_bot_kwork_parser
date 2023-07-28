from abc import ABC, abstractmethod

from .data_objects import Order


class IOrdersParser(ABC):

	@abstractmethod
	async def get_new_orders_ids(self) -> tuple[int, ...]: pass

	@abstractmethod
	async def get_order_by_id(self, id: int) -> Order: pass


class IUIForOrdersSending(ABC):

	@abstractmethod
	async def send_order(self, id: str, order: Order): pass


class IOrdersSendingRepo(ABC):

	@abstractmethod
	async def new_order(self, /, id_: int) -> None: pass

	@abstractmethod
	async def has_order(self, /, id_: int) -> bool: pass

	@abstractmethod
	async def get_subs(self, /) -> tuple[str, ...]: pass

from asyncpg import Connection
from abc import ABC, abstractmethod

from ..interfaces import IOrdersSendingRepo




class Repo_interface(ABC):
	# TODO: add DTO signatures
	@abstractmethod
	async def init(self) -> None: pass

	@abstractmethod
	async def get_orders(self, /) -> tuple[int, ...]: pass

	@abstractmethod
	async def new_order(self, /, id_: int) -> None: pass

	@abstractmethod
	async def has_order(self, /, pk: int) -> bool: pass

	@abstractmethod
	async def get_subs(self, /) -> tuple[str, ...]: pass

	@abstractmethod
	async def new_sub(self, /, id_: str) -> None: pass

	@abstractmethod
	async def del_sub(self, /, id_: str) -> None: pass

	@abstractmethod
	async def has_sub(self, /, pk: int) -> bool: pass


class Repo_psql(Repo_interface, IOrdersSendingRepo):
	conn: Connection = None


	def __init__(self, conn):
		self.conn = conn


	async def init(self) -> None:
		await self.conn.execute("""
			CREATE TABLE IF NOT EXISTS subs (
				id varchar(25) PRIMARY KEY
			);
			CREATE TABLE IF NOT EXISTS orders (
				id INT PRIMARY KEY
			);
		""")


	async def get_orders(self, /) -> list[dict['id': int], ...]:
		return await self.conn.fetch("""
			SELECT * FROM orders;
		""")


	async def new_order(self, /, id_: int) -> None:
		await self.conn.execute("""
			INSERT INTO orders
			VALUES ($1);
		""", id_)


	async def has_order(self, /, pk: int) -> bool:
		return await self.conn.fetchval("SELECT EXISTS (SELECT * FROM orders WHERE id = $1)", pk)


	async def get_subs(self, /) -> map:
		return map(lambda x: x['id'], await self.conn.fetch("""
			SELECT * FROM subs;
		"""))


	async def new_sub(self, /, id_: str) -> None:
		await self.conn.execute("""
			INSERT INTO subs
			VALUES ($1);
		""", id_)

	async def del_sub(self, /, id_: str) -> None:
		await self.conn.execute("""
			DELETE FROM subs
			WHERE id = $1;
		""", id_)

	async def has_sub(self, /, pk: int) -> bool:
		return await self.conn.fetchval("SELECT EXISTS (SELECT * FROM subs WHERE id = $1)", pk)




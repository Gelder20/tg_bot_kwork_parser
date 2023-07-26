from asyncpg import Connection
from abc import ABC, abstractmethod




class Repo_interface(ABC):
	# TODO: add DTO signatures
	@abstractmethod
	async def init(self) -> None: pass

	@abstractmethod
	async def get_orders(self, /) -> tuple[int, ...]: pass

	@abstractmethod
	async def new_order(self, /, id_: int) -> None: pass

	@abstractmethod
	async def get_subs(self, /) -> tuple[str, ...]: pass

	@abstractmethod
	async def new_sub(self, /, id_: str) -> None: pass

	@abstractmethod
	async def del_sub(self, /, id_: str) -> None: pass


class Repo_psql(Repo_interface):
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


	async def get_subs(self, /) -> tuple[str, ...]:
		return await self.conn.fetch("""
			SELECT * FROM subs;
		""")


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


def get_orders():
	with open('flat_files/old_orders.txt', 'r') as db_file:
		old_orders = tuple(map(lambda x: int(x.strip()), db_file.readlines()))

	return old_orders


def new_order(id_: str):
	with open('flat_files/old_orders.txt', 'r+') as db_file:
		db_file.seek(0, 2)
		print(id_, file=db_file)


def get_subs():
	with open('flat_files/subs.txt', 'r') as db_file:
		subs = tuple(map(lambda x: x.strip(), db_file.readlines()))

	return subs


def new_sub(id_: str):
	with open('flat_files/subs.txt', 'r+') as db_file:
		db_file.seek(0, 2)
		print(id_, file=db_file)


def del_sub(id_: str):
	with open('flat_files/subs.txt', encoding='utf-8') as db_file: lines = db_file.readlines()
	with open('flat_files/subs.txt', 'w', encoding='utf-8') as db_file:
		for line in lines:
			if line.strip() != id_:
				db_file.write(line)



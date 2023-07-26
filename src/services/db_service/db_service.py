# TODO: async db_srevies support and connection object with pattern repo


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

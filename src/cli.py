from asyncio import CancelledError




def cli(func):
	async def wrapper(*args, **kwargs):
		try:
			return await func(*args, **kwargs)
	
		except (KeyboardInterrupt, SystemExit, CancelledError):
			print('Bot stopped successfully!')

		except Exception as e:
			print(f'Bot stopped with an error!\n{repr(e)}\n{e}')
			raise e


	return wrapper
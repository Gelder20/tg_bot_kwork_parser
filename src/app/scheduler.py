from asyncio import sleep, timeout


def scheduler(delay: int | float = 10):

	def decorator(func):
		
		async def wrapper(*args, **kwargs):
	
			while True:
				try:
					await func(*args, **kwargs)
				except Exception as e:
					#TODO убрать заглушку
					print(e)
				await sleep(delay)
		return wrapper
	return decorator
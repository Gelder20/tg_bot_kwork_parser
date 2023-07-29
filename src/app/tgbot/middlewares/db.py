from aiogram import BaseMiddleware
from app.services.db_service import Repo_psql




class DbMiddleware(BaseMiddleware):
    def __init__(self, pool):
        super().__init__()
        self.pool = pool


    async def __call__(self, handler, event, data):
        async with self.pool.acquire() as conn:
            data['repo'] = Repo_psql(conn)
            result = await handler(event, data)

        return result

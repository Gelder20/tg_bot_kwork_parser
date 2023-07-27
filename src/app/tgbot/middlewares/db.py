from .base_middleware import MyMiddleware
from app.services.db_service import Repo_psql




class DbMiddleware(MyMiddleware):
    def __init__(self, pool):
        super().__init__()
        self.pool = pool

    async def pre_process(self, handler, event, data):
        data['repo'] = Repo_psql(await self.pool.acquire())
        return handler


    async def post_process(self, handler, event, data, result):
        await self.pool.release(data['repo'].conn)
        del data['repo']

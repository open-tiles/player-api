import aiomysql
from aiohttp import web


class Player:

    def __init__(self, username):
        self.username = username

    async def create(self, request):

        async with request.app['pool'].acquire() as db_conn:
            data = await request.json()
            name = data['username']
            cursor = await db_conn.cursor(aiomysql.DictCursor)
            query = f'''
            INSERT INTO players (username) VALUES ("{name}")
            '''
            await cursor.execute(query)
            await db_conn.commit()
        return web.Response(text='Player created')

    async def get(self, request):
        player_id = request.rel_url.query['id']
        async with request.app['pool'].acquire() as db_conn:
            query = f'SELECT * FROM players WHERE id = {player_id}'
            cursor = await db_conn.cursor(aiomysql.DictCursor)
            await cursor.execute(query)
            result = await cursor.fetchone()
            data = {
                    'id': result['id'],
                    'username': result['username']
                    }
            return web.json_response(data)

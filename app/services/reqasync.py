from app.log import logger


async def get(url, session, sema):
    async with sema, session.get(url) as response:
        logger.info(f'Acessing {url}')
        return await response.read()


async def post(url, session, data, sema):
    async with sema, session.post(url, data=data) as response:
        return await response.read()

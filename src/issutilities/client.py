import aiohttp


class HTTP:
    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.close()

    async def close(self):
        if not self.session.closed:
            await self.session.close()

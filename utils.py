from collections.abc import Coroutine
from socket import AF_INET
from typing import Optional, Any
import json
import aiohttp

SIZE_POOL_AIOHTTP = 100


class SingletonAiohttp:
    aiohttp_client: Optional[aiohttp.ClientSession] = None

    @classmethod
    def get_aiohttp_client(cls) -> aiohttp.ClientSession:
        if cls.aiohttp_client is None:
            timeout = aiohttp.ClientTimeout(total=2)
            connector = aiohttp.TCPConnector(
                family=AF_INET, limit_per_host=SIZE_POOL_AIOHTTP
            )
            cls.aiohttp_client = aiohttp.ClientSession(
                timeout=timeout, connector=connector
            )

        return cls.aiohttp_client

    @classmethod
    def set_cookie(cls, cookies):
        loose_cookies = []
        for k, v in json.loads(cookies).items():
            loose_cookies.append((k, v))
        cls.aiohttp_client._cookie_jar.update_cookies(cookies=loose_cookies)

    @classmethod
    async def close_aiohttp_client(cls) -> None:
        if cls.aiohttp_client:
            await cls.aiohttp_client.close()
            cls.aiohttp_client = None

    @classmethod
    async def query_url(cls, url: str, data: dict) -> Any:
        client = cls.get_aiohttp_client()

        try:
            async with client.post(url, data) as response:
                if response.status != 200:
                    return {"ERROR OCCURED" + str(await response.text())}

                json_result = await response.json()
        except Exception as e:
            return {"ERROR": e}

        return json_result


async def on_start_up() -> None:
    SingletonAiohttp.get_aiohttp_client()


async def on_shutdown() -> None:
    await SingletonAiohttp.close_aiohttp_client()

import asyncio
import requests


async def get_item(url):
    resposta = requests.get(url)
    print(resposta.text)


async def main():
    endpoint = "http://localhost:8080/api/resenha/"
    calls = [get_item(f"{endpoint}/{id}") for id in range(1, 11)]
    results = await asyncio.gather(*calls)


asyncio.run(main())

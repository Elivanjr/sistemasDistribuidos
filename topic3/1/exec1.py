import asyncio

async def teste():
    await asyncio.sleep(3)
    return "WARNING, WARNING..."

async def main():
    resposta = await teste()
    print(resposta)
    print(type(await teste()))

asyncio.run(main())

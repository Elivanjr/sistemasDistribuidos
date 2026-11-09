import asyncio

async def teste(tempo):
    await asyncio.sleep(tempo)
    return "WARNING, WARNING..."

async def main():
    num = int(input("Tempo de Espera: "))
    resposta = await teste(num)
    print(resposta)

asyncio.run(main())

import asyncio

async def teste():
    print("COMEÇA...")
    await asyncio.sleep(3)
    print("TERMINA...")
    print("SAI...")

async def testeOutro():
    print("COMEÇA DNV..")
    await asyncio.sleep(3)
    print("TERMINA DNV...")
    print("SAI DNV...")

async def main():
    task = asyncio.create_task(teste())
    otherTask = asyncio.create_task(testeOutro())

    await task
    await otherTask

asyncio.run(main())
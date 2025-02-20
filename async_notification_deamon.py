import asyncio

storage = {
    "usersList": [1, 2, 3]
}

async def paraswap_data(bot, user_id, data):
    bot.send_message(user_id, data)

async def jupiter_data(bot, user_id, data):
    bot.send_message(user_id, data)

async def get_data():
    return "Paraswap data", "Jupiter data"

async def process_paraswap_data(bot, user_id, data):
    await paraswap_data(bot, user_id, data)

async def process_jupiter_data(bot, user_id, data):
    await jupiter_data(bot, user_id, data)

async def send(bot):
    if users := storage.get("usersList"):
        paraswap_data_value, jupiter_data_value = await get_data()
        for userID in users:
            await asyncio.gather(
                process_paraswap_data(bot, userID, paraswap_data_value),
                process_jupiter_data(bot, userID, jupiter_data_value)
            )

async def deamon(bot, rpt):
    while True:
        await send(bot)
        await asyncio.sleep(rpt)

async def main():
    bot = lambda: None
    bot.send_message = lambda userID, message: print(f"[{userID}]: {message}")
    rpm = 60 / 40
    await deamon(bot, rpm)
    
    

    
asyncio.run(main())

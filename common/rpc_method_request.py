

async def get_screen_size(server):
    return await server.call("getScreenSize")
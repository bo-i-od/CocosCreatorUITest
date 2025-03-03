from common.ws_server import RPCServer


async def get_screen_size(server: RPCServer):
    return await server.call("getScreenSize")


async def get_position(server: RPCServer, element_data_list: list):
    return await server.call("getPosition", element_data_list)


async def get_position_by_id(server: RPCServer, id_list: list, offspring_path: str,
                             anchor_point: list, locator_camera: str):
    return await server.call("getPositionByID", id_list, offspring_path, anchor_point, locator_camera)


async def get_size(server: RPCServer, element_data_list: list):
    return await server.call("getSize", element_data_list)


async def get_size_by_id(server: RPCServer, id_list: list, offspring_path: str):
    return await server.call("getSizeByID", id_list, offspring_path)


async def get_text(server: RPCServer, element_data_list: list):
    return await server.call("getText", element_data_list)


async def get_text_by_id(server: RPCServer, id_list: list, offspring_path: str):
    return await server.call("getTextByID", id_list, offspring_path)


async def set_text(server: RPCServer, element_data_list: list, text: str):
    return await server.call("setText", element_data_list, text)


async def set_text_by_id(server: RPCServer, id_list: list, offspring_path: str, text: str):
    return await server.call("setTextByID", id_list, offspring_path, text)


async def get_sprite_name(server: RPCServer, element_data_list: list):
    return await server.call("getSpriteName", element_data_list)


async def get_sprite_name_by_id(server: RPCServer, id_list: list, offspring_path: str):
    return await server.call("getSpriteNameByID", id_list, offspring_path)


async def get_progress(server: RPCServer, element_data_list: list):
    return await server.call("getProgress", element_data_list)


async def get_progress_by_id(server: RPCServer, id_list: list, offspring_path: str):
    return await server.call("getProgressByID", id_list, offspring_path)


async def get_toggle_is_checked(server: RPCServer, element_data_list: list):
    return await server.call("getToggleIsChecked", element_data_list)


async def get_toggle_is_checked_by_id(server: RPCServer, id_list: list, offspring_path: str):
    return await server.call("getToggleIsCheckedByID", id_list, offspring_path)


async def get_name(server: RPCServer, element_data_list: list):
    return await server.call("getName", element_data_list)


async def get_name_by_id(server: RPCServer, id_list: list, offspring_path: str):
    return await server.call("getNameByID", id_list, offspring_path)


async def get_id(server: RPCServer, element_data_list: list):
    return await server.call("getID", element_data_list)


async def get_id_by_id(server: RPCServer, id_list: list, offspring_path: str):
    return await server.call("getIDByID", id_list, offspring_path)


async def get_parent_id(server: RPCServer, element_data_list: list):
    return await server.call("getParentID", element_data_list)


async def get_parent_id_by_id(server: RPCServer, id_list: list, offspring_path: str):
    return await server.call("getParentIDByID", id_list, offspring_path)


async def custom_command(server: RPCServer, command_list: list):
    return await server.call("customCommand", command_list)


async def command(server: RPCServer, command_list: list):
    return await server.call("command", command_list)


async def screen_shot(server: RPCServer, x: int, y: int, w: int, h: int):
    return await server.call("screenShot", x, y, w, h)

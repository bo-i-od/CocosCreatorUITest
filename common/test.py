from common import rpc_method_request
from common.ws_server import rpc_server, sleep
from configs.element_data import ElementsData


@rpc_server(port=5101)
async def main(server):
    await rpc_method_request.custom_command(server, command_list=["setCamera Canvas>Camera"])
    position = await rpc_method_request.get_position(server, [ElementsData.Test.button1, ElementsData.Test.button])
    print(f"position: {position}")
    await sleep(5)
    screen_size = await rpc_method_request.get_screen_size(server)
    print(f"Screen size: {screen_size}")


if __name__ == "__main__":
    main()
from common.base_page import BasePage
from common.ws_server import rpc_server, sleep
from configs.element_data import ElementsData


@rpc_server(port=5101)
async def main(server):
    bp = BasePage(window_title="Cocos Creator - NewProject", server=server)
    await bp.initialize()
    await bp.custom_command("setCamera Canvas>Camera")
    position = await bp.get_position_list(element_data_list=[ElementsData.Test.button1, ElementsData.Test.button])
    print(f"position: {position}")
    uuid = await bp.get_id(element_data=ElementsData.Test.button1)
    print(uuid)

    position = await bp.get_position(uuid=uuid)
    print(f"position: {position}")
    # name = await bp.get_name(element_data=ElementsData.Test.button1)
    # print(name)
    await bp.click_until_disappear(element_data=ElementsData.Test.button1)
    # # bp.click_position_base(position=position[1][1])
    # position = await bp.get_position(element_data=ElementsData.Test.toggle)
    # # bp.click_position_base(position=position)
    # await sleep(5)
    # screen_size = await bp.get_screen_size()
    # print(f"Screen size: {screen_size}")


if __name__ == "__main__":
    main()

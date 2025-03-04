from common.base_page import BasePage
from common.ws_server import rpc_server, sleep
from configs.element_data import ElementsData


async def get_screen_size_test(bp: BasePage):
    screen_size = await bp.get_screen_size()
    print(screen_size)


async def exist_test(bp: BasePage):
    print(await bp.exist(element_data=ElementsData.Test.A))
    print(await bp.exist(element_data=ElementsData.Test.B))
    uuid = await bp.get_id(element_data=ElementsData.Test.A)
    print(await bp.exist(uuid=uuid))


async def get_position_test(bp: BasePage):
    print(await bp.get_position(element_data=ElementsData.Test.A))
    # print(await bp.get_parent_id(element_data=ElementsData.Test.B))
    uuid = await bp.get_id(element_data=ElementsData.Test.A)
    print(await bp.get_position(uuid=uuid))


async def get_position_list_test(bp: BasePage):
    print(await bp.get_position_list(element_data_list=[ElementsData.Test.A, ElementsData.Test.B]))
    # print(await bp.get_parent_id(element_data=ElementsData.Test.B))
    uuid = await bp.get_id(element_data=ElementsData.Test.A)
    print(await bp.get_position_list(uuid=uuid, offspring_path="Button1"))
    print(await bp.get_position_list(uuid_list=[uuid, uuid], offspring_path="Button1"))


async def get_size_test(bp: BasePage):
    print(await bp.get_size(element_data=ElementsData.Test.A))
    # print(await bp.get_parent_id(element_data=ElementsData.Test.B))
    uuid = await bp.get_id(element_data=ElementsData.Test.A)
    print(await bp.get_size(uuid=uuid))


async def get_size_list_test(bp: BasePage):
    print(await bp.get_size_list(element_data_list=[ElementsData.Test.A, ElementsData.Test.B]))
    # print(await bp.get_parent_id(element_data=ElementsData.Test.B))
    uuid = await bp.get_id(element_data=ElementsData.Test.A)
    print(await bp.get_size_list(uuid=uuid, offspring_path="Button1"))
    print(await bp.get_size_list(uuid_list=[uuid, uuid], offspring_path="Button1"))


async def get_text_test(bp: BasePage):
    print(await bp.get_text(element_data=ElementsData.Test.button1, offspring_path="Label"))
    # print(await bp.get_parent_id(element_data=ElementsData.Test.B))
    uuid = await bp.get_id(element_data=ElementsData.Test.button2)
    print(await bp.get_text(uuid=uuid, offspring_path="Label"))


async def get_text_list_test(bp: BasePage):
    print(await bp.get_text_list(element_data_list=[ElementsData.Test.button1, ElementsData.Test.B], offspring_path="Label"))
    # print(await bp.get_parent_id(element_data=ElementsData.Test.B))
    uuid = await bp.get_id(element_data=ElementsData.Test.A)
    print(await bp.get_text_list(uuid=uuid, offspring_path="Button2/Label"))
    print(await bp.get_text_list(uuid_list=[uuid, uuid], offspring_path="Button2/Label"))

async def set_text_test(bp: BasePage):
    print(await bp.set_text(element_data=ElementsData.Test.button2, offspring_path="Label", text="ha"))
    # print(await bp.get_parent_id(element_data=ElementsData.Test.B))
    uuid = await bp.get_id(element_data=ElementsData.Test.button2)
    print(await bp.set_text(uuid=uuid, offspring_path="Label", text="456"))


async def set_text_list_test(bp: BasePage):
    # print(await bp.set_text_list(element_data_list=[ElementsData.Test.button2, ElementsData.Test.B], offspring_path="Label", text="789"))
    # print(await bp.get_parent_id(element_data=ElementsData.Test.B))
    uuid = await bp.get_id(element_data=ElementsData.Test.A)
    print(await bp.set_text_list(uuid=uuid, offspring_path="Button2/Label", text="101112"))
    # print(await bp.set_text_list(uuid_list=[uuid, uuid], offspring_path="Button2/Label", text="131415"))


async def get_sprite_name_test(bp: BasePage):
    print(await bp.get_sprite_name(element_data=ElementsData.Test.Sprite, offspring_path=""))
    # print(await bp.get_parent_id(element_data=ElementsData.Test.B))
    uuid = await bp.get_id(element_data=ElementsData.Test.Sprite)
    print(await bp.get_sprite_name(uuid=uuid))


async def get_sprite_name_list_test(bp: BasePage):
    print(await bp.get_sprite_name_list(element_data_list=[ElementsData.Test.Sprite, ElementsData.Test.B]))
    # print(await bp.get_parent_id(element_data=ElementsData.Test.B))
    uuid = await bp.get_id(element_data=ElementsData.Test.Canvas)
    print(await bp.get_sprite_name_list(uuid=uuid, offspring_path="Sprite"))
    print(await bp.get_sprite_name_list(uuid_list=[uuid, uuid], offspring_path="Sprite"))


async def get_progress_test(bp: BasePage):
    print(await bp.get_progress(element_data=ElementsData.Test.ProgressBar, offspring_path=""))
    # print(await bp.get_parent_id(element_data=ElementsData.Test.B))
    uuid = await bp.get_id(element_data=ElementsData.Test.ProgressBar)
    print(await bp.get_progress(uuid=uuid))


async def get_progress_list_test(bp: BasePage):
    print(await bp.get_progress_list(element_data_list=[ElementsData.Test.ProgressBar, ElementsData.Test.B]))
    # print(await bp.get_parent_id(element_data=ElementsData.Test.B))
    uuid = await bp.get_id(element_data=ElementsData.Test.Canvas)
    print(await bp.get_progress_list(uuid=uuid, offspring_path="ProgressBar"))
    print(await bp.get_progress_list(uuid_list=[uuid, uuid], offspring_path="ProgressBar"))

async def get_toggle_is_checked_test(bp: BasePage):
    print(await bp.get_toggle_is_checked(element_data=ElementsData.Test.Toggle, offspring_path=""))
    # print(await bp.get_parent_id(element_data=ElementsData.Test.B))
    uuid = await bp.get_id(element_data=ElementsData.Test.Toggle)
    print(await bp.get_toggle_is_checked(uuid=uuid))


async def get_toggle_is_checked_list_test(bp: BasePage):
    print(await bp.get_toggle_is_checked_list(element_data_list=[ElementsData.Test.Toggle, ElementsData.Test.B]))
    # print(await bp.get_parent_id(element_data=ElementsData.Test.B))
    uuid = await bp.get_id(element_data=ElementsData.Test.Canvas)
    print(await bp.get_toggle_is_checked_list(uuid=uuid, offspring_path="Toggle"))
    print(await bp.get_toggle_is_checked_list(uuid_list=[uuid, uuid], offspring_path="Toggle"))


async def get_name_test(bp: BasePage):
    print(await bp.get_name(element_data=ElementsData.Test.Sprite, offspring_path=""))
    # print(await bp.get_parent_id(element_data=ElementsData.Test.B))
    uuid = await bp.get_id(element_data=ElementsData.Test.Sprite)
    print(await bp.get_name(uuid=uuid))


async def get_name_list_test(bp: BasePage):
    print(await bp.get_name_list(element_data_list=[ElementsData.Test.Sprite, ElementsData.Test.B]))
    # print(await bp.get_parent_id(element_data=ElementsData.Test.B))
    uuid = await bp.get_id(element_data=ElementsData.Test.Canvas)
    print(await bp.get_name_list(uuid=uuid, offspring_path="Sprite"))
    print(await bp.get_name_list(uuid_list=[uuid, uuid], offspring_path="Sprite"))


async def get_id_test(bp: BasePage):
    print(await bp.get_id(element_data=ElementsData.Test.A))
    # print(await bp.get_parent_id(element_data=ElementsData.Test.B))
    uuid = await bp.get_id(element_data=ElementsData.Test.A)
    print(uuid)
    print(await bp.get_id(uuid=uuid))


async def get_id_list_test(bp: BasePage):
    print(await bp.get_id_list(element_data_list=[ElementsData.Test.A, ElementsData.Test.B]))
    # print(await bp.get_parent_id(element_data=ElementsData.Test.B))
    uuid = await bp.get_id(element_data=ElementsData.Test.A)
    print(uuid)
    print(await bp.get_id_list(uuid=uuid, offspring_path="Button1"))
    print(await bp.get_id_list(uuid_list=[uuid, uuid], offspring_path="Button1"))

async def get_parent_id_test(bp: BasePage):
    print(await bp.get_parent_id(element_data=ElementsData.Test.A))
    # print(await bp.get_parent_id(element_data=ElementsData.Test.B))
    uuid = await bp.get_id(element_data=ElementsData.Test.A)
    print(uuid)
    print(await bp.get_parent_id(uuid=uuid))


async def get_parent_id_list_test(bp: BasePage):
    print(await bp.get_parent_id_list(element_data_list=[ElementsData.Test.A, ElementsData.Test.B]))
    # print(await bp.get_parent_id(element_data=ElementsData.Test.B))
    uuid = await bp.get_id(element_data=ElementsData.Test.A)
    print(uuid)
    print(await bp.get_parent_id_list(uuid=uuid, offspring_path="Button1"))
    print(await bp.get_parent_id_list(uuid_list=[uuid, uuid], offspring_path="Button1"))




@rpc_server(port=5101)
async def main(server):
    bp = BasePage(window_title="Cocos Creator - NewProject", server=server)
    await bp.initialize()
    await bp.custom_command("setCamera Canvas/Camera")

    await get_screen_size_test(bp)

    # await exist_test(bp)

    # await get_position_test(bp)
    #
    # await get_position_list_test(bp)

    # await get_size_test(bp)
    #
    # await get_size_list_test(bp)

    # await get_text_test(bp)

    # await get_text_list_test(bp)

    # await set_text_test(bp)
    #
    # await set_text_list_test(bp)

    # await get_sprite_name_test(bp)
    #
    # await get_sprite_name_list_test(bp)

    # await get_progress_test(bp)
    #
    # await get_progress_list_test(bp)

    # await get_toggle_is_checked_test(bp)
    #
    # await get_toggle_is_checked_list_test(bp)

    # await get_name_test(bp)
    #
    # await get_name_list_test(bp)

    # await get_id_test(bp)
    #
    # await get_id_list_test(bp)

    # await get_parent_id_test(bp)

    # await get_parent_id_list_test(bp)



if __name__ == "__main__":
    main()

from common.base_page import BasePage
from common.ws_server import rpc_server
from configs.element_data import ElementsData


@rpc_server(port=5101)
async def main(server):
    bp = BasePage(server=server)
    await bp.custom_command("setCamera ui_layer/UICamera")
    perform_list = [
        ElementsData.UIStoryRecount.lab_continue,
        ElementsData.UIStoryDialogue.lab_continue,
        ElementsData.UIStoryGuide.hand,
        ElementsData.UILevelHUD.btn_rankup,
        ElementsData.UISupportPromote.UISupportPromote,
        ElementsData.UIStoryDialogue.lab_continue,
        ElementsData.UIStoryDialogue.but_choice1,
        ElementsData.UIStoryDialogue.lab_continue,
        ElementsData.UIStoryGuide.hand,
    ]
    await bp.click_a_until_b_appear_list(perform_list=perform_list)




if __name__ == "__main__":
    main()
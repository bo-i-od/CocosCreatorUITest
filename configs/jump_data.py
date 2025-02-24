from configs.element_data import ElementsData


class JumpData:
    element_data_home = ElementsData.HomePanel.HomePanel
    panel_list = [ElementsData.Test.A, ElementsData.Test.B]
    # 弹窗名
    pop_window_set = {
        ""
    }

    panel_dict = {
        "A": {"element_data": ElementsData.Test.A, "open_path": [ElementsData.HomePanel.HomePanel],  "close_path": [ElementsData.Test.B]},

    }

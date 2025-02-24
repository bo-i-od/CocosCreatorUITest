from configs.element_data import ElementsData

class JumpData:
    # 弹窗名
    pop_window_set = {
        ""
    }

    panel_dict = {
        "A": {"element_data": ElementsData.Test.A, "open_path": [ElementsData.HomePanel.btn_achievement],  "close_path": [ElementsData.AchievementPanel.btn_close]},

    }
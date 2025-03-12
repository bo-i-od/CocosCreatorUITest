class ElementsData:
    class Test:
        Canvas = {"locator": "Canvas"}
        button = {"locator": "Canvas/A/"}
        button1 = {"locator": "Canvas/A/Button1"}
        button2 = {"locator": "Canvas/A/Button2"}
        button1_label = {"locator": "Canvas/A/Button1/Label"}
        toggle = {"locator": "Canvas/Toggle"}
        A = {"locator": "Canvas/A"}
        B = {"locator": "Canvas/B"}
        Sprite = {"locator": "Canvas/Sprite"}
        ProgressBar = {"locator": "Canvas/ProgressBar"}
        Toggle = {"locator": "Canvas/Toggle"}
        Slider = {"locator": "Canvas/Slider"}

    class HomePanel:
        HomePanel = {"locator": "Canvas/HomePanel"}

    class UIStoryRecount:
        lab_continue = {"locator": "ui_layer/view/UIStoryRecount/UIStoryRecount/_lab_tips:lab", "focus": (0.5, 0.5)}

    class UIStoryDialogue:
        lab_continue = {"locator": "ui_layer/view/UIStoryDialogue/UIStoryDialogue/_dialogNode/dialog_item/group_continue/lab_continue:lab", "focus": (1, 0.5)}
        but_choice1 = {"locator": "ui_layer/view/UIStoryDialogue/UIStoryDialogue/_dialogNode/dialog_item/but_choice1:but", "focus": (0.5, 0.5)}
        but_choice2 = {"locator": "ui_layer/view/UIStoryDialogue/UIStoryDialogue/_dialogNode/dialog_item/but_choice2:but", "focus": (0.5, 0.5)}

    class UILevelHUD:
        btn_rankup = {"locator": "ui_layer/view/UILevelHUD/UIPopularwillRoot/UIPopularwillRoot/_top/_lock/_group_support_rankup/_btn_rankup:but", "focus": (0.5, 0.5)}



    class UIStoryGuide:
        hand = {"locator": "ui_layer/view/UIStoryGuide/UIStoryGuide/_hand", "focus": (0.5, 0.5)}


    class UISupportPromote:
        UISupportPromote = {"locator": "ui_layer/view/UISupportPromote/UISupportPromote", "focus": (0.5, 0.5)}



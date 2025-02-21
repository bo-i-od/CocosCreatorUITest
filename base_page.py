from airtest.core.api import connect_device
from error import InvalidOperationError


class BasePage:
    def __init__(self, dev=None):
        self.dev = dev
        if self.dev is None:
            self.dev = connect_device("Windows:///?title_re=.*Cocos Simulator.*")
            # self.dev = connect_device("Windows:///?title_re=.*Cocos Creator - NewProject.*")
            # self.dev = connect_device("Windows:///?title_re=.*Cocos Creator.*")



        self.screen_w, self.screen_h = self.get_screen_size()  # 获取屏幕尺寸
        print(self.screen_w, self.screen_h)
        self.scale_factor_w, self.scale_factor_h = self.get_scale_factor()

    def get_scale_factor(self):
        resolution_w, resolution_h = self.dev.get_current_resolution()
        print(resolution_w, resolution_h)
        scale_factor_w = self.screen_w / resolution_w
        scale_factor_h = self.screen_h / resolution_h

        return scale_factor_w, scale_factor_h

    def click_position_base(self, position):
        position[0] = (1 - self.scale_factor_w) * 0.5 + position[0] * self.scale_factor_w
        position[1] = 1 - self.scale_factor_h + self.scale_factor_h * position[1]
        if not (0 <= position[0] <= 1) or not (0 <= position[1] <= 1):
            raise InvalidOperationError('Click position out of screen. pos={}'.format(repr(position)))
        print(position)
        # self.dev.touch(position)

    def get_screen_size(self):
        return 1918, 1076




if __name__ == "__main__":
    bp = BasePage()
    # print(inputs.click(0, 0))
    # bp.click_position_base(position=[0, 1])



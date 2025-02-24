from airtest.core.api import connect_device

from common import rpc_method_request
from error import *


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
        self.server = None

    def get_scale_factor(self):
        resolution_w, resolution_h = self.dev.get_current_resolution()
        print(resolution_w, resolution_h)
        scale_factor_w = self.screen_w / resolution_w
        scale_factor_h = self.screen_h / resolution_h

        return scale_factor_w, scale_factor_h

    # 判断列表是不是长度为1，不为1会报错
    # 判断列表是不是长度为1，不为1会报错
    @staticmethod
    def is_single_element(element_list: list):
        """函数功能简述
            保证元素列表中的元素数量是1
            防止取单一元素时，取到多个或没取到

        参数:
            element_list: 获取到的元素组成的列表
        """
        if len(element_list) == 0:
            raise FindNoElementError("FindNoElement")
        elif len(element_list) > 1:
            raise PluralElementError("PluralElement")

    @staticmethod
    def get_element_data(element_data, offspring_path):
        """函数功能简述
            把路径和偏移路径合成为当前要用的的element_data

        参数:
            element_data: 元素定位信息，主要是路径信息
            offspring_path: 偏移路径

        返回:
            dict
        """
        element_data_copy = element_data
        if offspring_path != "":
            element_data_copy = element_data.copy()
            element_data_copy["locator"] = element_data_copy["locator"] + '>' + offspring_path
        return element_data_copy

    def get_element_data_list(self, element_data_list, offspring_path):
        """函数功能简述
            调用 get_element_data()方法
            依次把element_data_list中的element_data和offspring_path合成

        参数:
            element_data_list: 元素定位信息组成的列表
            offspring_path: 偏移路径

        返回:
            list[dict]
        """
        if offspring_path == "":
            return element_data_list
        cur = 0
        while cur < len(element_data_list):
            element_data_list[cur] = self.get_element_data(element_data_list[cur], offspring_path)
            cur += 1
        return element_data_list

    def exist(self, element_data=None, uuid=None, offspring_path=""):
        """函数功能简述
            判断元素是否存在

        参数:
            object_id和element_data输入其中的一个
            object_id: 优先object_id定位元素
            element_data: 元素定位信息定位
            offspring_path: 偏移路径

        返回:
            存在返回True
            不存在返回False
        """

        if self.get_id_list(element_data=element_data, uuid=uuid, offspring_path=offspring_path):
            return True
        return False

    # 得到元素的Instance Id
    def get_id(self, element_data: dict = None, uuid: str = None, offspring_path=""):
        """函数功能简述
            获取元素id

        参数:
            element_data: 元素定位信息
            offspring_path: 偏移路径

        返回:
            object_id_list有且只有一个元素时，返回str
        """
        uuid_list = self.get_id_list(element_data=element_data, uuid=uuid, offspring_path=offspring_path)
        self.is_single_element(uuid_list)
        return uuid_list[0]

    def get_id_list(self, element_data: dict = None, element_data_list: list = None, uuid: str = None, uuid_list: list = None, offspring_path=""):
        """函数功能简述
            根据偏移路径获取元素id

        参数:
            element_data, element_data_list, object_id, object_id_list输入其中一个
            object_id: 元素id
            object_id_list: object_id组成的list
            element_data: 元素定位信息
            element_data_list: element_data组成的list
            offspring_path: 偏移路径

        返回:
            输入uuid时，返回list[int]
            输入uuid_list时，返回list[list[int]]
            输入element_data时，返回list[int]
            输入element_data_list时，返回list[list[int]]
        """
        if uuid:
            return self.get_id_list(uuid_list=[uuid], offspring_path=offspring_path)[0]
        if uuid_list:
            return rpc_method_request.get_id_by_id(self.server, uuid_list, offspring_path)

        if element_data is not None:
            return self.get_id_list(element_data_list=[element_data], offspring_path=offspring_path)[0]
        element_data_copy_list = self.get_element_data_list(element_data_list, offspring_path)
        return rpc_method_request.get_id(server=self.server, element_data_list=element_data_copy_list)



    def click_position_base(self, position):
        position[0] = (1 - self.scale_factor_w) * 0.5 + position[0] * self.scale_factor_w
        position[1] = 1 - self.scale_factor_h + self.scale_factor_h * position[1]
        if not (0 <= position[0] <= 1) or not (0 <= position[1] <= 1):
            raise InvalidOperationError('Click position out of screen. pos={}'.format(repr(position)))
        self.dev.touch(position)

    def get_screen_size(self):
        return rpc_method_request.get_screen_size(self.server)




if __name__ == "__main__":
    bp = BasePage()
    # print(inputs.click(0, 0))
    # bp.click_position_base(position=[0, 1])



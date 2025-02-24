import random

from airtest.core.api import connect_device
from common import rpc_method_request
from configs.jump_data import JumpData
from error import *
from tools import common_tools
import asyncio


class BasePage:
    def __init__(self, server, window_title, dev=None):
        self.server = server
        self.dev = dev
        if self.dev is None:
            # self.dev = connect_device("Windows:///?title_re=.*Cocos Simulator.*")
            self.dev = connect_device(f"Windows:///?title_re=.*{window_title}.*")
            # self.dev = connect_device("Windows:///?title_re=.*Cocos Creator.*")
        self.screen_w = None
        self.screen_h = None
        self.scale_factor_w = None
        self.scale_factor_h = None

    async def initialize(self):
        self.screen_w, self.screen_h = await self.get_screen_size()  # 获取屏幕尺寸
        self.scale_factor_w, self.scale_factor_h = self.get_scale_factor()

    @staticmethod
    async def sleep(t):
        await asyncio.sleep(t)

    async def get_screen_size(self):
        return await rpc_method_request.get_screen_size(self.server)

    def get_scale_factor(self):
        resolution_w, resolution_h = self.dev.get_current_resolution()
        scale_factor_w = self.screen_w / resolution_w
        scale_factor_h = self.screen_h / resolution_h
        return scale_factor_w, scale_factor_h

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
    def get_element_data(element_data: dict, offspring_path: str):
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

    def get_element_data_list(self, element_data_list: list, offspring_path: str):
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

    async def exist(self, element_data: dict = None, uuid: str = None, offspring_path: str = ""):
        """函数功能简述
            判断元素是否存在

        参数:
            uuid和element_data输入其中的一个
            uuid: 优先uuid定位元素
            element_data: 元素定位信息定位
            offspring_path: 偏移路径

        返回:
            存在返回True
            不存在返回False
        """

        if await self.get_id_list(element_data=element_data, uuid=uuid, offspring_path=offspring_path):
            return True
        return False

    async def get_position(self, element_data: dict = None, uuid: str = None, offspring_path: str = "",
                           anchor_point: list = None, locator_camera: str = ""):
        """函数功能简述
            定位元素后取元素的position值

        参数:
            uuid和element_data输入其中的一个
            uuid: 元素id
            element_data: 元素定位信息
            offspring_path: 偏移路径

        返回:
            position_list有且只有一个元素时，返回[float, float]
            float值在0~1，以屏幕左上角作为原点

        """
        """
               (0, 0)    (0.5, 0)   (1, 0)
                      ______ ______
                     |      |      |
             (0, 0.5)|______|______|(1, 0.5)
                     |      |      |
                     |______|______|
               (0, 1)    (0.5, 1)   (1, 1)
        """
        if anchor_point is None:
            anchor_point = [0.5, 0.5]
        position_list = await self.get_position_list(element_data=element_data, uuid=uuid,
                                                     offspring_path=offspring_path, anchor_point=anchor_point,
                                                     locator_camera=locator_camera)
        self.is_single_element(position_list)
        return position_list[0]

    async def get_position_list(self,  element_data: dict = None, element_data_list: list = None,
                                uuid: str = None, uuid_list: list = None, offspring_path: str = "",
                                anchor_point: list = None, locator_camera: str = ""):
        """函数功能简述
            定位元素后取元素的position值

        参数:
            uuid, uuid_list, element_data, element_data_list输入其中一个
            uuid: 元素id
            uuid_list: 元素id组成的list
            element_data: 元素定位信息
            element_data_list: 元素定位信息组成的list
            offspring_path: 偏移路径

        返回:
            输入uuid或element_data时，返回list[[float, float]]
            输入uuid_list或element_data_list时，返回list[list[[float, float]]]
        """
        if anchor_point is None:
            anchor_point = [0.5, 0.5]

        if uuid:
            results = await self.get_position_list(uuid_list=[uuid], offspring_path=offspring_path,
                                                   anchor_point=anchor_point, locator_camera=locator_camera)
            return results[0]

        if uuid_list:
            return await rpc_method_request.get_position_by_id(self.server, uuid_list, offspring_path,
                                                               anchor_point, locator_camera)

        if element_data:
            results = await self.get_position_list(element_data_list=[element_data], offspring_path=offspring_path)
            return results[0]

        element_data_copy_list = self.get_element_data_list(element_data_list, offspring_path)
        return await rpc_method_request.get_position(self.server, element_data_copy_list)

    async def get_size(self, uuid: str = None, element_data: dict = None, offspring_path: str = ""):
        """函数功能简述
            定位元素后取元素的width和height值

        参数:
            uuid和element_data输入其中的一个
            uuid: 元素id
            element_data: 元素定位信息
            offspring_path: 偏移路径

        返回:
            size_list有且只有一个元素时，返回[float, float]
            width和height值在0~1
         """

        size_list = await self.get_size_list(element_data=element_data, uuid=uuid, offspring_path=offspring_path)
        self.is_single_element(size_list)
        return size_list[0]

    async def get_size_list(self, element_data: dict = None, element_data_list: list = None,
                            uuid: str = None, uuid_list: list = None, offspring_path: str = ""):
        """函数功能简述
            定位元素后取元素的width和height值

        参数:
            uuid, uuid_list, element_data, element_data_list输入其中一个
            uuid: 元素id
            uuid_list: 元素id组成的list
            element_data: 元素定位信息
            element_data_list: 元素定位信息组成的list
            offspring_path: 偏移路径

        返回:
            输入uuid或element_data时，返回list[[float, float]]
            输入uuid_list或element_data_list时，返回list[list[[float, float]]]
        """
        if uuid:
            results = await self.get_size_list(uuid_list=[uuid], offspring_path=offspring_path)
            return results[0]

        if uuid_list:
            return await rpc_method_request.get_size_by_id(self.server, uuid_list, offspring_path)

        if element_data:
            results = await self.get_size_list(element_data_list=[element_data], offspring_path=offspring_path)
            return results[0]

        element_data_copy_list = self.get_element_data_list(element_data_list, offspring_path)
        return await rpc_method_request.get_size(self.server, element_data_copy_list)

    async def get_text(self, uuid: str = None, element_data: dict = None, offspring_path: str = ""):
        """函数功能简述
            定位元素后取元素文本组件的值

        参数:
            uuid和element_data输入其中的一个
            uuid: 元素id
            element_data: 元素定位信息
            offspring_path: 偏移路径

        返回:
            text_list有且只有一个元素时，返回str
        """
        text_list = await self.get_text_list(element_data=element_data, uuid=uuid, offspring_path=offspring_path)
        self.is_single_element(text_list)
        return text_list[0]

    async def get_text_list(self, element_data: dict = None, element_data_list: list = None,
                            uuid: str = None, uuid_list: list = None, offspring_path=""):
        """函数功能简述
            定位元素后取元素文本组件的值

        参数:
            uuid, uuid_list, element_data, element_data_list输入其中一个
            uuid: 元素id
            uuid_list: 元素id组成的list
            element_data: 元素定位信息
            element_data_list: 元素定位信息组成的list
            offspring_path: 偏移路径

        返回:
            输入uuid或element_data时，返回list[str]
            输入uuid_list或element_data_list时，返回list[list[str]]
        """
        if uuid:
            results = await self.get_text_list(uuid_list=[uuid], offspring_path=offspring_path)
            return results[0]

        if uuid_list:
            return await rpc_method_request.get_text_by_id(self.server, uuid_list, offspring_path)

        if element_data:
            results = await self.get_text_list(element_data_list=[element_data], offspring_path=offspring_path)
            return results[0]

        element_data_copy_list = self.get_element_data_list(element_data_list, offspring_path)
        return await rpc_method_request.get_text(self.server, element_data_copy_list)

    async def set_text(self, uuid: str = None, element_data: dict = None, text: str = "", offspring_path: str = ""):
        """函数功能简述
            定位元素后设元素文本组件的值

        参数:
            uuid和element_data输入其中的一个
            uuid: 元素id
            element_data: 元素定位信息
            offspring_path: 偏移路径

        返回:
            None
        """
        await self.set_text_list(element_data=element_data, uuid=uuid, text=text, offspring_path=offspring_path)

    async def set_text_list(self, element_data: dict = None, element_data_list: list = None,
                            uuid: str = None, uuid_list: list = None, text: str = "", offspring_path: str = ""):
        """函数功能简述
            定位元素后设元素文本组件的值

        参数:
            uuid, uuid_list, element_data, element_data_list输入其中一个
            uuid: 元素id
            uuid_list: 元素id组成的list
            element_data: 元素定位信息
            element_data_list: 元素定位信息组成的list
            offspring_path: 偏移路径

        返回:
            None
        """

        if uuid:
            await self.set_text_list(uuid_list=[uuid], offspring_path=offspring_path, text=text)
            return

        if uuid_list:
            await rpc_method_request.set_text_by_id(self.server, uuid_list, offspring_path, text)
            return

        if element_data:
            await self.set_text_list(element_data_list=[element_data], text=text, offspring_path=offspring_path)
            return

        element_data_copy_list = self.get_element_data_list(element_data_list, offspring_path)
        await rpc_method_request.set_text(self.server, element_data_copy_list, text)

    async def get_sprite_name(self, uuid: str = None, element_data: dict = None, offspring_path: str = ""):
        """函数功能简述
            定位元素后取元素名

        参数:
            uuid和element_data输入其中的一个
            uuid: 元素id
            element_data: 元素定位信息
            offspring_path: 偏移路径

        返回:
            name_list有且只有一个元素时，返回str
         """
        sprite_name_list = await self.get_sprite_name_list(element_data=element_data, uuid=uuid,
                                                           offspring_path=offspring_path)
        self.is_single_element(sprite_name_list)
        return sprite_name_list[0]

    async def get_sprite_name_list(self,  element_data: dict = None, element_data_list: list = None,
                                   uuid: str = None, uuid_list: list = None, offspring_path: str = ""):
        """函数功能简述
            定位元素后取元素图标组件的Sprite名

        参数:
            uuid, uuid_list, element_data, element_data_list输入其中一个
            uuid: 元素id
            uuid_list: 元素id组成的list
            element_data: 元素定位信息
            element_data_list: 元素定位信息组成的list
            offspring_path: 偏移路径

        返回:
            输入uuid或element_data时，返回list[str]
            输入uuid_list或element_data_list时，返回list[list[str]]
        """
        if uuid:
            results = await self.get_sprite_name_list(uuid_list=[uuid], offspring_path=offspring_path)
            return results[0]

        if uuid_list:
            return await rpc_method_request.get_sprite_name_by_id(self.server, uuid_list, offspring_path)

        if element_data:
            results = await self.get_sprite_name_list(element_data_list=[element_data], offspring_path=offspring_path)
            return results[0]

        element_data_copy_list = self.get_element_data_list(element_data_list, offspring_path)
        return await rpc_method_request.get_sprite_name(self.server, element_data_copy_list)

    async def get_progress(self, uuid: str = None, element_data: dict = None, offspring_path: str = ""):
        """函数功能简述
            定位元素后取元素slider组件的值

        参数:
            uuid和element_data输入其中的一个
            uuid: 元素id
            element_data: 元素定位信息
            offspring_path: 偏移路径

        返回:
            slider_value_list有且只有一个元素时，返回float
            值在0~1
         """
        progress_list = await self.get_progress_list(element_data=element_data, uuid=uuid,
                                                     offspring_path=offspring_path)
        self.is_single_element(progress_list)
        return progress_list[0]

    async def get_progress_list(self, element_data: dict = None, element_data_list: list = None,
                                uuid: str = None, uuid_list: list = None, offspring_path: str = ""):
        """函数功能简述
            定位元素后取元素slider组件的值

        参数:
            uuid, uuid_list, element_data, element_data_list输入其中一个
            uuid: 元素id
            uuid_list: 元素id组成的list
            element_data: 元素定位信息
            element_data_list: 元素定位信息组成的list
            offspring_path: 偏移路径

        返回:
            输入uuid或element_data时，返回list[float]
            输入uuid_list或element_data_list时，返回list[list[float]]
        """
        if uuid:
            results = await self.get_progress_list(uuid_list=[uuid], offspring_path=offspring_path)
            return results[0]

        if uuid_list:
            return await rpc_method_request.get_progress_by_id(self.server, uuid_list, offspring_path)

        if element_data:
            results = await self.get_progress_list(element_data_list=[element_data], offspring_path=offspring_path)
            return results[0]

        element_data_copy_list = self.get_element_data_list(element_data_list, offspring_path)
        return await rpc_method_request.get_progress(self.server, element_data_copy_list)

    async def get_toggle_is_checked(self, uuid: str = None, element_data: dict = None, offspring_path: str = ""):
        """函数功能简述
            定位元素后取元素toggle组件的IsOn

        参数:
            uuid和element_data输入其中的一个
            uuid: 元素id
            element_data: 元素定位信息
            offspring_path: 偏移路径

        返回:
            toggle_is_on_list有且只有一个元素时，返回bool
        """
        toggle_is_on_list = await self.get_toggle_is_checked_list(element_data=element_data, uuid=uuid,
                                                                  offspring_path=offspring_path)
        self.is_single_element(toggle_is_on_list)
        return toggle_is_on_list[0]

    async def get_toggle_is_checked_list(self, element_data: dict = None, element_data_list: list = None,
                                         uuid: str = None, uuid_list: list = None, offspring_path: str = ""):
        """函数功能简述
            定位元素后取元素toggle组件的IsOn

        参数:
            uuid, uuid_list, element_data, element_data_list输入其中一个
            uuid: 元素id
            uuid_list: 元素id组成的list
            element_data: 元素定位信息
            element_data_list: 元素定位信息组成的list
            offspring_path: 偏移路径

        返回:
            输入uuid或element_data时，返回list[bool]
            输入uuid_list或element_data_list时，返回list[list[bool]]
        """
        if uuid:
            results = await self.get_toggle_is_checked_list(uuid_list=[uuid], offspring_path=offspring_path)
            return results[0]

        if uuid_list:
            return await rpc_method_request.get_toggle_is_checked_by_id(self.server, uuid_list, offspring_path)

        if element_data:
            results = await self.get_toggle_is_checked_list(element_data_list=[element_data],
                                                            offspring_path=offspring_path)
            return results[0]

        element_data_copy_list = self.get_element_data_list(element_data_list, offspring_path)
        return await rpc_method_request.get_toggle_is_checked(self.server, element_data_copy_list)

    async def get_name(self, uuid: str = None, element_data: dict = None, offspring_path: str = ""):
        """函数功能简述
            定位元素后取元素名

        参数:
            uuid和element_data输入其中的一个
            uuid: 元素id
            element_data: 元素定位信息
            offspring_path: 偏移路径

        返回:
            name_list有且只有一个元素时，返回str
         """
        name_list = await self.get_name_list(element_data=element_data, uuid=uuid, offspring_path=offspring_path)
        self.is_single_element(name_list)
        return name_list[0]

    async def get_name_list(self,  element_data: dict = None, element_data_list: list = None,
                            uuid: str = None, uuid_list: list = None, offspring_path: str = ""):
        """函数功能简述
            定位元素后取元素图标组件的Sprite名

        参数:
            uuid, uuid_list, element_data, element_data_list输入其中一个
            uuid: 元素id
            uuid_list: 元素id组成的list
            element_data: 元素定位信息
            element_data_list: 元素定位信息组成的list
            offspring_path: 偏移路径

        返回:
            输入uuid或element_data时，返回list[str]
            输入uuid_list或element_data_list时，返回list[list[str]]
        """
        # 输入uuid的情况，将uuid加上[]转为uuid_list
        if uuid:
            results = await self.get_name_list(uuid_list=[uuid], offspring_path=offspring_path)
            return results[0]

        # 输入uuid_list的情况，直接调用rpc
        if uuid_list:
            return await rpc_method_request.get_name_by_id(self.server, uuid_list, offspring_path)

        # 输入element_data的情况,将element_data加[]转为element_data_list
        if element_data:
            results = await self.get_name_list(element_data_list=[element_data], offspring_path=offspring_path)
            return results[0]

        # 输入element_data_list的情况，直接调用rpc
        element_data_copy_list = self.get_element_data_list(element_data_list, offspring_path)
        return await rpc_method_request.get_name(self.server, element_data_copy_list)

    # 得到元素的Instance Id
    async def get_id(self, element_data: dict = None, uuid: str = None, offspring_path: str = ""):
        """函数功能简述
            获取元素id

        参数:
            element_data: 元素定位信息
            offspring_path: 偏移路径

        返回:
            uuid_list有且只有一个元素时，返回str
        """
        uuid_list = await self.get_id_list(element_data=element_data, uuid=uuid, offspring_path=offspring_path)
        self.is_single_element(uuid_list)
        return uuid_list[0]

    async def get_id_list(self, element_data: dict = None, element_data_list: list = None,
                          uuid: str = None, uuid_list: list = None, offspring_path: str = ""):
        """函数功能简述
            根据偏移路径获取元素id

        参数:
            element_data, element_data_list, uuid, uuid_list输入其中一个
            uuid: 元素id
            uuid_list: uuid组成的list
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
            results = await self.get_id_list(uuid_list=[uuid], offspring_path=offspring_path)
            return results[0]

        if uuid_list:
            return await rpc_method_request.get_id_by_id(self.server, uuid_list, offspring_path)

        if element_data:
            results = await self.get_id_list(element_data_list=[element_data], offspring_path=offspring_path)
            return results[0]

        element_data_copy_list = self.get_element_data_list(element_data_list, offspring_path)
        return await rpc_method_request.get_id(server=self.server, element_data_list=element_data_copy_list)

    async def get_parent_id(self, uuid: str = None, element_data: dict = None, offspring_path: str = ""):
        """函数功能简述
            定位元素后取元素的父节点id

        参数:
            uuid和element_data输入其中的一个
            uuid: 元素id
            element_data: 元素定位信息
            offspring_path: 偏移路径

        返回:
            parent_id_list有且只有一个元素时，返回int
        """

        parent_id_list = await self.get_parent_id_list(element_data=element_data, uuid=uuid,
                                                       offspring_path=offspring_path)
        self.is_single_element(parent_id_list)
        return parent_id_list[0]

    async def get_parent_id_list(self, element_data: dict = None, element_data_list: list = None,
                                 uuid: str = None, uuid_list: list = None, offspring_path: str = ""):
        """函数功能简述
            定位元素后取元素的父节点id

        参数:
            uuid, uuid_list, element_data, element_data_list输入其中一个
            uuid: 元素id
            uuid_list: 元素id组成的list
            element_data: 元素定位信息
            element_data_list: 元素定位信息组成的list
            offspring_path: 偏移路径

        返回:
            输入uuid或element_data时，返回list[int]
            输入uuid_list或element_data_list时，返回list[list[int]]
        """
        if uuid:
            results = await self.get_parent_id_list(uuid_list=[uuid], offspring_path=offspring_path)
            return results[0]

        if uuid_list:
            return await rpc_method_request.get_parent_id_by_id(self.server, uuid_list, offspring_path)

        if element_data:
            results = await self.get_parent_id_list(element_data_list=[element_data], offspring_path=offspring_path)
            return results[0]

        element_data_copy_list = self.get_element_data_list(element_data_list, offspring_path)
        return await rpc_method_request.get_parent_id(self.server, element_data_copy_list)

    async def command(self, cmd: str):
        await self.command_list([cmd])

    async def command_list(self, cmd_list: list):
        await rpc_method_request.command(self.server, cmd_list)

    async def custom_command(self, cmd: str):
        await self.custom_command_list([cmd])

    async def custom_command_list(self, cmd_list: list):
        await rpc_method_request.custom_command(self.server, cmd_list)

    def click_position_base(self, position):
        """函数功能简述
            点击position处
        参数:
            position[float, float]
        """
        position[0] = (1 - self.scale_factor_w) * 0.5 + position[0] * self.scale_factor_w
        position[1] = 1 - self.scale_factor_h + self.scale_factor_h * position[1]
        if not (0 <= position[0] <= 1) or not (0 <= position[1] <= 1):
            raise InvalidOperationError('Click position out of screen. pos={}'.format(repr(position)))
        self.dev.touch(position)

    def click_position(self, position, ignore_set=None):
        """函数功能简述
            点击position处
            点击前会清除一遍弹窗
        参数:
            position[float, float]
            ignore_set: 需要忽略清除的弹窗
        """
        self.clear_popup(ignore_set)
        self.click_position_base(position)

    async def click_element(self, uuid: str = None, element_data: dict = None, offspring_path: str = "",
                            anchor_point: list = None, locator_camera: str = "", ignore_set=None):
        """函数功能简述
            定位元素后取元素的position值

        参数:
            object_id和element_data输入其中的一个
            object_id: 元素id
            element_data: 元素定位信息
            offspring_path: 偏移路径
            ignore_set: 需要忽略清除的弹窗
            focus: 元素锚点，用于计算元素中心位置

        返回:
            position_list有且只有一个元素时，返回[float, float]
        """
        self.clear_popup(ignore_set)
        position_list = await self.get_position_list(element_data=element_data, uuid=uuid,
                                                     offspring_path=offspring_path, anchor_point=anchor_point,
                                                     locator_camera=locator_camera)
        self.is_single_element(position_list)
        self.click_position_base(position_list[0])
        return position_list[0]

    async def click_element_safe(self, uuid: str = None, element_data: dict = None, offspring_path="",
                                 anchor_point: list = None, locator_camera: str = ""):
        """函数功能简述
            元素存在且在屏幕范围内时再点击
            不清除弹窗

        参数:
            object_id和element_data选择一个输入
            object_id: 元素id
            element_data: 检测元素
            offspring_path: 偏移路径
        """
        position_list = await self.get_position_list(uuid=uuid, element_data=element_data,
                                                     offspring_path=offspring_path, anchor_point=anchor_point,
                                                     locator_camera=locator_camera)

        if not position_list:
            return
        try:
            r = random.randint(0, len(position_list) - 1)
            self.click_position_base(position_list[r])
        except InvalidOperationError:
            pass

    def clear_popup_once(self, ignore_set=None):
        """函数功能简述
            清除弹窗一次

        参数:
            ignore_set: 忽略的弹窗
        """
        if ignore_set is None:
            ignore_set = set()
        panel_name_list = self.get_name_list(element_data_list=JumpData.panel_list)
        panel_name_list = common_tools.merge_list(panel_name_list)
        # 弹窗=检测到的弹窗-忽略的弹窗
        pop_window_set = set(panel_name_list) & JumpData.pop_window_set - ignore_set

        # 没有弹窗
        if not pop_window_set:
            return True
        for panel_name in pop_window_set:
            if "close_path" not in JumpData.panel_dict[panel_name]:
                continue
            for close_element in JumpData.panel_dict[panel_name]["close_path"]:
                self.click_element_safe(element_data=close_element)
                self.sleep(1)
        return False

    def clear_popup(self, ignore_set=None):
        """函数功能简述
            一直清弹窗直到没有弹窗

        参数:
            ignore_set: 忽略的弹窗{str, str, ……}
        """
        while True:
            res = self.clear_popup_once(ignore_set)
            if res:
                break

    def go_home(self, cur_panel=None, target_panel=None):
        """函数功能简述
            回到主界面

        参数:
            cur_panel: 有一些面板会在HomePanel存在时同时存在，需要特殊记录这些面板
            target_panel: 目标面板，在回主界面的过程中，如果遇到target_panel也会跳出循环
        """
        at_home_flag = False
        while not at_home_flag:
            # 关闭一次除了HomePanel的所有面板
            self.clear_panel_except_home()
            self.sleep(0.5)

            # 在返回大厅过程中找到目标面板就直接返回
            at_target_panel_flag = False
            if target_panel:
                at_target_panel_flag = self.exist(element_data=JumpData.panel_dict[target_panel]["element_data"])
            if at_target_panel_flag:
                return

            # 有HomePanel且没有cur_panel需要关闭时才判断停止
            at_home_flag = self.exist(element_data=JumpData.element_data_home)
            if cur_panel is not None:
                at_home_flag = at_home_flag and not self.exist(
                    element_data=JumpData.panel_dict[cur_panel]["element_data"])

    def clear_panel_except_home(self):
        """函数功能简述
            关除了主界面的其它界面一次
        """
        panel_name_list = self.get_name_list(element_data_list=JumpData.panel_list)
        panel_name_list = common_tools.merge_list(panel_name_list)
        for panel_name in panel_name_list:
            if panel_name not in JumpData.panel_dict:
                continue
            self.clear_popup_once()
            if "close_path" not in JumpData.panel_dict[panel_name]:
                continue
            for close_element in JumpData.panel_dict[panel_name]["close_path"]:
                self.click_element_safe(element_data=close_element)
            break
        self.sleep(0.2)

    def go_to_panel(self, panel):
        """函数功能简述
            去指定面板

        参数:
            panel: 目标面板
        """
        panel_dict = JumpData.panel_dict[panel]
        # 在目标面板就直接返回
        if self.exist(element_data=panel_dict["element_data"]):
            return

        # 回大厅
        self.go_home(target_panel=panel)

        # 按照JumpData.panel_dict中记录的路径尝试点击，直到到目标面板
        while not self.exist(element_data=panel_dict["element_data"]):
            self.clear_popup_once()
            for element_data in panel_dict["open_path"]:
                self.click_element_safe(element_data=element_data)
                self.sleep(0.5)

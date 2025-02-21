'''
Author: zengbaocheng
Date: 2025-02-21 17:34:47
LastEditors: zengbaocheng
LastEditTime: 2025-02-21 18:25:17
Desc: 
'''
import struct

HEADER_SIZE = 4

class SimpleProtocolFilter(object):
    """ 
    简单协议过滤器
    协议按照 [有效数据字节数][有效数据] 这种协议包的格式进行打包和解包
    [有效数据字节数]长度HEADER_SIZE字节
    [有效数据]长度有效数据字节数字节
    本类按照这种方式，顺序从数据流中取出数据进行拼接，一旦接收完一个完整的协议包，就会将协议包返回
    [有效数据]字段接收到后会按照utf-8进行解码，因为在传输过程中是用utf-8进行编码的
    所有编解码的操作在该类中完成
    """
    # 初始化类的实例，创建一个空的字节缓冲区 self.buf，用于存储接收到的数据片段
    def __init__(self):
        super(SimpleProtocolFilter, self).__init__()
        self.buf = b''

    """
    该方法接收一个数据片段 data，并将其添加到缓冲区 self.buf 中。
    不断检查缓冲区中的数据是否足够组成一个完整的协议包。
    如果是，则从缓冲区中提取出完整的 [有效数据] 部分，并通过 yield 关键字将其返回，同时更新缓冲区，移除已处理的数据。
    如果数据不足，则停止处理。
    """
    def input(self, data):
        """
        小数据片段拼接成完整数据包
        如果内容足够则yield数据包
        """
        self.buf += data
        while len(self.buf) > HEADER_SIZE:
            data_len = struct.unpack('i', self.buf[0:HEADER_SIZE])[0]
            if len(self.buf) >= data_len + HEADER_SIZE:
                content = self.buf[HEADER_SIZE:data_len + HEADER_SIZE]
                self.buf = self.buf[data_len + HEADER_SIZE:]
                yield content
            else:
                break
    
    """
    这是一个静态方法，用于将给定的内容 content 按照协议格式进行打包。
    如果 content 是文本类型。
    使用 struct.pack 函数将 [有效数据字节数] 打包为 4 字节的整数，然后将其与 [有效数据] 拼接在一起返回。
    """
    @staticmethod
    def pack(content):
        """ 
        content should be str
        """
        return struct.pack('i', len(content)) + content

    """
    这是一个静态方法，用于将接收到的完整协议包进行解包。
    使用 struct.unpack 函数从协议包的前 4 字节中提取出 [有效数据字节数]。
    返回 [有效数据字节数] 和 [有效数据] 部分。
    """
    @staticmethod
    def unpack(data):
        """ 
        return length, content
        """
        length = struct.unpack('i', data[0:HEADER_SIZE])
        return length[0], data[HEADER_SIZE:]
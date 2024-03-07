import struct

def decode_binary_data(binary_data, data_types:str):
    """
    解码一串二进制数据为整数或浮点数列表。

    :param binary_data: 要解码的二进制数据，假设为bytes类型。
    :param data_type: 指定解码类型，'int'表示整数，'float'表示浮点数。
    :return: 包含解码后的整数或浮点数的列表。
    """
    decoded_data = []
    data_type_idx = 0
    for i in range(0, len(binary_data), 4):
        chunk = binary_data[i:i+4]
        data_type = data_types[data_type_idx]
        if data_type == 'int':
            # 解码为整数，使用大端格式
            decoded_data.append(struct.unpack('<i', chunk)[0])
        elif data_type == 'float':
            # 解码为浮点数，使用大端格式
            decoded_data.append(struct.unpack('<f', chunk)[0])
        else:
            raise ValueError("未知的数据类型: '{}'。请使用'int'或'float'。".format(data_type))
        data_type_idx += 1
    return decoded_data

if __name__ == "__main__":
    binary =  b'\x01\x00\x00\x00\x02\x00\x00\x00\xdb\x0f\x49\x40'
    types = ['int', 'int', 'float']
    print(decode_binary_data(binary, types))
import hashlib


def encrypt(text, line_num):
    """

    :param text: the damage text row without last | and encryption code
    :param line_num: line number of record
    :return: encryption code
    """
    test_str = (text + '|' + line_num).encode('utf-8')
    m = hashlib.sha256()
    m.update(test_str)
    hex_bytes = m.digest()
    t = u_49152(hex_bytes)
    return t


def u_49152(byte_str):
    lookup = u_49151()
    res = []
    for _ in range(16):
        res.append(None)
    for i in range(8):
        num = lookup[byte_str[i]]
        res[2*i] = chr(num % 128)
        res[2*i + 1] = chr((num >> 16) % 128)
    return "".join(res)


def u_49151():
    num_array = []
    for i in range(256):
        string = '{:02x}'.format(i)
        num_array.append(ord(string[0]) + (ord(string[1]) << 16))
    return num_array
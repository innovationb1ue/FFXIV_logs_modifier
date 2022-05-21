import hashlib
import os

# test function for fix a single row after modifying
def main():
    while True:
        text_str = input("Text: ")
        line_count = input("Line Num: ")
        test_str = (text_str + '|' + line_count).encode('utf-8')
        m = hashlib.sha256()
        m.update(test_str)
        hex_bytes = m.digest()
        t = u_49152(hex_bytes)
        print(t)


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


def change_file(path: str, source_name, multiplier, target_name):
    # open logs file
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    splited_path = os.path.splitext(path)
    target_path = f"{splited_path[0]}_modified{splited_path[1]}"
    f = open(target_path, 'w', encoding='utf-8')
    # iter lines
    idx = 0
    for row in lines:
        row_cols = row.split('|')
        # handle index
        idx = int(idx)+1
        idx = str(idx)
        if row_cols[0] == '01':
            idx = 1
        # skip non-relevant rows
        if row_cols[0] != '21':
            f.write(row)
            continue
        # skip self
        # self_name == target_name
        if row_cols[3] == row_cols[7]:
            f.write(row)
            continue
        # check target
        # [6] is target id              [7] is target name
        if row_cols[7] not in target_name and row_cols[6] not in target_name:
            f.write(row)
            continue
        # retrieve damage
        damage_str = row_cols[9]
        if damage_str.endswith('0000'):
            damage = int(damage_str[:-4], 16)
        elif damage_str.endswith('4001'):
            damage = 65535 + int(damage_str[:-4], 16)
        elif damage_str == '0':
            f.write(row)
            continue
        else:
            f.write(row)
            continue
        # modify teammates in order to cover their reports
        # if row_cols[3] != source_name:
        #     damage *= 1.003
        # modify self damage
        damage *= multiplier
        # reconstruct the hex representation of damage string
        damage = int(damage)
        if damage >= 65536:
            damage_increased = '{:X}4001'.format(damage - 65535)
        elif 0 < damage <= 65535:
            damage_increased = '{:X}0000'.format(damage)
        else:
            raise ValueError("damage increased error")
        row_cols[9] = damage_increased
        text = "|".join(row_cols[:-1])
        enc_code = encrypt(text, idx)
        row_cols[-1] = enc_code + '\n'
        new_row = "|".join(row_cols)
        print(idx, row, end='')
        print(idx, new_row, end='')
        f.write(new_row)
        f.flush()
    f.close()


if __name__ == '__main__':
    source_name = ''  # your player name here
    multiplier = 1.13  # damage modifier
    target_name = ['菲尼克司']
    # path to the logs file
    change_file('./logs_files/SplitNetwork_26404_20220427-2022-04-27T20-04-11.809Z.log',
                source_name,
                multiplier,
                target_name)
    # main()






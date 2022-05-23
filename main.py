import hashlib
import os

from encrypt_funcs import encrypt, u_49152


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


def modify_file(path: str, source_name, multiplier, target_name):
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
            print("reset")
            idx = 1
        if row_cols[0] != "21" or (row_cols[6] not in target_name and row_cols[7] not in target_name):
            f.write(row)
            continue
        # skip self
        # self_name == target_name
        if row_cols[3] != source_name or row_cols[3] == row_cols[7]:
            f.write(row)
            continue
        # check target
        # [6] is target id              [7] is target name
        if row_cols[6] not in target_name and row_cols[7] not in target_name:
            f.write(row)
            continue
        # retrieve damage
        damage_str = row_cols[9]
        if damage_str.endswith('0000'):
            damage = int(damage_str[:-4], 16)
        elif damage_str.endswith('4001'):
            damage = 65535 + int(damage_str[:-4], 16)
        elif damage_str == '0':
            print("bugged row? ")
            print(row)
            f.write(row)
            continue
        else:
            print("bugged row? ")
            print(row)
            f.write(row)
            continue
        # modify self damage
        damage *= multiplier
        # reconstruct the hex representation of damage string
        damage = int(damage)
        if damage >= 65536:
            damage_increased = '{:X}4001'.format(damage - 65535)
        elif 0 < damage <= 65535:
            damage_increased = '{:X}0000'.format(damage)
        elif damage == 0:
            print("bugged row? ")
            print(row)
            f.write(row)
            continue
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


def modify_date(path, original_date: str, target_date: str):
    # open logs file
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    splited_path = os.path.splitext(path)
    target_path = f"{splited_path[0]}_modified_date{splited_path[1]}"
    f = open(target_path, 'w', encoding='utf-8')
    # iter lines
    idx = 0
    for row in lines:
        row_cols = row.split('|')
        # handle index
        idx = int(idx)+1
        idx = str(idx)
        print(row_cols)
        if row_cols[0] == '01':
            print("reset")
            idx = str(1)
        time_str = row_cols[1]
        if original_date not in time_str:
            f.write(row)
            continue
        print(time_str)
        row_cols[1] = time_str.replace(original_date, target_date)
        text = "|".join(row_cols[:-1])
        enc_code = encrypt(text, idx)
        row_cols[-1] = enc_code + '\n'
        new_row = "|".join(row_cols)
        f.write(new_row)
        f.flush()
    f.close()


def fix_file(path):
    # open logs file
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    splited_path = os.path.splitext(path)
    target_path = f"{splited_path[0]}_fixed{splited_path[1]}"
    f = open(target_path, 'w', encoding='utf-8')
    # iter lines
    idx = 0
    for row in lines:
        row_cols = row.split('|')
        # handle index
        idx = int(idx) + 1
        idx = str(idx)
        if row_cols[0] == '01':
            idx = str(1)
            f.write(row)
            continue
        text = "|".join(row_cols[:-1])
        enc_code = encrypt(text, idx)
        row_cols[-1] = enc_code + '\n'
        new_row = "|".join(row_cols)
        f.write(new_row)
        f.flush()
    f.close()


if __name__ == '__main__':
    source_name = ''
    multiplier = 1.1
    target_name = ['鱼尾海马怪']
    # target_name = '赫斯珀洛斯'
    # modify_file('./logs_files/SplitNetwork_26404_20220501_modified-2022-05-01T05-23-35.572Z.log',
    #             source_name,
    #             multiplier,
    #             target_name)
    modify_date('./logs_files/11.log', '2022-05-02T15', '2022-05-05T20')
    main()






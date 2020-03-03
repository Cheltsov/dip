import os

import sys
import random
from bitstring import BitArray
from Cryptodome.Hash import SHA256

nb = 4  # number of coloumn of State (for AES = 4)
nr = 10  # number of rounds ib ciper cycle (if nb = 4 nr = 10)
nk = 4  # the key length (in 32-bit words)

# This dict will be used in SubBytes().
hex_symbols_to_int = {'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15}

sbox = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

inv_sbox = [
    0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
    0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
    0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
    0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
    0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
    0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
    0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
    0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
    0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
    0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
    0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
    0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
    0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
    0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
    0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
]

rcon = [[0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36],
        [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
        [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
        [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
]



class AES:

    @classmethod
    def init_encrypt(cls, key, path_file):
        input_path = os.path.abspath("media\\" + path_file)

        main_file = os.path.join(os.path.dirname(input_path), os.path.basename(input_path))

        if not os.path.exists(
                os.path.join(os.path.dirname(input_path), 'crypted\\crypted_' + os.path.basename(input_path))):

            with open(input_path, 'rb') as f:
                data = f.read()

            crypted_data = []
            temp = []
            for byte in data:
                temp.append(byte)
                if len(temp) == 16:
                    crypted_part = cls.encrypt(temp, key)
                    crypted_data.extend(crypted_part)
                    del temp[:]
            else:
                if 0 < len(temp) < 16:
                    empty_spaces = 16 - len(temp)
                    for i in range(empty_spaces - 1):
                        temp.append(0)
                    temp.append(1)
                    crypted_part = cls.encrypt(temp, key)
                    crypted_data.extend(crypted_part)

            out_path = os.path.join(os.path.dirname(input_path), 'crypted\\crypted_' + os.path.basename(input_path))
            # Ounput data
            with open(out_path, 'xb') as ff:
                ff.write(bytes(crypted_data))

            os.remove(main_file)
            return os.path.basename(out_path)
        else:
            print("Файл уже есть")
            return False

    @classmethod
    def init_decrypt(cls, key, path_file):
        input_path = os.path.abspath("media\\doc\\crypted\\" + os.path.basename(path_file))
        new_path = os.path.abspath("media\\doc\\decrypted_" + os.path.basename(path_file))

        if not os.path.exists(new_path):
            if os.path.exists(input_path):

                with open(input_path, 'rb') as f:
                    data = f.read()

                decrypted_data = []
                temp = []
                for byte in data:
                    temp.append(byte)
                    if len(temp) == 16:
                        decrypted_part = cls.decrypt(temp, key)
                        decrypted_data.extend(decrypted_part)
                        del temp[:]
                else:
                    # padding v1
                    # decrypted_data.extend(temp)

                    # padding v2
                    if 0 < len(temp) < 16:
                        empty_spaces = 16 - len(temp)
                        for i in range(empty_spaces - 1):
                            temp.append(0)
                        temp.append(1)
                        decrypted_part = cls.encrypt(temp, key)
                        decrypted_data.extend(crypted_part)

                out_path = os.path.abspath("media\\doc\\" + 'decrypted_' + os.path.basename(input_path))

                # Ounput data
                with open(out_path, 'xb') as ff:
                    ff.write(bytes(decrypted_data))
                return os.path.basename(out_path)
            else:
                print("Файл для дешифрования нет")
                return False
        else:
            print("Файл уже дешифрован")
            return False


    @classmethod
    def encrypt(cls, input_bytes, key):

        state = [[] for j in range(4)]
        for r in range(4):
            for c in range(nb):
                state[r].append(input_bytes[r + 4 * c])

        key_schedule = cls.key_expansion(key)

        state = cls.add_round_key(state, key_schedule)

        for rnd in range(1, nr):
            state = cls.sub_bytes(state)
            state = cls.shift_rows(state)
            state = cls.mix_columns(state)
            state = cls.add_round_key(state, key_schedule, rnd)

        state = cls.sub_bytes(state)
        state = cls.shift_rows(state)
        state = cls.add_round_key(state, key_schedule, rnd + 1)

        output = [None for i in range(4 * nb)]
        for r in range(4):
            for c in range(nb):
                output[r + 4 * c] = state[r][c]

        return output

    @classmethod
    def decrypt(cls, cipher, key):
        state = [[] for i in range(nb)]
        for r in range(4):
            for c in range(nb):
                state[r].append(cipher[r + 4 * c])

        key_schedule = cls.key_expansion(key)

        state = cls.add_round_key(state, key_schedule, nr)

        rnd = nr - 1
        while rnd >= 1:
            state = cls.shift_rows(state, inv=True)
            state = cls.sub_bytes(state, inv=True)
            state = cls.add_round_key(state, key_schedule, rnd)
            state = cls.mix_columns(state, inv=True)

            rnd -= 1

        state = cls.shift_rows(state, inv=True)
        state = cls.sub_bytes(state, inv=True)
        state = cls.add_round_key(state, key_schedule, rnd)

        output = [None for i in range(4 * nb)]
        for r in range(4):
            for c in range(nb):
                output[r + 4 * c] = state[r][c]

        return output

    @staticmethod
    def sub_bytes(state, inv=False):
        if inv == False:  # encrypt
            box = sbox
        else:  # decrypt
            box = inv_sbox

        for i in range(len(state)):
            for j in range(len(state[i])):
                row = state[i][j] // 0x10
                col = state[i][j] % 0x10
                box_elem = box[16 * row + col]
                state[i][j] = box_elem
        return state

    @classmethod
    def shift_rows(cls, state, inv=False):
        count = 1
        if inv == False:  # encrypting
            for i in range(1, nb):
                state[i] = cls.left_shift(state[i], count)
                count += 1
        else:  # decryptionting
            for i in range(1, nb):
                state[i] = cls.right_shift(state[i], count)
                count += 1
        return state

    @classmethod
    def mix_columns(cls, state, inv=False):
        for i in range(nb):

            if inv == False:  # encryption
                s0 = cls.mul_by_02(state[0][i]) ^ cls.mul_by_03(state[1][i]) ^ state[2][i] ^ state[3][i]
                s1 = state[0][i] ^ cls.mul_by_02(state[1][i]) ^ cls.mul_by_03(state[2][i]) ^ state[3][i]
                s2 = state[0][i] ^ state[1][i] ^ cls.mul_by_02(state[2][i]) ^ cls.mul_by_03(state[3][i])
                s3 = cls.mul_by_03(state[0][i]) ^ state[1][i] ^ state[2][i] ^ cls.mul_by_02(state[3][i])
            else:  # decryption
                s0 = cls.mul_by_0e(state[0][i]) ^ cls.mul_by_0b(state[1][i]) ^ cls.mul_by_0d(state[2][i]) ^ cls.mul_by_09(state[3][i])
                s1 = cls.mul_by_09(state[0][i]) ^ cls.mul_by_0e(state[1][i]) ^ cls.mul_by_0b(state[2][i]) ^ cls.mul_by_0d(state[3][i])
                s2 = cls.mul_by_0d(state[0][i]) ^ cls.mul_by_09(state[1][i]) ^ cls.mul_by_0e(state[2][i]) ^ cls.mul_by_0b(state[3][i])
                s3 = cls.mul_by_0b(state[0][i]) ^ cls.mul_by_0d(state[1][i]) ^ cls.mul_by_09(state[2][i]) ^ cls.mul_by_0e(state[3][i])

            state[0][i] = s0
            state[1][i] = s1
            state[2][i] = s2
            state[3][i] = s3

        return state

    @staticmethod
    def key_expansion(key):
        key_symbols = [ord(symbol) for symbol in key]

        # ChipherKey shoul contain 16 symbols to fill 4*4 table. If it's less
        # complement the key with "0x01"
        if len(key_symbols) < 4 * nk:
            for i in range(4 * nk - len(key_symbols)):
                key_symbols.append(0x01)

        # make ChipherKey(which is base of KeySchedule)
        key_schedule = [[] for i in range(4)]
        for r in range(4):
            for c in range(nk):
                key_schedule[r].append(key_symbols[r + 4 * c])

        # Comtinue to fill KeySchedule
        for col in range(nk, nb * (nr + 1)):  # col - column number
            if col % nk == 0:
                # take shifted (col - 1)th column...
                tmp = [key_schedule[row][col - 1] for row in range(1, 4)]
                tmp.append(key_schedule[0][col - 1])

                # change its elements using Sbox-table like in SubBytes...
                for j in range(len(tmp)):
                    sbox_row = tmp[j] // 0x10
                    sbox_col = tmp[j] % 0x10
                    sbox_elem = sbox[16 * sbox_row + sbox_col]
                    tmp[j] = sbox_elem

                # and finally make XOR of 3 columns
                for row in range(4):
                    s = (key_schedule[row][col - 4]) ^ (tmp[row]) ^ (rcon[row][int(col / nk - 1)])
                    key_schedule[row].append(s)

            else:
                # just make XOR of 2 columns
                for row in range(4):
                    s = key_schedule[row][col - 4] ^ key_schedule[row][col - 1]
                    key_schedule[row].append(s)

        return key_schedule

    @classmethod
    def add_round_key(cls, state, key_schedule, round=0):
        for col in range(nk):
            # nb*round is a shift which indicates start of a part of the KeySchedule
            s0 = state[0][col] ^ key_schedule[0][nb * round + col]
            s1 = state[1][col] ^ key_schedule[1][nb * round + col]
            s2 = state[2][col] ^ key_schedule[2][nb * round + col]
            s3 = state[3][col] ^ key_schedule[3][nb * round + col]

            state[0][col] = s0
            state[1][col] = s1
            state[2][col] = s2
            state[3][col] = s3

        return state

    @staticmethod
    def left_shift(array, count):
        """Rotate the array over count times"""

        res = array[:]
        for i in range(count):
            temp = res[1:]
            temp.append(res[0])
            res[:] = temp[:]

        return res

    @staticmethod
    def right_shift(array, count):
        """Rotate the array over count times"""
        res = array[:]
        for i in range(count):
            tmp = res[:-1]
            tmp.insert(0, res[-1])
            res[:] = tmp[:]
        return res

    @staticmethod
    def mul_by_02(num):
        if num < 0x80:
            res = (num << 1)
        else:
            res = (num << 1) ^ 0x1b
        return res % 0x100

    @classmethod
    def mul_by_03(cls, num):
        return (cls.mul_by_02(num) ^ num)

    @classmethod
    def mul_by_09(cls, num):
        # return mul_by_03(num)^mul_by_03(num)^mul_by_03(num) - works wrong, I don't know why
        return cls.mul_by_02(cls.mul_by_02(cls.mul_by_02(num))) ^ num

    @classmethod
    def mul_by_0b(cls, num):
        # return mul_by_09(num)^mul_by_02(num)
        return cls.mul_by_02(cls.mul_by_02(cls.mul_by_02(num))) ^ cls.mul_by_02(num) ^ num

    @classmethod
    def mul_by_0d(cls, num):
        # return mul_by_0b(num)^mul_by_02(num)
        return cls.mul_by_02(cls.mul_by_02(cls.mul_by_02(num))) ^ cls.mul_by_02(cls.mul_by_02(num)) ^ num

    @classmethod
    def mul_by_0e(cls, num):
        # return mul_by_0d(num)^num
        return cls.mul_by_02(cls.mul_by_02(cls.mul_by_02(num))) ^ cls.mul_by_02(cls.mul_by_02(num)) ^ cls.mul_by_02(num)


class DES:

    # Various items stored as class variables. This may be an artifact of my early days
    # as a Java programmer, but in certain cases I preferred to use a class variable
    # rather than pass lots of variables back and forth between methods. If this were
    # "production", I feel like I would probably want to take more steps to obscure or hide the
    # key when it's in memory, but for this, I decided not to worry about that part.
    def __init__(self):
        self.key = BitArray()
        self.roundKeys = list()
        self.setLookupTables()

        # I set most of the lookup tables as class variables so that I only have to do it once, on

    # instantiation of the class, and they're accessible across methods.
    def setLookupTables(self):
        # This is the initial permutation of the key
        self.INITIAL_P = [58, 50, 42, 34, 26, 18, 10, 2,
                          60, 52, 44, 36, 28, 20, 12, 4,
                          62, 54, 46, 38, 30, 22, 14, 6,
                          64, 56, 48, 40, 32, 24, 16, 8,
                          57, 49, 41, 33, 25, 17, 9, 1,
                          59, 51, 43, 35, 27, 19, 11, 3,
                          61, 53, 45, 37, 29, 21, 13, 5,
                          63, 55, 47, 39, 31, 23, 15, 7]

        # Permutation to be used to generate each 48-bit key
        self.ROUND_P = [14, 17, 11, 24, 1, 5, 3, 28,
                        15, 6, 21, 10, 23, 19, 12, 4,
                        26, 8, 16, 7, 27, 20, 13, 2,
                        41, 52, 31, 37, 47, 55, 30, 40,
                        51, 45, 33, 48, 44, 49, 39, 56,
                        34, 53, 46, 42, 50, 36, 29, 32]

        # Left shift to be applied to each of the sixteen round keys
        self.roundShift = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

        # The eight DES S-Boxes
        self.S_BOX = [
            [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
             [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
             [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
             [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
             ],

            [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
             [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
             [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
             [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
             ],

            [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
             [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
             [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
             [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
             ],

            [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
             [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
             [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
             [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
             ],

            [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
             [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
             [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
             [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
             ],

            [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
             [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
             [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
             [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
             ],

            [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
             [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
             [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
             [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
             ],

            [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
             [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
             [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
             [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
             ]
        ]

        # Expansion permutation used to expand a 32-bit segment to 48 bits
        self.EXPANSION_P = [32, 1, 2, 3, 4, 5,
                            4, 5, 6, 7, 8, 9,
                            8, 9, 10, 11, 12, 13,
                            12, 13, 14, 15, 16, 17,
                            16, 17, 18, 19, 20, 21,
                            20, 21, 22, 23, 24, 25,
                            24, 25, 26, 27, 28, 29,
                            28, 29, 30, 31, 32, 1]

        # P-Box Permutation
        self.P_BOX = [16, 7, 20, 21, 29, 12, 28, 17,
                      1, 15, 23, 26, 5, 18, 31, 10,
                      2, 8, 24, 14, 32, 27, 3, 9,
                      19, 13, 30, 6, 22, 11, 4, 25]

        self.P_FINAL = [40, 8, 48, 16, 56, 24, 64, 32,
                        39, 7, 47, 15, 55, 23, 63, 31,
                        38, 6, 46, 14, 54, 22, 62, 30,
                        37, 5, 45, 13, 53, 21, 61, 29,
                        36, 4, 44, 12, 52, 20, 60, 28,
                        35, 3, 43, 11, 51, 19, 59, 27,
                        34, 2, 42, 10, 50, 18, 58, 26,
                        33, 1, 41, 9, 49, 17, 57, 25]

        # Function to permute the bits of a starting array based on a given lookup table

    def permuteBits(self, inputBits, table):
        permuted = BitArray()
        count = 0
        # Go through the lookup table in order
        for x in table:
            # And append the bit at the given location of the initial array
            permuted.append(inputBits[(x - 1):x])
            count = count + 1
        # At the end, you have an array of bits permuted as dictated by the lookup table
        return permuted

        # Method to create the keyfile from an initial 192-bit key

    # The 192-bit key contains the 3 starting 64-bit keys in sequential order
    def createKeyFile(self, initialKey, filename):

        # Lookup table to be used in permuting the key from 64 to 56 bits
        # In "real" DES, the deleted bits are parity-checking bits, but this is
        # just a demo/simulation.
        KEY_P = [57, 49, 41, 33, 25, 17, 9,
                 1, 58, 50, 42, 34, 26, 18,
                 10, 2, 59, 51, 43, 35, 27,
                 19, 11, 3, 60, 52, 44, 36,
                 63, 55, 47, 39, 31, 23, 15,
                 7, 62, 54, 46, 38, 30, 22,
                 14, 6, 61, 53, 45, 37, 29,
                 21, 13, 5, 28, 20, 12, 4]

        keyCount = 0
        keyWriter = open(filename, 'w')

        # Loop 3 times, each time taking the next 64-bit key and permuting it the 56-bit DES key
        while keyCount < 192:
            subKey = initialKey[keyCount:(keyCount + 64)]
            subKey = self.permuteBits(subKey, KEY_P)

            # After permuting, write 56-bit key to the keyfile
            # Written as a string of 1s and 0s rather than a literal bit sequence to aid in debugging
            keyWriter.write(subKey.bin)
            keyCount = keyCount + 64

        keyWriter.closed

    # Method to read in the keyfile, where the keyfile is a string of 168 0s and 1s
    def readKeyFile(self, filename):

        keyReader = open(filename, 'r')
        self.key = BitArray(bin=keyReader.read())

    # Method to generate 16 round keys, based on an initial 56-bit key
    def roundKeyGen(self, initialKey, operation):

        cKey = BitArray()
        dKey = BitArray()
        self.roundKeys = list()

        for roundCount in range(0, 16):
            # Split 56-bit key into C and D
            cKey = initialKey[0:28]
            dKey = initialKey[28:56]

            # Rotate to the left by the amount appropriate for each round
            cKey.rol(self.roundShift[roundCount])
            dKey.rol(self.roundShift[roundCount])

            # Put them back together for the 56-bit key
            cKey.append(dKey)
            initialKey = cKey
            # The 48-bit permutation is calculated and stored in the list of round keys
            # The 56-bit key is kept and saved to calculate the next round key
            self.roundKeys.append(self.permuteBits(initialKey, self.ROUND_P))

        # If we're doing a decryption we need to run the round keys in reverse order.
        if (operation == 'DECRYPT'):

            roundKeyReversal = list()
            i = 0

            for i in range(0, 16):
                roundKeyReversal.append(self.roundKeys[15 - i])

            self.roundKeys = roundKeyReversal

    def encrypt(self, infile, outfile, mode):
        # If encryption, we run the triple DES algorithm with operation set to 'ENCRYPT'
        self.runTripleDes(infile, outfile, mode, 'ENCRYPT')

    def decrypt(self, infile, outfile, mode):
        # If decryption, we run the triple DES algorithm with operation set to 'DECRYPT'
        self.runTripleDes(infile, outfile, mode, 'DECRYPT')

    def runTripleDes(self, infile, outfile, mode, operation):

        inputRead = open(infile, 'r')
        stringToProcess = inputRead.read()
        # If reading from unencrypted text file, then file input will be a standard string
        # Otherwise it will be a hex string
        if (operation == 'ENCRYPT'):
            inputBits = BitArray(bytes=stringToProcess.encode('utf8'))
            inputBits = self.bufferInput(inputBits)
        elif (operation == 'DECRYPT'):
            inputBits = BitArray(hex=stringToProcess)

            # If decrypting, you will need to use the last key (K3) and the first key (K1) third.
            # So just reverse the order of the 3 56-bit subkeys in the overall 168-bit key.
            #
            # This does not apply to OFB, which treats encryption and decryption the same.
            if (mode != 'OFB'):
                keyReverse = BitArray()
                j = 0
                for j in range(0, 3):
                    readFrom = 112 - (j * 56)
                    keyReverse.append(self.key[readFrom:(readFrom + 56)])
                self.key = keyReverse

        # position will track our progress through the input bits
        position = 0
        # outputBits is where we're going to store the finished output and will
        # eventually write it to the output file.
        outputBits = BitArray()

        # For CBC and OFB modes we need to set an initialization vector.
        if (mode != 'ECB'):

            # If encrypting, generate a new 64 bit random string.
            if (operation == 'ENCRYPT'):

                # xorVector will store the initialization vector here
                # During triple DES it will keep storing the value to use for XORing in the next round
                xorVector = BitArray()
                # Leaving the seed argument blank seeds rand with the time
                random.seed()
                randomNum = random.getrandbits(64)

                # Convert random integer to 64-bit bitstring
                xorVector = BitArray(uint=randomNum, length=64)
                # Append to the beginning of the output string, so IV will be the first
                # 64 bits of the file
                outputBits.append(xorVector)

            elif (operation == 'DECRYPT'):
                # If decrypting, the first 64 bits of the input is the IV. Read in, store,
                # and delete it from the input.
                xorVector = inputBits[0:64]
                del inputBits[:64]

                # This is the loop that actually cycles through each 64 bits of the input.
        while position < inputBits.length:

            # unProcessedBits stores the next 64 bit input from the file.
            # It's plaintext if encrypting, ciphertext if decrypting.
            unprocessedBits = inputBits[position:(position + 64)]

            # If CBC our input into the encryption will be the XOR Vector from the previous round
            # (or IV if the first round) XORed with the plaintext from file
            if (mode == 'CBC'):
                if (operation == 'ENCRYPT'):
                    segmentInput = unprocessedBits ^ xorVector
                # For CBC decryption our input into the encryption is ciphertext
                else:
                    segmentInput = unprocessedBits
                    # In OFB mode (encryption or decryption) input is the result of the XOR from the previous round.
            elif (mode == 'OFB'):
                segmentInput = xorVector
            # In ECB mode (encryption or decryption), our input just the plaintext (encryption) or ciphertext (decryption)
            else:
                segmentInput = unprocessedBits

            # If OFB, decryption runs the same as encryption.
            if (mode == 'OFB'):
                processedBits = self.tripleDesSegment(segmentInput, 'ENCRYPT')
            # Else let the triple DES algorithm know if it's encrypting or decrypting
            else:
                # The triple DES segment method is what actually does the round key
                # generation and processing for each 64 bit segment
                processedBits = self.tripleDesSegment(segmentInput, operation)

            # For OFB mode
            if (mode == 'OFB'):
                # The output from this round of 3DES is stored as the XOR vector for the next round
                xorVector = processedBits
                # Final output of this cycle is an XOR of the 3DES output and the
                # unprocessed file input (plaintext if encrypting, ciphertext if decrypting).
                segmentOutput = unprocessedBits ^ processedBits
            # For CBC mode
            elif (mode == 'CBC'):
                # On encryption, both final output (ciphertext) and XOR vector for next round are the
                # output from this round of 3DES.
                if (operation == 'ENCRYPT'):
                    xorVector = processedBits
                    segmentOutput = processedBits
                    # For decryption, final output is an XOR of output from this round of 3DES
                # and ciphertext from previous round.
                if (operation == 'DECRYPT'):
                    segmentOutput = processedBits ^ xorVector
                    # For next round, store xorVector as ciphertext from this round
                    xorVector = unprocessedBits
            # If ECB
            else:
                # Final output is the direct output from 3DES algorithm
                segmentOutput = processedBits

            # Append final output to string of output bits
            outputBits.append(segmentOutput)
            # Increment position for the next round of 3DES
            position = position + 64

        # After 3DES is done, write output
        outputWriter = open(outfile, 'w')

        # If the overall operation was an encrypt, we're writing out an encrypted hex string
        if (operation == 'ENCRYPT'):
            outputWriter.write(outputBits.hex)
        # If the overall operation was a decrypt, we're writing out a cleartext string.
        elif (operation == 'DECRYPT'):
            # Remove the buffer that was originally added to make sure the input
            # was divisible by 64 bits
            bitsToProcess = self.removeBuffer(outputBits)
            outputWriter.write((bitsToProcess.bytes).decode('utf8'))

    # Runs Triple DES on a given bit string, for the given operation and mode.
    def tripleDesSegment(self, bitsToProcess, oper):

        i = 0
        # For Triple DES, repeat the DES process 3 times
        for i in range(0, 3):
            # Grab the next 56-bit portion of the 168-bit key.
            stepKey = self.key[(56 * i):((56 * i) + 56)]
            # Generate the 16 48-bit round keys off the 56-bit key
            self.roundKeyGen(stepKey, oper)

            # Run DES on the input string. The keys are stored in class variables, and set
            # in the appropriate order for encryption or decryption by the generator method.
            bitsToProcess = self.runSixteenRounds(bitsToProcess)

            # Flip between encryption and decryption on every round but the last
            if (i != 2):
                if (oper == 'ENCRYPT'):
                    oper = 'DECRYPT'
                elif (oper == 'DECRYPT'):
                    oper = 'ENCRYPT'

        return bitsToProcess

    # Method to buffer the input string so the number of bits to encrypt is
    # evenly divisible by 64
    def bufferInput(self, inputBits):

        length = inputBits.length
        # Get the modulus of the input string length at 64
        amtToBuffer = length % 64
        # If length is not evenly divisible by 64, then the amount
        # we need to buffer is actually (64 - modulus)
        if (amtToBuffer > 0):
            amtToBuffer = 64 - amtToBuffer

        # Append the appropriate hex string based on the amount of buffer needed
        if (amtToBuffer == 8):
            inputBits.append('0x01')
        elif (amtToBuffer == 16):
            inputBits.append('0x0202')
        elif (amtToBuffer == 24):
            inputBits.append('0x030303')
        elif (amtToBuffer == 32):
            inputBits.append('0x04040404')
        elif (amtToBuffer == 40):
            inputBits.append('0x0505050505')
        elif (amtToBuffer == 48):
            inputBits.append('0x060606060606')
        elif (amtToBuffer == 56):
            inputBits.append('0x07070707070707')

        return inputBits

    # Method to remove hex buffer after decryption, if one is present
    def removeBuffer(self, inputBits):

        # Check the last byte. If it's part of a buffer, crop the necessary length
        # from the string
        testByte = inputBits[(inputBits.length - 8):inputBits.length]
        if (testByte == '0x07'):
            del inputBits[-56:]
        elif (testByte == '0x06'):
            del inputBits[-48:]
        elif (testByte == '0x05'):
            del inputBits[-40:]
        elif (testByte == '0x04'):
            del inputBits[-32:]
        elif (testByte == '0x03'):
            del inputBits[-24:]
        elif (testByte == '0x02'):
            del inputBits[-16:]
        elif (testByte == '0x01'):
            del inputBits[-8:]

        return inputBits

    # Method to process the next 64-bit segment of plaintext
    def runSixteenRounds(self, inputBits):

        # Do initial permutation on the plaintext
        inputBits = self.permuteBits(inputBits, self.INITIAL_P)

        # Split into L0 and R0
        leftBits = inputBits[0:32]
        rightBits = inputBits[32:64]

        # Do 16 rounds of encryption/decryption
        for roundCount in range(0, 16):
            # Permute the 32 bits of R0 into 48
            expandedBits = self.permuteBits(rightBits, self.EXPANSION_P)

            # XOR the right bits and the round key
            result = expandedBits ^ self.roundKeys[roundCount]

            # Run the SBoxes on the result of the right bits/round key XOR
            result = self.sBoxes(result)
            # Do a PBox permutation
            result = self.permuteBits(result, self.P_BOX)
            # XOR the result with the left side
            result = result ^ leftBits

            # Swap the left and right if it's not the last round
            if (roundCount < 15):
                leftBits = rightBits
                rightBits = result
            else:
                leftBits = result

        # After 16 rounds, concatenate left and right sides
        cText = leftBits
        cText.append(rightBits)

        # Do final permutation
        cText = self.permuteBits(cText, self.P_FINAL)

        return cText

        # Method to run the S-Box substitutions for a single round

    def sBoxes(self, inputString):

        outputString = BitArray()

        sBoxIncrement = 0
        # 8 SBoxes
        for sBoxIncrement in range(0, 8):
            # Take the next 6 characters of the input string
            currentPos = sBoxIncrement * 6
            currentBits = inputString[currentPos:(currentPos + 6)]
            # The four inner bits are the column lookup
            innerBits = currentBits[1:5]
            # The two outer bits are the row lookup
            outerBits = currentBits[0:1]
            outerBits.append(currentBits[5:6])
            # Find the correct substitution in the SBox and append the bit representation to the output string
            nextSegment = BitArray(uint=self.S_BOX[sBoxIncrement][outerBits.uint][innerBits.uint], length=4)
            outputString.append(nextSegment)

        return outputString

    # Option 1: Key Generation


from GF_2_4 import *


# noinspection PyMethodMayBeStatic
class S_ASE(object):
    def __init__(self, key):
        self.key0 = key
        self.key1 = None
        self.key2 = None
        self.S_Box = [
            [0x9, 0x4, 0xA, 0xB],
            [0xD, 0x1, 0x8, 0x5],
            [0x6, 0x2, 0x0, 0x3],
            [0xC, 0xE, 0xF, 0x7]
        ]
        self.inv_S_Box = [
            [0xA, 0x5, 0x9, 0xB],
            [0x1, 0x7, 0x8, 0xF],
            [0x6, 0x0, 0x2, 0x3],
            [0xC, 0x4, 0xD, 0xE]
        ]

    def to_nibble_matrix(self, bitstring):
        if len(bitstring) != 16:
            raise ValueError("输入比特串必须是16位")

        nibble_matrix = [[0, 0], [0, 0]]

        for i in range(2):
            for j in range(2):
                start_index = 8 * i + 4 * j
                nibble = bitstring[start_index:start_index + 4]
                nibble_matrix[j][i] = int(nibble, 2)

        return nibble_matrix

    def Add_Key(self, key, nibble_matrix):
        # print(nibble_matrix)
        # 执行逐半字节异或操作
        s00 = nibble_matrix[0][0] ^ self.to_nibble_matrix(key)[0][0]
        s01 = nibble_matrix[0][1] ^ self.to_nibble_matrix(key)[0][1]
        s10 = nibble_matrix[1][0] ^ self.to_nibble_matrix(key)[1][0]
        s11 = nibble_matrix[1][1] ^ self.to_nibble_matrix(key)[1][1]
        # 将结果转换为二进制字符串, [2:] 用于去除结果中的 '0b' 前缀
        return [[s00, s01], [s10, s11]]

    def Nibble_Substitution(self, nibble_matrix, inv=False):
        # print(nibble_matrix)
        result = [[0, 0], [0, 0]]
        if not inv:
            for i in range(2):
                for j in range(2):
                    nibble = nibble_matrix[i][j]
                    bits = bin(nibble)[2:].zfill(4)
                    result[i][j] = self.S_Box[int(bits[0:2], 2)][int(bits[2:4], 2)]
        else:
            for i in range(2):
                for j in range(2):
                    nibble = nibble_matrix[i][j]
                    bits = bin(nibble)[2:].zfill(4)
                    result[i][j] = self.inv_S_Box[int(bits[0:2], 2)][int(bits[2:4], 2)]
        return result

    def Shift_Row(self, nibble_matrix):
        # print(nibble_matrix)
        nibble_matrix[1][0], nibble_matrix[1][1] = nibble_matrix[1][1], nibble_matrix[1][0]
        return nibble_matrix

    def Mix_Column(self, nibble_matrix, inv=False):
        # print(nibble_matrix)
        result = [[0, 0], [0, 0]]
        if not inv:
            result[0][0] = GF2_4_add(nibble_matrix[0][0], GF2_4_multiply(4, nibble_matrix[1][0]))
            result[0][1] = GF2_4_add(nibble_matrix[0][1], GF2_4_multiply(4, nibble_matrix[1][1]))
            result[1][0] = GF2_4_add(GF2_4_multiply(4, nibble_matrix[0][0]), nibble_matrix[1][0])
            result[1][1] = GF2_4_add(GF2_4_multiply(4, nibble_matrix[0][1]), nibble_matrix[1][1])
        else:
            result[0][0] = GF2_4_add(GF2_4_multiply(9, nibble_matrix[0][0]), GF2_4_multiply(2, nibble_matrix[1][0]))
            result[0][1] = GF2_4_add(GF2_4_multiply(9, nibble_matrix[0][1]), GF2_4_multiply(2, nibble_matrix[1][1]))
            result[1][0] = GF2_4_add(GF2_4_multiply(2, nibble_matrix[0][0]), GF2_4_multiply(9, nibble_matrix[1][0]))
            result[1][1] = GF2_4_add(GF2_4_multiply(2, nibble_matrix[0][1]), GF2_4_multiply(9, nibble_matrix[1][1]))
        return result

    def key_extension(self):
        def RotNib(w):
            N1 = w & 0x0F
            N0 = (w >> 4) & 0x0F
            return (N1 << 4) | N0

        def SubNib(w):
            N1 = bin(w & 0x0F)[2:].zfill(4)
            N1 = self.S_Box[int(N1[0:2], 2)][int(N1[2:4], 2)]
            N0 = bin((w >> 4) & 0x0F)[2:].zfill(4)
            N0 = self.S_Box[int(N0[0:2], 2)][int(N0[2:4], 2)]
            return (N0 << 4) | N1

        w0, w1 = int(self.key0[0:8], 2), int(self.key0[8:16], 2)
        w2 = w0 ^ 0b10000000 ^ SubNib(RotNib(w1))
        w3 = w2 ^ w1
        w4 = w2 ^ 0b00110000 ^ SubNib(RotNib(w3))
        w5 = w4 ^ w3
        # print(w0, w1, w2, w3, w4, w5)
        self.key1 = bin((w2 << 8) | w3)[2:].zfill(16)
        # print(self.key1)
        self.key2 = bin((w4 << 8) | w5)[2:].zfill(16)
        # print(self.key2)

    def to_str(self, nibble_matrix):
        binary_string = ""
        for row in nibble_matrix:
            for element in row:
                binary_element = bin(element)[2:].zfill(4)
                binary_string += binary_element
        return binary_string

    def encrypt(self, plain_text):
        self.key_extension()
        cypher_text = self.Add_Key(
            self.key2, self.Shift_Row(
                self.Nibble_Substitution(
                    self.Add_Key(
                        self.key1, self.Mix_Column(
                            self.Shift_Row(
                                self.Nibble_Substitution(
                                    self.Add_Key(
                                        self.key0, self.to_nibble_matrix(plain_text))
                                ))
                        ))
                ))
        )
        return self.to_str(cypher_text)

    def decrypt(self, cypher_text):
        self.key_extension()
        plain_text = self.Add_Key(
            self.key0, self.Nibble_Substitution(
                self.Shift_Row(
                    self.Mix_Column(
                        self.Add_Key(
                            self.key1, self.Nibble_Substitution(
                                self.Shift_Row(
                                    self.Add_Key(
                                        self.key2, self.to_nibble_matrix(cypher_text))
                                ), inv=True)
                        ), inv=True)
                ), inv=True)
        )
        return self.to_str(plain_text)


if __name__ == '__main__':
    key = '0010110101010101'
    print(f'key = {key}')
    S_ASE = S_ASE(key)

    plain_text = '1010011101001001'
    print(f'plain_text  = {plain_text}')
    cypher_text = S_ASE.encrypt(plain_text)
    print(f'cypher_text = {cypher_text}')
    decryption = S_ASE.decrypt(cypher_text)
    print(f'decryption  = {decryption}')

import S_AES
import random

iv = random.randint(0, 2 ** 16 - 1)


class CBC:
    def __init__(self, key):
        self.key = key
        self.iv = iv

    def encrypt(self, plaintext):
        plain_text = []
        length = (len(plaintext) // 16)
        for i in range(0, length):
            plt = plaintext[16 * i:16 * (i + 1)]
            plain_text.append(plt)
        S = S_AES.S_AES(self.key)
        cyper_text = [S.encrypt(format(self.iv ^ int(plain_text[0], 2), '016b'))]
        for i in range(1, length):
            cyper_text.append(S.encrypt(format(int(cyper_text[i - 1], 2) ^ int(plain_text[i], 2), '016b')))
        return cyper_text

    def decrypt(self, cyphertext):
        cyper_text = []
        length = (len(cyphertext) // 16)
        for i in range(0, length):
            plt = cyphertext[16 * i:16 * (i + 1)]
            cyper_text.append(plt)
        S = S_AES.S_AES(self.key)
        plain_text = [format(self.iv ^ int(S.decrypt(cyper_text[0]), 2), '016b')]
        for i in range(1, length):
            plain_text.append(format(int(cyper_text[i - 1], 2) ^ int(S.decrypt(cyper_text[i]), 2), '016b'))
        return plain_text


if __name__ == '__main__':
    key = '1010101010101010'
    C = CBC(key=key)
    plaintext = '10100101101001011111000011110000'
    cyper_text = C.encrypt(plaintext)
    print(cyper_text)
    print(C.decrypt(cyper_text[0] + cyper_text[1]))

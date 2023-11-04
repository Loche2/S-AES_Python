def GF2_4_add(a, b):
    if a < 0 or a >= 16 or b < 0 or b >= 16:
        raise ValueError("输入必须是0到15之间的整数")

    result = a ^ b
    return result


def GF2_4_multiply(a, b):
    if a < 0 or a >= 16 or b < 0 or b >= 16:
        raise ValueError("输入必须是0到15之间的整数")

    result = 0
    for i in range(4):
        if b & 1:
            result ^= a
        a <<= 1
        if a & 0b10000:
            a ^= 0b10011
        b >>= 1

    result &= 0b1111
    return result


if __name__ == '__main__':
    a = 4
    b = 12
    print(GF2_4_add(a, b))
    print(GF2_4_multiply(a, b))

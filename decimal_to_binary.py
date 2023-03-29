# Written by chatGPT

def decimal_to_binary(num):
    """
    将十进制数转换为32位二进制浮点格式
    """
    # 检查数字是否为零
    if num == 0:
        return '0'*32

    # 检查数字是否为负数
    sign = 0
    if num < 0:
        sign = 1
        num = abs(num)

    # 计算指数位数
    exp = 0
    while num >= 2:
        num /= 2
        exp += 1
    while num < 1:
        num *= 2
        exp -= 1

    # 调整指数范围
    exp += 127
    if exp < 0:
        exp = 0
    elif exp > 255:
        exp = 255

    # 转换尾数
    frac = ""
    num -= 1
    for i in range(23):
        num *= 2
        if num >= 1:
            frac += '1'
            num -= 1
        else:
            frac += '0'

    # 将二进制字符串拼接起来
    sign_bit = str(sign)
    exp_bits = format(exp, '08b')
    frac_bits = frac.ljust(23, '0')
    binary = sign_bit + exp_bits + frac_bits

    return binary


if __name__ == "__main__":
    a = eval(input())
    print(decimal_to_binary(a))

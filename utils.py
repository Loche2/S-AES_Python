import re

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
from qfluentwidgets import InfoBar, InfoBarPosition


def to_16bits(txt):
    return [txt[i:i+16] for i in range(0, len(txt), 16)]


def is_bin(s):
    # 使用正则表达式匹配字符串是否只包含 "0" 和 "1"
    pattern = r'^[01]+$'
    return bool(re.match(pattern, s))


def str2asc(input_string):
    if len(input_string) % 2 != 0:
        input_string += ' '
    # 使用列表推导将字符串中的字符转换为它们的ASCII码值的二进制表示，并将结果连接成字符串
    bin_ascii_values = [format(ord(char), '08b') for char in input_string]
    return ''.join(bin_ascii_values)


def asc2str(binary_ascii_string):
    # 从连续的8位二进制值中提取每个二进制表示，然后将其转换为字符
    binary_values = [binary_ascii_string[i:i + 8] for i in range(0, len(binary_ascii_string), 8)]
    original_string = ''.join([chr(int(binary, 2)) for binary in binary_values])
    return original_string


def showErrorInfoBar(parent, text):
    InfoBar.error(
        title='警告',
        content=text,
        orient=Qt.Horizontal,
        isClosable=False,  # disable close button
        position=InfoBarPosition.BOTTOM_RIGHT,
        duration=2000,
        parent=parent
    )


def openWebsite(url):
    QDesktopServices.openUrl(QUrl(url))

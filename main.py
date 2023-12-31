# from PyQt5 import uic
from PyQt5.QtWidgets import *
from qfluentwidgets import FluentIcon

from CBC import CBC
from cracker import Cracker
from two_fold_S_AES import two_fold_S_AES, treble_S_AES
from ui_main import Ui_Form
from S_AES import S_AES
from utils import *


# class Main():
# noinspection PyArgumentList
class Main(QWidget):
    def __init__(self):
        # 从UI定义中动态加载窗口对象
        # self.ui = uic.loadUi("Forms/main.ui")
        # 从文件中加载UI定义
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.cracker = None

        self.resize(400, 600)

        self.ui.rBtn_Bin.setChecked(True)
        self.ui.lineEdit_Key.setClearButtonEnabled(True)

        self.ui.pBtn_Github.setIcon(FluentIcon.GITHUB)
        self.ui.pBtn_Github.clicked.connect(lambda: openWebsite("https://github.com/Loche2/S-AES_Python"))
        self.ui.tBtn_Issue.setIcon(FluentIcon.FEEDBACK)
        self.ui.tBtn_Issue.setToolTip('提供反馈')
        self.ui.tBtn_Issue.setToolTipDuration(-1)
        self.ui.tBtn_Issue.clicked.connect(lambda: openWebsite("https://github.com/Loche2/S-AES_Python/issues"))

        self.ui.comboBox_Multi_Encrypt.addItems(['一重加密', '双重加密', '三重加密'])
        self.ui.comboBox_Multi_Encrypt.setCurrentIndex(0)

        self.ui.pBtn_Encrypt.clicked.connect(self.encrypt)
        self.ui.pBtn_Decrypt.clicked.connect(self.decrypt)
        self.ui.pBtn_Crack.clicked.connect(self.openCracker)
        self.ui.sBtn_CBC.checkedChanged.connect(self.off_multi)

    def encrypt(self):
        self.ui.cypherTextEdit.clear()
        key = self.ui.lineEdit_Key.text()
        plain_txt = self.ui.plainTextEdit.toPlainText()

        if self.ui.rBtn_Str.isChecked():
            plain_txt = str2asc(plain_txt)

        # 异常处理：
        if not plain_txt.strip():  # 使用strip()方法移除前后的空白字符并检查文本是否为空
            showErrorInfoBar(self, '明文为空，请输入')
            return
        if len(plain_txt) % 16 != 0 or not is_bin(plain_txt):
            showErrorInfoBar(self, '明文不是16-bit，请查证后再输入')
            return

        if self.ui.comboBox_Multi_Encrypt.currentText() == '一重加密':
            if len(self.ui.lineEdit_Key.text()) != 16 or not is_bin(self.ui.lineEdit_Key.text()):
                showErrorInfoBar(self, '一重加密时密钥仅能为16位比特串')
                return
            if self.ui.sBtn_CBC.isChecked():
                CBC_S_AES = CBC(key=key)
                cypher_txt = CBC_S_AES.encrypt(plain_txt)
                cypher_txt = ''.join(cypher_txt)
                self.ui.cypherTextEdit.insertPlainText(cypher_txt)
            else:
                m_S_AES = S_AES(key=key)
                for two_byte in to_16bits(plain_txt):
                    cypher_txt = m_S_AES.encrypt(two_byte)
                    self.ui.cypherTextEdit.insertPlainText(cypher_txt)
        elif self.ui.comboBox_Multi_Encrypt.currentText() == '双重加密':
            if len(self.ui.lineEdit_Key.text()) != 32 or not is_bin(self.ui.lineEdit_Key.text()):
                showErrorInfoBar(self, '双重加密时密钥仅能为32位比特串')
                return
            double_S_AES = two_fold_S_AES(key=key)
            for two_byte in to_16bits(plain_txt):
                cypher_txt = double_S_AES.two_fold_encrypt(two_byte)
                self.ui.cypherTextEdit.insertPlainText(cypher_txt)
        elif self.ui.comboBox_Multi_Encrypt.currentText() == '三重加密':
            if len(self.ui.lineEdit_Key.text()) != 48 or not is_bin(self.ui.lineEdit_Key.text()):
                showErrorInfoBar(self, '三重加密时密钥仅能为48位比特串')
                return
            triple_S_AES = treble_S_AES(key=key)
            for two_byte in to_16bits(plain_txt):
                cypher_txt = triple_S_AES.treble_encrypt(two_byte)
                self.ui.cypherTextEdit.insertPlainText(cypher_txt)

        if self.ui.rBtn_Str.isChecked():
            self.ui.cypherTextEdit.setPlainText(
                asc2str(self.ui.cypherTextEdit.toPlainText())
            )

    def decrypt(self):
        self.ui.plainTextEdit.clear()
        key = self.ui.lineEdit_Key.text()
        cypher_txt = self.ui.cypherTextEdit.toPlainText()

        if self.ui.rBtn_Str.isChecked():
            cypher_txt = str2asc(cypher_txt)

        # 异常处理：
        if not cypher_txt.strip():  # 使用strip()方法移除前后的空白字符并检查文本是否为空
            showErrorInfoBar(self, '密文为空，请输入')
            return
        if len(cypher_txt) % 16 != 0 or not is_bin(cypher_txt):
            print(cypher_txt)
            showErrorInfoBar(self, '密文不是16-bit，请查证后再输入')
            return

        if self.ui.comboBox_Multi_Encrypt.currentText() == '一重加密':
            if len(self.ui.lineEdit_Key.text()) != 16 or not is_bin(self.ui.lineEdit_Key.text()):
                showErrorInfoBar(self, '一重加密时密钥仅能为16位比特串')
                return
            if self.ui.sBtn_CBC.isChecked():
                CBC_S_AES = CBC(key=key)
                plain_text = CBC_S_AES.decrypt(cypher_txt)
                plain_text = ''.join(plain_text)
                self.ui.plainTextEdit.insertPlainText(plain_text)
            else:
                m_S_AES = S_AES(key=key)
                for two_byte in to_16bits(cypher_txt):
                    plain_text = m_S_AES.decrypt(two_byte)
                    self.ui.plainTextEdit.insertPlainText(plain_text)
        elif self.ui.comboBox_Multi_Encrypt.currentText() == '双重加密':
            if len(self.ui.lineEdit_Key.text()) != 32 or not is_bin(self.ui.lineEdit_Key.text()):
                showErrorInfoBar(self, '双重加密时密钥仅能为32位比特串')
                return
            double_S_AES = two_fold_S_AES(key=key)
            for two_byte in to_16bits(cypher_txt):
                plain_text = double_S_AES.two_fold_decrypt(two_byte)
                self.ui.plainTextEdit.insertPlainText(plain_text)
        elif self.ui.comboBox_Multi_Encrypt.currentText() == '三重加密':
            if len(self.ui.lineEdit_Key.text()) != 48 or not is_bin(self.ui.lineEdit_Key.text()):
                showErrorInfoBar(self, '三重加密时密钥仅能为48位比特串')
                return
            triple_S_AES = treble_S_AES(key=key)
            for two_byte in to_16bits(cypher_txt):
                plain_text = triple_S_AES.treble_decrypt(two_byte)
                self.ui.plainTextEdit.insertPlainText(plain_text)

        if self.ui.rBtn_Str.isChecked():
            self.ui.plainTextEdit.setPlainText(
                asc2str(self.ui.plainTextEdit.toPlainText())
            )

    def off_multi(self):
        if self.ui.sBtn_CBC.isChecked():
            self.ui.comboBox_Multi_Encrypt.setCurrentIndex(0)
            self.ui.comboBox_Multi_Encrypt.setDisabled(True)
        else:
            self.ui.comboBox_Multi_Encrypt.setDisabled(False)

    def openCracker(self):
        if self.cracker is None:  # 仅当Cracker窗口不存在时创建
            self.cracker = Cracker()
        self.cracker.show()


QApplication.setHighDpiScaleFactorRoundingPolicy(
    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

app = QApplication([])
main = Main()
# main.ui.show()
main.show()
app.exec_()

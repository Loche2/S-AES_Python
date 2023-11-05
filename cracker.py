from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem
from qfluentwidgets import TeachingTip, InfoBarIcon, TeachingTipTailPosition

# from brute_force_attack import main_brute_force_attack
from ui_cracker import Ui_Form
from utils import showErrorInfoBar, is_bin

pairCount = 1


class Cracker(QWidget):
    def __init__(self):
        # 从UI定义中动态加载窗口对象
        # self.ui = uic.loadUi("Forms/main.ui")
        # 从文件中加载UI定义
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.resize(330, 530)

        self.ui.sBox_Pairs.setValue(1)
        self.ui.TableWidget_Pairs.setWordWrap(False)
        self.ui.TableWidget_Pairs.setColumnCount(2)
        self.ui.TableWidget_Pairs.setRowCount(1)
        self.ui.TableWidget_Pairs.setHorizontalHeaderLabels(['明文', '密文'])
        self.ui.TableWidget_Pairs.horizontalHeader().setSectionResizeMode(1)
        self.ui.TableWidget_Keys.setWordWrap(False)
        self.ui.TableWidget_Keys.setColumnCount(1)
        self.ui.TableWidget_Keys.setRowCount(4)
        self.ui.TableWidget_Keys.setHorizontalHeaderLabels(['可能的密钥'])
        self.ui.TableWidget_Keys.horizontalHeader().setSectionResizeMode(1)
        self.ui.TableWidget_Keys.setEditTriggers(QTableWidget.NoEditTriggers)
        self.ui.IndeterminateProgressBar.setVisible(False)

        self.ui.sBox_Pairs.valueChanged.connect(self.setPairCount)
        self.ui.ppBtn_Crack.clicked.connect(self.crack)

    def setPairCount(self):
        self.ui.TableWidget_Pairs.setRowCount(self.ui.sBox_Pairs.value())

    def get_column_data(self, column_index):
        column_data = []
        for row in range(self.ui.TableWidget_Pairs.rowCount()):
            item = self.ui.TableWidget_Pairs.item(row, column_index)
            if item is not None:
                text = item.text()
                values = [int(char) for char in text]  # 将单元格文本分割为单独的数字
                column_data.append(values)
        return column_data

    def crack(self):
        # 异常处理：
        for row in range(self.ui.TableWidget_Pairs.rowCount()):
            for col in range(self.ui.TableWidget_Pairs.columnCount()):
                item = self.ui.TableWidget_Pairs.item(row, col)
                if item is None or not item.text():
                    showErrorInfoBar(self, '明密文对不完整，请确认')
                    self.ui.IndeterminateProgressBar.setVisible(False)
                    return
                if len(item.text()) != 8 or not is_bin(item.text()):
                    showErrorInfoBar(self, '不是整数个Byte，请查证后再输入')
                    self.ui.IndeterminateProgressBar.setVisible(False)
                    return
        self.ui.TableWidget_Keys.clearContents()
        self.ui.IndeterminateProgressBar.setVisible(True)
        plain_data = self.get_column_data(0)
        cypher_data = self.get_column_data(1)
        keys, duration = main_brute_force_attack(self.ui.TableWidget_Pairs.rowCount(), plain_data, cypher_data)
        print(keys)
        if len(keys) == 0:
            showErrorInfoBar(self, '未找到可能的密钥')
        if len(keys) > 4:
            self.ui.TableWidget_Keys.setRowCount(len(keys))
        for row, row_data in enumerate(keys):
            data_str = ''.join(map(str, row_data))  # 将每行数据转换为字符串并连接在一起
            item = QTableWidgetItem(data_str)
            self.ui.TableWidget_Keys.setItem(row, 0, item)
        TeachingTip.create(
            target=self.ui.ppBtn_Crack,
            icon=InfoBarIcon.SUCCESS,
            title='计时器',
            content=f'暴力破解耗时：{duration}',
            isClosable=True,
            tailPosition=TeachingTipTailPosition.TOP,
            duration=5000,
            parent=self
        )
        self.ui.IndeterminateProgressBar.setVisible(False)

# app = QApplication([])
# cracker = Cracker()
# # main.ui.show()
# cracker.show()
# app.exec_()

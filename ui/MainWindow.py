from PyQt5.QtCore import QEasingCurve, QPoint, QPropertyAnimation, QThread, pyqtSignal
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QAbstractItemView, QFrame, QHeaderView, QMainWindow, QMessageBox, QPlainTextEdit, QScrollArea, QStackedWidget, QVBoxLayout, QWidget
from ui.MainWindow_ui import Ui_MainWindow
from ui.ResultWidget import FullResultWidget, PartResultWidget
from ui.ToolBar_ui import Ui_ToolBar
from communication.CheckResult import CheckResultPresentation as Result
from communication.Request import getBaseInfo, duplicateResultGet


class ConnectThread(QThread):
    """
    连接服务器的线程
    """
    def __init__(self, ip: str, toolBar):
        super().__init__()
        self.ip = ip
        self.toolBar = toolBar

    def run(self):
        ret = getBaseInfo(self.ip)
        if ret is None:
            self.toolBar.connectWarning.emit()
        else:
            self.toolBar.serversChanged.emit(ret[0], ret[1])
            self.toolBar.dataGroupsChanged.emit(ret[2], ret[3])
        return super().run()


class DuplicateThread(QThread):
    """
    查重的线程
    """
    def __init__(self, ip: str, win):
        super().__init__()
        self.address = (ip, 11451)
        self.win = win

    def run(self):
        s: str = self.win.plainTextEdit.toPlainText()
        results = duplicateResultGet(('0', 0), [s])
        self.win.progressBarUpdate.emit(1)
        for it in results:
            self.win.resultUpdate.emit(it)


class ToolBar(Ui_ToolBar, QWidget):
    """
    工具栏
    """
    connectWarning = pyqtSignal()
    serversChanged = pyqtSignal(list, list)
    dataGroupsChanged = pyqtSignal(list, list)

    open = pyqtSignal()
    isClicked = True
    isOpened = False

    def __init__(self, serversList, dataGroupsList, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.resize(512, 800)
        self.setAutoFillBackground(True)

        self.tableView.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        #self.tableView.setSelectionBehavior(1)(
        #    QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableView.setModel(serversList)
        self.tableView_2.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        #self.tableView_2.setSelectionBehavior(1)(
        #    QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableView_2.setModel(dataGroupsList)

        self.pushButton_2.clicked.connect(self.refreshInfo)
        self.serversChanged.connect(serversList.update)
        self.dataGroupsChanged.connect(dataGroupsList.update)
        self.connectWarning.connect(self.showConnectWarning)

    def showConnectWarning(self):
        QMessageBox.warning(self, "连接服务器失败", "请检查网络连接与服务器地址拼写，或联系服务器管理员")

    def refreshInfo(self):
        ip = self.lineEdit.text()
        self.__thd = ConnectThread(ip, self)
        self.__thd.start()

    def mousePressEvent(self, e: QMouseEvent):
        self.isClicked = True
        if e.pos().x() >= 500 and -500 == self.pos().x():
            self.open.emit()
            self.isOpened = True
        return super().mousePressEvent(e)


class MainWidget(Ui_MainWindow, QWidget):
    """
    中心主窗体
    """
    class ClickedSignTextEdit(QPlainTextEdit):
        """
        响应点击的文本框部件
        """
        clicked = pyqtSignal()

        def __init__(self, parent=None):
            super().__init__(parent)

        def mousePressEvent(self, e: QMouseEvent):
            self.clicked.emit()
            return super().mousePressEvent(e)

    resultUpdate = pyqtSignal(Result)
    progressBarUpdate = pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # 展示框
        self.stackWidget = QStackedWidget(self)
        # 缩略展示
        self.__scrollArea1 = QScrollArea(self.stackWidget)
        self.partPresentWidget = QWidget(self.stackWidget)
        self.partPresentWidget.setMinimumWidth(970)
        # self.partPresentWidget.setMinimumHeight(300)
        self.partPresentLayout = QVBoxLayout()
        self.partPresentWidget.setLayout(self.partPresentLayout)
        self.__scrollArea1.setWidget(self.partPresentWidget)
        self.stackWidget.addWidget(self.__scrollArea1)
        # 详细展示
        self.__scrollArea2 = QScrollArea(self.stackWidget)
        self.fullPresentWidget = None
        self.stackWidget.insertWidget(1, self.__scrollArea2)

        self.verticalLayout_2.insertWidget(0, self.stackWidget, 4)

        # 文本框
        self.plainTextEdit = MainWidget.ClickedSignTextEdit(self)
        self.verticalLayout_2.insertWidget(0, self.plainTextEdit, 1)
        self.stackWidget.hide()
        self.progressBar.hide()

        self.resultUpdate.connect(self.addResult)
        self.progressBarUpdate.connect(self.updateProgressBar)

# ===========================

    def updateProgressBar(self, s: float):
        if s < 0:
            self.progressBar.setRange(0, 0)
            self.progressBar.show()
        else:
            self.progressBar.setRange(0, 100)
            self.progressBar.setValue(min(100, 100 * s))

        if s >= 1:
            self.progressBar.hide()

    def addResult(self, result: Result):
        """
        添加一项结果到PartResult中
        """
        flag = 0 == self.partPresentLayout.count()
        if not flag:
            line = QFrame(self)
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Plain)
            self.partPresentLayout.addWidget(line)

        cur = PartResultWidget(result, 64, self.partPresentWidget)
        cur.adjustSize()
        self.partPresentLayout.addWidget(cur)
        self.partPresentWidget.resize(
            self.partPresentWidget.width(),
            self.partPresentWidget.height() + cur.height())

        cur.clicked.connect(self.showFullResult)
        if flag:
            self.stackWidget.setCurrentIndex(0)
            self.stackWidget.show()

    def clearResult(self):
        """
        清空当前正在显示的结果
        """
        for i in range(self.partPresentLayout.count()):
            self.partPresentLayout.itemAt(i).widget().deleteLater()
        self.stackWidget.hide()

    def showFullResult(self, result: Result):
        """
        展示结果的完整内容
        """
        self.fullPresentWidget = FullResultWidget(result, 256)
        self.__scrollArea2.setWidget(self.fullPresentWidget)
        self.fullPresentWidget.setFixedWidth(880)
        self.fullPresentWidget.clicked.connect(self.showPartResult)
        self.stackWidget.setCurrentIndex(1)

    def showPartResult(self):
        """
        展示全部内容
        """
        if not self.fullPresentWidget is None:
            self.fullPresentWidget.deleteLater()
        self.stackWidget.setCurrentIndex(0)


# ===========================


class MainWindow(QMainWindow):
    """
    主窗体
    """
    packToolBar = pyqtSignal()

    def __init__(self, serversList, databasesList):
        super().__init__()

        self.setFixedSize(1000, 800)

        # TODO: 测试临时改私有为共有
        self.mainWidget = MainWidget(self)
        self.setCentralWidget(self.mainWidget)

        self.__toolBar = ToolBar(serversList, databasesList, self)
        self.__toolBar.show()
        self.__toolBar.move(-500, 0)

        # ToolBar展开动画
        toolBarAnimation1 = QPropertyAnimation(self.__toolBar, b'pos', self)
        toolBarAnimation1.setDuration(500)
        toolBarAnimation1.setStartValue(QPoint(-500, 0))
        toolBarAnimation1.setEndValue(QPoint(0, 0))
        toolBarAnimation1.setEasingCurve(QEasingCurve.OutQuad)
        self.__toolBar.open.connect(toolBarAnimation1.start)

        # ToolBar收起动画
        toolBarAnimation2 = QPropertyAnimation(self.__toolBar, b'pos', self)
        toolBarAnimation2.setDuration(500)
        toolBarAnimation2.setStartValue(QPoint(0, 0))
        toolBarAnimation2.setEndValue(QPoint(-500, 0))
        toolBarAnimation2.setEasingCurve(QEasingCurve.InQuad)
        self.packToolBar.connect(toolBarAnimation2.start)
        self.mainWidget.plainTextEdit.clicked.connect(self.__preToolBarPack)
        self.__toolBar.pushButton.clicked.connect(self.startDuplicateCheck)

    def startDuplicateCheck(self):
        self.__preToolBarPack()

        self.mainWidget.progressBarUpdate.emit(-1)
        self.thd = DuplicateThread(self.__toolBar.lineEdit.text(),
                                   self.mainWidget)
        self.thd.start()

    def __preToolBarPack(self):
        if self.__toolBar.isClicked:
            self.__toolBar.isClicked = False
        elif self.__toolBar.isOpened:
            self.packToolBar.emit()
            self.__toolBar.isOpened = False

    def mousePressEvent(self, e: QMouseEvent):
        self.__preToolBarPack()
        return super().mousePressEvent(e)

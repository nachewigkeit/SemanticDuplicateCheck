from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget
from communication.CheckResult import CheckResultPresentation as Result


class PartResultWidget(QWidget):
    """
    缩略展示
    """
    clicked = pyqtSignal(Result)

    def __init__(self, result: Result, maxLen: int, parent=None):
        """
        需提供展示内容以及所容许的最大字符串长度
        """
        super().__init__(parent)
        self.result = result

        self.__layout = QHBoxLayout()

        # 展示显示句
        self.__source = QLabel(self)
        l, r = result.pos
        if r - l >= maxLen:
            s = result.s[l:l + maxLen]
            s = "<font color=red>" + s + "</font>"
        else:
            b = min(l, 5, maxLen - r + l)
            s = result.s[l - b:l]
            s += "<font color=red>"
            s += result.s[l:r]
            s += "</font>"
            b = min(len(result.s) - r, max(0, maxLen - r + l - b))
            if b > 0:
                s += result.s[r:r + b]
        self.__source.setWordWrap(True)
        self.__source.setText(s)
        self.__source.adjustSize()
        self.__layout.addWidget(self.__source)

        # 分割线
        self.__line = QFrame(self)
        self.__line.setFrameShape(QFrame.VLine)
        self.__line.setFrameShadow(QFrame.Plain)
        self.__layout.addWidget(self.__line)

        # 展示重复句
        self.__layout_2 = QVBoxLayout()
        cnt = 0
        for it in result.retList:
            if 2 == cnt and 3 != len(result.retList):
                break
            if 0 != cnt:
                self.__line = QFrame(self)
                self.__line.setFrameShape(QFrame.HLine)
                self.__line.setFrameShadow(QFrame.Plain)
                self.__layout_2.addWidget(self.__line)
            simRet = QLabel(self)
            l, r = it[2]
            if r - l >= maxLen:
                s1 = it[0][l:l + maxLen]
                s1 = "<font color=red>" + s + "</font>"
            else:
                b = min(l, 5, maxLen - r + l)
                s1 = it[0][l - b:l]
                s1 += "<font color=red>"
                s1 += it[0][l:r]
                s1 += "</font>"
                b = min(len(it[0]) - r, max(0, maxLen - r + l - b))
                if b > 0:
                    s1 += it[0][r:r + b]
            simRet.setWordWrap(True)
            simRet.setText(s1)
            simRet.adjustSize()
            self.__layout_2.addWidget(simRet)
            cnt += 1
        if len(result.retList) > 3:
            self.__line = QFrame(self)
            self.__line.setFrameShape(QFrame.HLine)
            self.__line.setFrameShadow(QFrame.Plain)
            self.__layout_2.addWidget(self.__line)

            simRet = QLabel(self)
            simRet.setWordWrap(True)
            simRet.setText("与其余" + str(len(result.retList) - 2) + "项")
            simRet.adjustSize()
            self.__layout_2.addWidget(simRet)
        self.__layout.addLayout(self.__layout_2)

        self.setLayout(self.__layout)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        self.clicked.emit(self.result)
        return super().mousePressEvent(e)


class FullResultWidget(QWidget):
    """
    完全展示
    """
    clicked = pyqtSignal()

    def __init__(self, result: Result, maxLen: int, parent=None):
        """
        需提供展示内容以及所容许的最大字符串长度
        """
        super().__init__(parent)

        self.__layout = QVBoxLayout()

        # 展示显示句
        self.__source = QLabel(self)
        l, r = result.pos
        if r - l >= maxLen:
            s = result.s[l:l + maxLen]
            s = "<font color=red>" + s + "</font>"
        else:
            b = min(l, 5, maxLen - r + l)
            s = result.s[l - b:l]
            s += "<font color=red>"
            s += result.s[l:r]
            s += "</font>"
            b = min(len(result.s) - r, max(0, maxLen - r + l - b))
            if b > 0:
                s += result.s[r:r + b]
        self.__source.setWordWrap(True)
        self.__source.setText(s)
        self.__source.adjustSize()
        self.__layout.addWidget(self.__source)

        # 分割线
        self.__line = QFrame(self)
        self.__line.setFrameShape(QFrame.HLine)
        self.__line.setFrameShadow(QFrame.Plain)
        self.__layout.addWidget(self.__line)

        # 展示重复句
        for it in result.retList:
            self.__line = QFrame(self)
            self.__line.setFrameShape(QFrame.HLine)
            self.__line.setFrameShadow(QFrame.Plain)
            self.__layout.addWidget(self.__line)

            simRet = QLabel(self)
            l, r = it[2]
            if r - l >= maxLen:
                s1 = it[0][l:l + maxLen]
                s1 = "<font color=red>" + s + "</font>"
            else:
                b = min(l, 5, maxLen - r + l)
                s1 = it[0][l - b:l]
                s1 += "<font color=red>"
                s1 += it[0][l:r]
                s1 += "</font>"
                b = min(len(it[0]) - r, max(0, maxLen - r + l - b))
                if b > 0:
                    s1 += it[0][r:r + b]
            simRet.setWordWrap(True)
            simRet.setText(s1)
            simRet.adjustSize()

            infos = QLabel(self)
            infos.setWordWrap(True)
            infos.setText(it[1])
            infos.adjustSize()

            self.__layout.addWidget(simRet)
            self.__layout.addWidget(infos)

        self.setLayout(self.__layout)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        self.clicked.emit()
        return super().mousePressEvent(e)

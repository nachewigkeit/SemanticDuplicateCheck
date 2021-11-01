import sys
from PyQt5.QtCore import QThread

from PyQt5.QtWidgets import QApplication

from ui.MainWindow import MainWindow
from communication.DataGroupsList import DataGroupsList
from communication.ServersList import ServersList

if '__main__' == __name__:
    # import ui.ResultWidget as ttt
    # ttt.test()

    app = QApplication(sys.argv)

    serversList = ServersList()
    databasesList = DataGroupsList()

    win = MainWindow(serversList, databasesList)
    win.show()

    # from communication.CheckResult import CheckResultPresentation as Result
    # result = Result(
    #     "这是上文，这是相关句，这是下文",
    #     (5, 10),
    #     [
    #         ("这是上文，这是重复句一号，这是下文", "重复句一号", (5, 12)),
    #         ("这是重复句二号，这是下文", "重复句二号", (0, 7)),
    #         ("这是上文，这是重复句三号", "重复句三号", (5, 12)),
    #         ("这是重复句四号", "重复句四号", (0, 7)),
    #     ],
    # )
    # win.mainWidget.addResult(result)

    # result = Result(
    #     "这是上文，这是结果二号里的相关句，这是下文",
    #     (5, 10),
    #     [
    #         ("这是上文，这是重复句一号，这是下文QLabel 文本内容自动换行显示 需要把QLabel的 WordWrap属性设置成TRUE,可以通过界面设置,也可以通过程序设置 分类:Qt编程 好文要顶关注我收藏该文 我是张洪铭我是熊博士 关注- 12 粉",
    #          "重复句一号", (5, 12)),
    #         ("这是重复句二号，这是下文QLabel 文本内容自动换行显示 需要把QLabel的 WordWrap属性设置成TRUE,可以通过界面设置,也可以通过程序设置 分类:Qt编程 好文要顶关注我收藏该文 我是张洪铭我是熊博士 关注- 12 粉",
    #          "重复句二号", (0, 7)),
    #         ("这是上文，这是重复句三号", "重复句三号", (5, 12)),
    #         ("这是重复句四号", "重复句四号", (0, 7)),
    #     ],
    # )
    # win.mainWidget.addResult(result)

    # thr = Thread1()
    # # thr.start()

    app.exec_()

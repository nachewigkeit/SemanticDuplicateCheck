class CheckResultPresentation():
    """
    用于展示的检测结果
    由原始检测结果解析包装后得来
    """
    s: str  # 可能被用于展示的前后文
    pos: tuple  # 相关句子窗口
    retList: list  # 对应的重复句子信息[内容，描述，窗口]

    def __init__(self, s, pos, retList):
        self.s = s
        self.pos = pos
        self.retList = retList

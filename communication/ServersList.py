from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant


class ServersList(QAbstractTableModel):
    '服务器列表'

    servers = []

    def __init__(self):
        super().__init__()

    def update(self, names, counts):
        self.beginResetModel()
        self.servers = [(True, names[i], counts[i]) for i in range(len(names))]
        self.endResetModel()

    # ==============================================

    def rowCount(self, parent: QModelIndex = ...):
        return len(self.servers)

    def columnCount(self, parent: QModelIndex = ...):
        return 3

    def headerData(self,
                   section: int,
                   orientation: Qt.Orientation,
                   role: int = ...):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return ["", "模型名称", "可用服务器数"][section]
        return int(section + 1)

    def data(self, index: QModelIndex, role: int = ...):
        if not index.isValid() or not 0 <= index.row() < self.rowCount():
            return QVariant()

        row = index.row()
        col = index.column()

        if role == Qt.CheckStateRole and 0 == col:
            return Qt.Checked if self.servers[row][col] else Qt.Unchecked
        if role == Qt.DisplayRole:
            if 0 == col:
                return ""
            elif row < len(self.servers) and col < 3:
                return self.servers[row][col]
        return QVariant()

    def setData(self, index: QModelIndex, value, role) -> bool:
        row = index.row()
        col = index.column()
        if role == Qt.CheckStateRole and 0 == col:
            if value == Qt.Unchecked:
                self.servers[row][0] = False
                self.dataChanged.emit(index, index)
            elif value == Qt.Checked:
                self.servers[row][0] = True
                self.dataChanged.emit(index, index)

        return super().setData(index, value, role=role)

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        col = index.column()
        if 0 == col:
            return Qt.ItemIsUserCheckable

        return super().flags(index)

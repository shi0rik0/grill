from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QWidget


class JumpDialog(QDialog):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._label = QLabel('请输入要跳转的时间，按Enter跳转。')
        self._line_edit = QLineEdit()
        self._layout = QVBoxLayout()
        self._layout.addWidget(self._label)
        self._layout.addWidget(self._line_edit)
        self.setLayout(self._layout)

        self._line_edit.returnPressed.connect(self._on_return)

    def _on_return(self) -> None:
        s = self._line_edit.text().strip()
        if len(s) == 0:
            return
        ss = s[-2:]
        mm = s[-4:-2]
        h = s[:-4]
        try:
            ss = int(ss) if ss else 0
            mm = int(mm) if mm else 0
            h = int(h) if h else 0
        except ValueError:
            return
        self._time = (h * 3600 + mm * 60 + ss) * 1000
        self.accept()

    @property
    def time(self) -> int:
        '''unit: ms'''
        return self._time

import pathlib

from PySide6.QtWidgets import (QDialog, QGridLayout, QLabel, QMessageBox,
                               QPushButton, QWidget)

from select_file_edit import SelectFileEdit
from utils import create_button


class SelectFileDialog(QDialog):
    _layout: QGridLayout
    _layout_0: QGridLayout
    _label: QLabel
    _select_file_edit: SelectFileEdit
    _button: QPushButton

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        self._label = QLabel('视频路径：')
        self._select_file_edit = SelectFileEdit('视频文件 (*.mp4 *.mkv)')
        self._button = create_button('打开', self._on_clicked)

        self._layout_0 = QGridLayout()
        self._layout_0.addWidget(self._label, 0, 0)
        self._layout_0.addWidget(self._select_file_edit, 0, 1)

        self._layout = QGridLayout()
        self._layout.addLayout(self._layout_0, 0, 0)
        self._layout.addWidget(self._button, 1, 0)

        self.setLayout(self._layout)

    def _on_clicked(self) -> None:
        if not pathlib.Path(self.path).is_file():
            QMessageBox.critical(self, '错误', '文件不存在。')
            return
        self.accept()

    @property
    def path(self) -> str:
        return self._select_file_edit.path

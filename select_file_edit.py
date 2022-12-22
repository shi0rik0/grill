from PySide6.QtCore import Qt, QUrl, Signal, Slot
from PySide6.QtWidgets import (QDialog, QFileDialog, QHBoxLayout, QLineEdit,
                               QPushButton, QWidget, QGridLayout)
from utils import create_button


class SelectFileEdit(QWidget):
    _line_edit: QLineEdit
    _button: QPushButton
    _layout: QHBoxLayout

    def __init__(self, filter: str) -> None:
        super().__init__()

        self._filter = filter

        self._line_edit = QLineEdit()
        self._button = create_button('...', self._on_clicked)
        self._layout = QGridLayout()
        self._layout.addWidget(self._line_edit, 0, 0)
        self._layout.addWidget(self._button, 0, 1)
        self._button.setMaximumWidth(30)

        self.setLayout(self._layout)
        self._is_disabled = False

    @property
    def path(self) -> str:
        return self._line_edit.text()

    def _on_clicked(self) -> None:
        path, _ = QFileDialog.getOpenFileName(parent=self, filter=self._filter)
        self._line_edit.setText(path)

    @property
    def is_disabled(self) -> bool:
        return self._is_disabled

    @is_disabled.setter
    def is_disabled(self, disabled: bool) -> None:
        self._line_edit.setDisabled(disabled)
        self._button.setDisabled(disabled)

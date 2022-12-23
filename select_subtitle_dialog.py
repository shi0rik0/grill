
import pathlib
from typing import Optional, Sequence, Union

from PySide6.QtWidgets import (QComboBox, QDialog, QGridLayout, QHBoxLayout,
                               QLabel, QMessageBox, QWidget)

from select_file_edit import SelectFileEdit
from utils import create_button, create_radio_button


class SelectSubtitleDialog(QDialog):
    def __init__(self, parent: Optional[QWidget], subtitle_languages: Sequence[str]) -> None:
        super().__init__(parent)

        self._radio_0 = create_radio_button('使用内封字幕', self._on_radio_0_selected)
        self._radio_1 = create_radio_button('使用外挂字幕', self._on_radio_1_selected)
        self._label_0 = QLabel('字幕语言：')
        self._combo_box = QComboBox()

        self._combo_box.addItems(subtitle_languages)

        self._label_1 = QLabel('字幕路径：')
        self._select_file_edit = SelectFileEdit('字幕文件 (*.srt *.ass)')
        self._button = create_button('确定', self._on_button_clicked)

        self._layout_0 = QHBoxLayout()
        self._layout_0.addWidget(self._label_0)
        self._layout_0.addWidget(self._combo_box)
        self._layout_0.addStretch()

        self._layout_1 = QGridLayout()
        self._layout_1.addWidget(self._label_1, 0, 0)
        self._layout_1.addWidget(self._select_file_edit, 0, 1)

        self._layout = QGridLayout()
        self._layout.addWidget(self._radio_0, 0, 0)
        self._layout.addLayout(self._layout_0, 1, 0)
        self._layout.addWidget(self._radio_1, 2, 0)
        self._layout.addLayout(self._layout_1, 3, 0)
        self._layout.addWidget(self._button, 4, 0)

        self.setLayout(self._layout)

        if len(subtitle_languages) > 0:
            self._radio_0.setChecked(True)
        else:
            self._radio_0.setDisabled(True)
            self._radio_0.setText(self._radio_0.text() + '（未检测到内封字幕）')
            self._radio_1.setChecked(True)

    def _on_radio_0_selected(self) -> None:
        self._combo_box.setDisabled(False)
        self._select_file_edit.is_disabled = True

    def _on_radio_1_selected(self) -> None:
        self._combo_box.setDisabled(True)
        self._select_file_edit.is_disabled = False

    def _on_button_clicked(self) -> None:
        if isinstance(self.subtitle, str) and not pathlib.Path(self.subtitle).is_file():
            QMessageBox.critical(self, '错误', '文件不存在。')
            return
        self.accept()

    @property
    def subtitle(self) -> Union[int, str]:
        if self._radio_0.isChecked():
            return self._combo_box.currentIndex()
        else:
            return self._select_file_edit.path

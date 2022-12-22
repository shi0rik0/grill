from dataclasses import dataclass
from time import sleep
from typing import Callable, Dict, Tuple

from PySide6.QtCore import Qt, QUrl, Signal, Slot
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import QPushButton, QRadioButton


def create_button(text: str, callback: Callable[[], None], cls=QPushButton):
    btn = cls(text)
    btn.clicked.connect(callback)
    return btn


def create_radio_button(text: str, callback: Callable[[], None], cls=QRadioButton):
    btn = cls(text)

    def wrapper(toggled: bool) -> None:
        if toggled:
            callback()

    btn.toggled.connect(wrapper)
    return btn

from dataclasses import dataclass
from datetime import timedelta
from typing import List, Sequence

from PySide6.QtCore import QUrl
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import (QDialog, QMessageBox, QTextEdit, QVBoxLayout,
                               QWidget)

from jump_dialog import JumpDialog


class MainWidget(QWidget):
    _THRESHOLD = 200  # 200 ms

    @dataclass
    class SubtitleLine:
        start: timedelta
        end: timedelta
        content: str

    _media_player: QMediaPlayer
    _video_widget: QVideoWidget
    _audio_output: QAudioOutput
    _text_edit: QTextEdit

    _pause_position: int
    _subtitle: List[SubtitleLine]
    __current_subtitle_line: int
    _media_player_inited: bool

    def __init__(self):
        super().__init__()

    def late_init(self, video_path: str, subtitle: Sequence[SubtitleLine]):
        self._media_player_inited = False
        self._playback_rates = [1, 0.75]
        self._current_playback_rate_idx = 0
        self._subtitle = list(subtitle)
        if len(self._subtitle) == 0:
            QMessageBox.critical(self, '错误', '不能使用空字幕。')
            self.close()

        self._text_edit = QTextEdit()
        self._media_player = QMediaPlayer()
        self._media_player.setSource(QUrl(video_path))
        self._video_widget = QVideoWidget()
        self._media_player.setVideoOutput(self._video_widget)
        self._audio_output = QAudioOutput()
        self._media_player.setAudioOutput(self._audio_output)
        self._media_player.setPlaybackRate(self._playback_rates[self._current_playback_rate_idx])
        # TODO: adjust size according to the size of video
        self._video_widget.setMinimumSize(800, 600)

        self._layout = QVBoxLayout(self)
        self._layout.addWidget(self._video_widget)
        # self._layout.addWidget(self._text_edit)
        self.setLayout(self._layout)

        self._media_player.positionChanged.connect(self._on_position_changed)
        self._media_player.mediaStatusChanged.connect(self._on_media_status_changed)

        self._init_shortcuts()

    @property
    def _current_subtitle_line(self) -> int:
        return self.__current_subtitle_line

    @_current_subtitle_line.setter
    def _current_subtitle_line(self, idx: int) -> None:
        if idx < 0 or idx >= len(self._subtitle):
            raise ValueError('invalid subtitle index')
        self.__current_subtitle_line = idx
        s = self._subtitle[idx]
        start = int(s.start.total_seconds() * 1000)
        end = int(s.end.total_seconds() * 1000)
        self._pause_position = end
        self._set_video_position(start)

    def _init_shortcuts(self):
        self.shortcut_shift_space = self._add_shortcut('Space', self._on_space)
        self.shortcut_shift_left = self._add_shortcut('Left', self.on_left)
        self.shortcut_shift_right = self._add_shortcut('Right', self.on_right)
        self.shortcut_s = self._add_shortcut('S', self._on_s)
        # self.shortcut_j = self._add_shortcut('J', self._on_j)

    def _add_shortcut(self, key_seq: str, callback) -> QShortcut:
        s = QShortcut(QKeySequence(key_seq), self)
        s.activated.connect(callback)
        return s

    def _on_position_changed(self, pos: int) -> None:
        '''make sure that the video never ends'''
        max_pos = min(self._pause_position, self._media_player.duration() - MainWidget._THRESHOLD)
        if pos >= max_pos:
            self._media_player.pause()

    def _set_video_position(self, pos: int) -> None:
        if (self._media_player.duration() > 0 and pos >= self._media_player.duration()) or pos < 0:
            raise ValueError('invalid position')
        if self._media_player.duration() > 0:
            pos = min(pos, self._media_player.duration() - MainWidget._THRESHOLD)
        pos = max(pos, 0)
        self._media_player.setPosition(pos)

    def _play_video(self) -> None:
        if self._media_player.duration() > 0 and self._media_player.position() >= self._media_player.duration() - MainWidget._THRESHOLD:
            return
        self._media_player.play()

    # shortcut callbacks
    def _on_space(self) -> None:
        status = self._media_player.playbackState()
        s = self._subtitle[self._current_subtitle_line]
        start = int(s.start.total_seconds() * 1000)
        self._set_video_position(start)
        if status != QMediaPlayer.PlaybackState.PlayingState:
            self._play_video()

    def on_left(self) -> None:
        idx = self._current_subtitle_line
        idx = max(idx - 1, 0)
        self._current_subtitle_line = idx
        self._play_video()

    def on_right(self) -> None:
        idx = self._current_subtitle_line
        idx = min(idx + 1, len(self._subtitle) - 1)
        self._current_subtitle_line = idx
        self._play_video()

    def _on_s(self) -> None:
        self._current_playback_rate_idx = (
            self._current_playback_rate_idx + 1) % len(self._playback_rates)
        self._media_player.setPlaybackRate(
            self._playback_rates[self._current_playback_rate_idx])

    def _on_j(self) -> None:
        dialog = JumpDialog(self)
        ret = dialog.exec()
        if ret != QDialog.DialogCode.Accepted:
            return
        # TODO
        # self._pause_position = -1
        # self._set(dialog.time)

    def _on_media_status_changed(self, status: QMediaPlayer.MediaStatus) -> None:
        if not self._media_player_inited and status == QMediaPlayer.MediaStatus.InvalidMedia:
            QMessageBox.critical(self, '错误', '不支持该视频格式。')
            self.close()
        elif not self._media_player_inited and status == QMediaPlayer.MediaStatus.LoadedMedia:
            self._media_player_inited = True
            self._current_subtitle_line = 0

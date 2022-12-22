import sys

import srt
from PySide6.QtWidgets import QApplication, QDialog

from select_file_dialog import SelectFileDialog
from select_subtitle_dialog import SelectSubtitleDialog
from subtitle_extractor import subtitle_extractor
from temp_file_manager import temp_file_manager
from main_widget import MainWidget


def main():
    app = QApplication(sys.argv)
    main_widget = MainWidget()
    select_file_dialog = SelectFileDialog(main_widget)
    ret = select_file_dialog.exec()
    if ret != QDialog.DialogCode.Accepted:
        sys.exit(0)
    video_path = select_file_dialog.path
    subtitle_metadata = subtitle_extractor.read_subtitle_metadata(video_path)
    select_subtitle_dialog = SelectSubtitleDialog(main_widget, [i.language for i in subtitle_metadata])
    ret = select_subtitle_dialog.exec()
    if ret != QDialog.DialogCode.Accepted:
        sys.exit(0)
    if isinstance(select_subtitle_dialog.subtitle, int):
        subtitle_path = temp_file_manager.get_temp_file_path()
        track_id = subtitle_metadata[select_subtitle_dialog.subtitle].track_id
        subtitle_extractor.extract_subtitle(video_path, track_id, subtitle_path)
    else:
        subtitle_path = select_subtitle_dialog.subtitle

    with open(subtitle_path, encoding='utf-8') as f:
        subtitle = f.read()
    subtitle = [MainWidget.SubtitleLine(i.start, i.end, i.content) for i in srt.parse(subtitle)]
    main_widget.late_init(video_path, subtitle)
    main_widget.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

import pathlib
import shutil
import uuid


class _TempFileManager:
    def __init__(self) -> None:
        '''This function should be called only once.'''
        self._temp_dir = pathlib.Path(__file__).resolve().parent / 'temp'
        if self._temp_dir.is_file():
            self._temp_dir.unlink()
        elif self._temp_dir.is_dir():
            shutil.rmtree(self._temp_dir)
        self._temp_dir.mkdir()

    def get_temp_file_path(self) -> str:
        return str(self._temp_dir / uuid.uuid1().hex)


temp_file_manager = _TempFileManager()

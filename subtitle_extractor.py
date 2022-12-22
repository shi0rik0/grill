import os
import pathlib
import platform
import re
import subprocess
from dataclasses import dataclass
from typing import List, Union

from temp_file_manager import temp_file_manager


@dataclass
class SubtitleMetadata:
    track_id: int
    name: str
    language: str


class _SubtitleExtractor:
    def __init__(self):
        '''This function should be called only once.'''
        self._add_program_dir_to_path_env_var()
        cmd = [['mkvextract', '-V'], ['mkvmerge', '-V'], ['mkvinfo', '-V']]
        ok = [self._exec_command(i) == 0 for i in cmd]
        if not all(ok):
            raise RuntimeError('please make sure you have installed mkvtoolnix')

    @staticmethod
    def _add_program_dir_to_path_env_var():
        dir = str(pathlib.Path(__file__).resolve().parent / 'mkvtoolnix')
        if platform.system() == 'Windows':
            if dir.find(';') != -1:
                dir = '"' + dir + '"'
            os.environ['PATH'] = dir + ';' + os.environ['PATH']
        else:
            if dir.find(':') != -1:
                raise RuntimeError("the path shouldn't contain ':'")
            os.environ['PATH'] = dir + ':' + os.environ['PATH']

    @staticmethod
    def _exec_command(cmd: Union[str, List[str]]) -> int:
        # TODO: use subprocess.run() instead?
        return subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    @staticmethod
    def read_subtitle_metadata(path: str) -> List[SubtitleMetadata]:
        path = str(pathlib.Path(path).resolve())
        temp = temp_file_manager.get_temp_file_path()
        _SubtitleExtractor._exec_command(['mkvmerge', '-i', path, '-r', temp, '--ui-language', 'en'])
        encoding = 'utf-8-sig' if platform.system() == 'Windows' else 'utf-8'
        with open(temp, encoding=encoding) as f:
            output = f.read()
        output = output[:output.find('\n')]
        s = 'container: '
        container_format = output[output.rfind(s) + len(s):]
        if container_format != 'Matroska':
            return []

        temp = temp_file_manager.get_temp_file_path()
        _SubtitleExtractor._exec_command(['mkvinfo', path, '-r', temp, '--ui-language', 'en'])
        encoding = 'utf-8-sig' if platform.system() == 'Windows' else 'utf-8'
        with open(temp, encoding=encoding) as f:
            output = f.read()
        tracks = output.split('| + Track')[1:]
        ret = []
        for i, v in enumerate(tracks):
            kind = re.search(r'\|  \+ Track type: (.*)\n', v).group(1)
            if kind != 'subtitles':
                continue
            name = re.search(r'\|  \+ Name: (.*)\n', v).group(1)
            language = re.search(r'\|  \+ Language: (.*)\n', v).group(1)
            ret.append(SubtitleMetadata(track_id=i, name=name, language=language))
        return ret

    @staticmethod
    def extract_subtitle(video_path: str, track_id: int, out_path: str) -> None:
        video_path = str(pathlib.Path(video_path).resolve())
        out_path = str(pathlib.Path(out_path).resolve())
        # TODO: what if 'out_path' contains spaces?
        _SubtitleExtractor._exec_command(['mkvextract', video_path, 'tracks',
                                         f'{track_id}:{out_path}', '--ui-language', 'en'])


subtitle_extractor = _SubtitleExtractor()

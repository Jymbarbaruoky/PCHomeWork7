from ast import arg
import re
from pathlib import Path
import shutil
import sys
import argparse
import os


cyrillic_characters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
latin_equivalent = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
dict_for_translate = {}
for cyr, lat in zip(cyrillic_characters, latin_equivalent):
    dict_for_translate[ord(cyr)] = lat
    dict_for_translate[ord(cyr.upper())] = lat.upper()

def create_folders(path_dir: Path) -> None:
    (path_dir / 'images').mkdir(exist_ok=True, parents=True)
    (path_dir / 'documents').mkdir(exist_ok=True, parents=True)
    (path_dir / 'audio').mkdir(exist_ok=True, parents=True)
    (path_dir / 'video').mkdir(exist_ok=True, parents=True)
    (path_dir / 'archives').mkdir(exist_ok=True, parents=True)
    (path_dir / 'other').mkdir(exist_ok=True, parents=True)

images_list = []
documents_list = []
audio_list = []
video_list = []
archives_list = []
other_list = []

all_files = {
    'images': images_list,
    'documents': documents_list,
    'audio': audio_list,
    'video': video_list,
    'archives': archives_list,
    'other': other_list,
}

def normalize(name: Path) -> str:
    trans_name = name.name.translate(dict_for_translate)
    trans_name = re.sub(r'\W', '_', trans_name[:-(len(name.suffix)):])
    trans_name =  f'{trans_name}{name.suffix}'
    return trans_name

def delete_dirs(path: Path) -> None:
    for object in path.iterdir():
        if object.is_dir() and object.name in ('archives', 'video', 'audio', 'documents', 'images', 'other'):
            continue
        shutil.rmtree(object)

def looking_files(path) -> None:
    for object in path.iterdir():
        if object.is_dir() and object.name in ('archives', 'video', 'audio', 'documents', 'images', 'other'):
            continue
        if object.is_dir():
            looking_files(object)
        else:
            if object.suffix[1:] in ('jpeg', 'png', 'jpg', 'svg'):
                images_list.append(normalize(object))
                shutil.move(object, parents_path / 'images' / normalize(object))
                continue
            if object.suffix[1:] in ('doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'):
                documents_list.append(normalize(object))
                shutil.move(object, Path(parents_path / 'documents' / normalize(object)))
                continue
            if object.suffix[1:] in ('mp3', 'ogg', 'wav', 'amr'):
                audio_list.append(normalize(object))
                shutil.move(object, parents_path / 'audio' / normalize(object))
                continue
            if object.suffix[1:] in ('avi', 'mp4', 'mov', 'mkv'):
                video_list.append(normalize(object))
                shutil.move(object, parents_path / 'video' / normalize(object))
                continue
            if object.suffix[1:] in ('zip', 'zg', 'tar'):
                (parents_path / 'archives' / normalize(object).replace(object.suffix, '')).mkdir(exist_ok=True, parents=True)
                shutil.unpack_archive(object, parents_path / 'archives' / normalize(object).replace(object.suffix, ''))
                archives_list.append(normalize(object))
                shutil.move(object, parents_path / 'archives' / normalize(object))
                continue
            elif object.suffix[1:] != '':
                other_list.append(normalize(object))
                shutil.move(object, parents_path / 'other' / normalize(object))
        continue

def main():
    try:
        global parents_path
        folder_for_scan = Path(sys.argv[1])
        parents_path = Path(sys.argv[1])
    except IndexError:
        Exception
        print('You did not enter an argument')
    create_folders(folder_for_scan)
    looking_files(folder_for_scan)
    delete_dirs(folder_for_scan)
    print(all_files)


if __name__ == '__sort__':
    main()

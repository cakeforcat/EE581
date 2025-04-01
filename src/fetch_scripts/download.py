import shutil
from inspect import cleandoc

import requests
from tqdm import tqdm
import zipfile
import os
import pathlib

def download_data(source, path, clean=False):
    match source:
        case 0:
            # CAS
            url = 'https://zenodo.org/api/records/10294997/files-archive'
        case 1:
            # Landslide4Sense
            url = 'https://zenodo.org/api/records/10463239/files-archive'
        case _:
            raise ValueError('Invalid data set index')

    if clean and path.exists():
        shutil.rmtree(path)
        print(f'Cleaned {path}!')

    # create directory if it doesn't exist
    if not path.exists():
        os.makedirs(path)
        print(f'Created {path}!')

    print('Downloading data set...')
    # download data set
    response = requests.get(url, stream=True)
    with open(path / 'data.zip', 'wb') as handle:
        for data in tqdm(response.iter_content(chunk_size=1024), unit="kB"):
            handle.write(data)
    print('Download complete!')

    # extract data set
    print('Extracting data set...')
    with zipfile.ZipFile(path / 'data.zip', 'r') as top_zip_ref:
        top_zip_ref.extractall(path)
    print('Extracted top zip file')
    # extract extracted archives into folders with same name
    for file in list(path.glob('*.zip')):
        # skip extra files and delete them
        if file.stem == 'data' or file.stem == 'study areas shp':
            os.remove(file)
            continue

        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(path) if source == 1 else zip_ref.extractall(path / file.stem)
        os.remove(file)
        print(f'Extracted {file.stem}!')
    os.remove(path / 'CAS Landslide Dataset README.html') if source == 0 else None
    print('Extraction complete!')


# fix folder names by replacing '（' and '）' with '(' and ')'
def fix_folder_names(path):
    for folder in list(path.glob('*')):
        if '（' in folder.name or '）' in folder.name:
            new_name = folder.name.replace('（', '(').replace('）', ')')
            folder.rename(path / new_name)
            print(f'Fixed {folder.name} to {new_name}!')

def delete_extra_cas(store_path):
    for folder in list(store_path.glob('*')):
        if folder.is_dir():
            # remove the 'mask' dir and files in it
            mask_dir = folder / 'mask'
            if mask_dir.exists():
                shutil.rmtree(mask_dir)
                print(f'Removed {mask_dir}!')


if __name__ == '__main__':
    dataset = input('choose dataset (0 for CAS, 1 for [Landslide4Sense]): ')
    dataset = int(dataset) if dataset.isnumeric() else 1
    match dataset:
        case 0:
            path = pathlib.Path('../../data/CAS_original')
        case 1:
            path = pathlib.Path('../../data/Landslide4Sense_original')
        case _:
            raise ValueError('Invalid data set index')

    # download data set
    clean = input('Clean installation? ([y]/n): ')
    clean = True if clean.lower() == 'y' or clean == '' else False
    download_data(dataset, path, clean=True)
    # fix folder names
    fix_folder_names(path)
    # delete extra CAS files
    delete_extra_cas(path) if dataset == 0 else None
    print('All done!')
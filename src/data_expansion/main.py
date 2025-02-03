# imports
import cv2 as cv
from pathlib import Path
import numpy
from tqdm import tqdm
import requests
import zipfile
import os

# download data set if not present in ../../data/original_dataset
def download_dataset(store_path, data_url):
    # check if folder is empty
    if not list(store_path.glob('*')):
        print('Downloading data set...')
        # download data set
        response = requests.get(data_url, stream=True)
        with open(store_path / 'data.zip', 'wb') as handle:
            for data in tqdm(response.iter_content(chunk_size=1024), unit="kB"):
                handle.write(data)
        print('Download complete!')

        # extract data set
        print('Extracting data set...')
        with zipfile.ZipFile(store_path / 'data.zip', 'r') as top_zip_ref:
            top_zip_ref.extractall(store_path)
        print('Extracted top zip file')
        # extract extracted archives into folders with same name
        for file in list(store_path.glob('*.zip')):
            # skip extra files and delete them
            if file.stem == 'data' or file.stem == 'study areas shp':
                os.remove(file)
                continue

            with zipfile.ZipFile(file, 'r') as zip_ref:
                zip_ref.extractall(data_path / file.stem)

            os.remove(file)
            print(f'Extracted {file.stem}!')
        os.remove(data_path / 'CAS Landslide Dataset README.html')
        print('Extraction complete!')
    else:
        print('Data folder not empty, skipping download!')

# fix folder names by replacing '（' and '）' with '(' and ')'
def fix_folder_names(store_path):
    for folder in list(store_path.glob('*')):
        if '（' in folder.name or '）' in folder.name:
            new_name = folder.name.replace('（', '(').replace('）', ')')
            folder.rename(data_path / new_name)
            print(f'Fixed {folder.name} to {new_name}!')

if __name__ == '__main__':
    # download data set if not present in ../../data/original_dataset
    data_url = 'https://zenodo.org/api/records/10294997/files-archive'
    data_path = Path('..') / '..' / 'data' / 'original_dataset'
    download_dataset(data_path, data_url)

    # fix folder names
    fix_folder_names(data_path)

    # list available data sets (only folders)
    print('Available data sets:')
    for i, folder in enumerate(list(data_path.glob('*'))):
        if folder.is_dir():
            print(f'{i}: {folder.name}')
    # select data set
    data_set = input('Select data set (index): ')
    # load data set
    data_set_path = data_path / list(data_path.glob('*'))[int(data_set)]
    # load all original images and labels into lists
    images = []
    labels = []
    print(f'Selected {data_set_path.name}, reading images and labels...')
    for org_file in list(data_set_path.joinpath('img').glob('*')):
        images.append(cv.imread(str(org_file)))
    for label_file in list(data_set_path.joinpath('label').glob('*')):
        labels.append(cv.imread(str(label_file)))
    print('Read images and labels!')
    # rotate images and labels by random angle while preserving size, then save them in a new folder in ../../data/rotated_dataset
    # keep image in 'img' folder and label in 'label' folder
    # fill outside of image with white
    # threshold label to 0 and 255
    # save images as .tif

    # create new folder in ../../data/rotated_dataset and subfolders 'img' and 'label'
    rotated_path = Path('..') / '..' / 'data' / 'rotated_dataset' / data_set_path.name
    rotated_path.mkdir(parents=True, exist_ok=True)
    rotated_path.joinpath('img').mkdir(parents=True, exist_ok=True)
    rotated_path.joinpath('label').mkdir(parents=True, exist_ok=True)
    # clear folders
    for file in list(rotated_path.joinpath('img').glob('*')):
        os.remove(file)
    for file in list(rotated_path.joinpath('label').glob('*')):
        os.remove(file)

    print('Rotating images and labels...')
    # rotate images and labels
    for i, (image, label) in enumerate(zip(images, labels)):
        # rotate image and label
        angle = numpy.random.randint(0, 360)
        image_center = (image.shape[1]//2, image.shape[0]//2)
        rot_mat = cv.getRotationMatrix2D(image_center, angle, 1.0)
        image_rot = cv.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv.INTER_LINEAR, borderValue=(255, 255, 255))
        label_rot = cv.warpAffine(label, rot_mat, label.shape[1::-1], flags=cv.INTER_LINEAR, borderValue=(255, 255, 255))
        # threshold label
        _, label_rot = cv.threshold(label_rot, 127, 255, cv.THRESH_BINARY)
        # save image and label
        cv.imwrite(str(rotated_path.joinpath('img').joinpath(f'r_{data_set_path.name.replace(" ", "_")}_{str(i).zfill(4)}.tif')), image_rot)
        cv.imwrite(str(rotated_path.joinpath('label').joinpath(f'r_{data_set_path.name.replace(" ", "_")}_{str(i).zfill(4)}.tif')), label_rot)

    print('Rotated images and labels!')






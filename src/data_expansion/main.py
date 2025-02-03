# imports
import cv2 as cv
from pathlib import Path
import numpy
from tqdm import tqdm
import requests
import zipfile
import os

# download data set if not present in ../../data/original_dataset
def download_dataset():
    data_path = Path('..') / '..' / 'data' / 'original_dataset'
    data_url = 'https://zenodo.org/api/records/10294997/files-archive'
    # check if folder is empty
    if not list(data_path.glob('*')):
        print('Downloading data set...')
        # download data set
        response = requests.get(data_url, stream=True)
        with open(data_path / 'data.zip', 'wb') as handle:
            for data in tqdm(response.iter_content(chunk_size=1024), unit="kB"):
                handle.write(data)
        print('Download complete!')

        # extract data set
        print('Extracting data set...')
        with zipfile.ZipFile(data_path / 'data.zip', 'r') as top_zip_ref:
            top_zip_ref.extractall(data_path)
        print('Extracted top zip file')
        # extract extracted archives into folders with same name
        for file in list(data_path.glob('*.zip')):
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

if __name__ == '__main__':
    # download data set if not present in ../../data/original_dataset
    download_dataset()
    # load data set
    data_path = Path('..') / '..' / 'data' / 'original_dataset'
    # list available data sets (only folders)
    print('Available data sets:')
    for i, folder in enumerate(list(data_path.glob('*'))):
        if folder.is_dir():
            print(f'{i+1}: {folder.stem}')
    # select data set
    data_set = input('Select data set (index): ')
    # load data set
    data_set_path = data_path / list(data_path.glob('*'))[int(data_set)-1].stem
    # load all original images and labels into lists
    images = []
    labels = []
    for file in list(data_set_path.joinpath('img').glob('*')):
        images.append(cv.imread(str(file)))
    for file in list(data_set_path.joinpath('label').glob('*')):
        labels.append(cv.imread(str(file)))

    # rotate images and labels by random angle while preserving size, then save them in a new folder in ../../data/rotated_dataset
    # keep image in 'img' folder and label in 'label' folder
    # fill outside of image with white
    # threshold label to 0 and 255
    # save images as .tif

    # create new folder in ../../data/rotated_dataset
    rotated_path = Path('..') / '..' / 'data' / 'rotated_dataset' / data_set_path.stem
    rotated_path.mkdir(parents=True, exist_ok=True)
    rotated_path.joinpath('img').mkdir(parents=True, exist_ok=True)
    rotated_path.joinpath('label').mkdir(parents=True, exist_ok=True)
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
        cv.imwrite(str(rotated_path.joinpath('img').joinpath(f'{i}.tif')), image_rot)
        cv.imwrite(str(rotated_path.joinpath('label').joinpath(f'{i}.tif')), label_rot)








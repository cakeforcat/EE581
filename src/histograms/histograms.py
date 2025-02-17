import cv2 as cv
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    data_path = Path('..') / '..' / 'data' / 'original_dataset'
    print('found data sets:')
    sets_idx = []
    for i, folder in enumerate(list(data_path.glob('*'))):
        if folder.is_dir():
            print(f'{i}: {folder.name}')
            sets_idx.append(i)

    for data_set in sets_idx:
        # load data set
        data_set_path = data_path / list(data_path.glob('*'))[int(data_set)]
        # check if images and labels have the same length
        img_files = list(data_set_path.joinpath('img').glob('*'))
        label_files = list(data_set_path.joinpath('label').glob('*'))
        if len(img_files) != len(label_files):
            print(f'Error: number of images and labels do not match for {data_set_path.name}!')
            continue

        # load all original images and labels into lists
        images = []
        labels = []
        print(f'Selected {data_set_path.name}, reading images and labels...')
        for org_file in img_files:
            images.append(cv.imread(str(org_file)))
        for label_file in label_files:
            labels.append(cv.imread(str(label_file)))
        print('Read images and labels!')


        # invert and binarize labels
        for i, label in enumerate(labels):
            labels[i] = cv.threshold(label, 127, 255, cv.THRESH_BINARY_INV)[1]


        # split color channels of each image, convert to a numpy array, flatten and concatenate them
        # as a feature vector
        # feature_vector_table = numpy.zeros((len(images), 3 * images[0].shape[0] * images[0].shape[1]))
        feature_vector_table = np.zeros((3, images[0].shape[0] * images[0].shape[1] * len(images)))
        im_len = images[0].shape[0] * images[0].shape[1]

        for i, image in enumerate(images):
            for j in range(3):
                feature_vector = image[:, :, j].flatten()
                feature_vector_table[j, (i*im_len):((i+1)*im_len)] = feature_vector


        # same but now mask images with labels
        feature_vector_table_masked = np.zeros((3, images[0].shape[0] * images[0].shape[1] * len(images)))
        for i, (image, label) in enumerate(zip(images, labels)):
            for j in range(3):
                feature_vector = cv.bitwise_and(image[:, :, j], label[:, :, j]).flatten()
                feature_vector_table_masked[j, (i*im_len):((i+1)*im_len)] = feature_vector


        # calculate and show histograms
        hist_table = np.zeros((3, 50))
        hist_table_masked = np.zeros((3, 50))
        for i in range(3):
            hist_table[i], _ = np.histogram(feature_vector_table[i], bins=50, range=(1, 254))
            hist_table_masked[i], _ = np.histogram(feature_vector_table_masked[i], bins=50, range=(1, 254))

        # plot histograms
        fig, axs = plt.subplots(2, 3)
        fig.tight_layout(pad=3.0)
        for i, col in enumerate(('r', 'g', 'b')):
            axs[0, i].plot(hist_table[i], color=col)
            axs[0, i].set_title(f'ch: {col}')
            axs[1, i].plot(hist_table_masked[i], color=col)
            axs[1, i].set_title(f'ch: {col} masked')
        plt.savefig(f'histograms_{data_set_path.name}.png')

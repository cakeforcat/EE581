import cv2 as cv
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import itertools
from math import ceil

if __name__ == '__main__':
    data_path = Path('..') / '..' / 'data' / 'CAS_original'
    print('found data sets:')
    sets_idx = []
    for i, folder in enumerate(list(data_path.glob('*'))):
        if folder.is_dir():
            print(f'{i}: {folder.name}')
            sets_idx.append(i)

    batch_size = 500
    nbins = 100
    bin_edges = np.linspace(0, 255, nbins + 1)
    hist_table_total_super = np.zeros((3, nbins))
    hist_table_masked_total_super = np.zeros((3, nbins))
    for data_set in [15, 16]:
        # load data set
        data_set_path = data_path / list(data_path.glob('*'))[int(data_set)]
        # check if images and labels have the same length
        img_files = list(data_set_path.joinpath('img').glob('*'))
        label_files = list(data_set_path.joinpath('label').glob('*'))
        if len(img_files) != len(label_files):
            print(f'Error: number of images and labels do not match for {data_set_path.name}!')
            continue

        # combine image and label lists into a list of tuples
        img_label_pairs = list(zip(img_files, label_files))


        # load the images and labels in batches
        hist_table_total = np.zeros((3, nbins))
        hist_table_masked_total = np.zeros((3, nbins))
        total_batch_len = ceil(len(img_label_pairs)/batch_size)
        print(f'Selected {data_set_path.name}, reading images and labels...')
        for batch_no, batch in enumerate(itertools.batched(img_label_pairs, batch_size)):
            images = []
            labels = []
            for pair in list(batch):
                images.append(cv.imread(str(pair[0])))
                labels.append(cv.imread(str(pair[1])))


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
            hist_table = np.zeros((3, nbins))
            hist_table_masked = np.zeros((3, nbins))
            for i in range(3):
                hist_table[i], _ = np.histogram(feature_vector_table[i], bins=nbins, range=(1, 254))
                hist_table_total[i] += hist_table[i]
                hist_table_masked[i], _ = np.histogram(feature_vector_table_masked[i], bins=nbins, range=(1, 254))
                hist_table_masked_total[i] += hist_table_masked[i]

            print(f'Processed images and labels in batch: {batch_no+1} out of {total_batch_len}!')

        # plot histograms
        fig, axs = plt.subplots(2, 3)
        fig.tight_layout(pad=3.0)
        for i, col in enumerate(('r', 'g', 'b')):
            axs[0, i].hist(bin_edges[:-1], bins=bin_edges,weights=hist_table_total[i], color=col)
            axs[0, i].set_title(f'ch: {col}')
            axs[1, i].hist(bin_edges[:-1], bins=bin_edges,weights=hist_table_masked_total[i], color=col)
            axs[1, i].set_title(f'ch: {col} masked')
        plt.savefig(f'histograms_{data_set_path.name}.png')

        for i in range(3):
            hist_table_total_super[i] += hist_table_total[i]
            hist_table_masked_total_super[i] += hist_table_masked_total[i]

    # plot super histogram
    fig, axs = plt.subplots(2, 3)
    fig.tight_layout(pad=3.0)
    for i, col in enumerate(('r', 'g', 'b')):
        axs[0, i].hist(bin_edges[:-1], bins=bin_edges,weights=hist_table_total_super[i], color=col)
        axs[0, i].set_title(f'ch: {col}')
        axs[1, i].hist(bin_edges[:-1], bins=bin_edges,weights=hist_table_masked_total_super[i], color=col)
        axs[1, i].set_title(f'ch: {col} masked')
    plt.savefig(f'histograms_{data_path.name}.png')

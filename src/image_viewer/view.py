import pathlib
import cv2 as cv
import h5py
import numpy as np

def read_images(datagroup, dataset, index):

    image_path = pathlib.Path('..') / '..' / 'data' / datagroup / dataset / 'img'
    label_path = pathlib.Path('..') / '..' / 'data' / datagroup / dataset
    if (label_path / 'label').exists():
        label_path = label_path / 'label'
    else:
        label_path = label_path / 'mask'

    images = list(image_path.glob('*'))
    labels = list(label_path.glob('*'))

    if images[index].suffix == '.h5' or labels[index].suffix == '.h5':
        with h5py.File(images[index], 'r') as f:
            image = f['img'][:]
        with h5py.File(labels[index], 'r') as f:
            label = f['mask'][:]

        image = np.asarray(image, np.float32)
        label = np.asarray(label, np.float32)
        image = image.transpose((-1, 0, 1))

        chs = input('Multispectral image! select channels (0-13) or 3 channels to map to RGB (i.e. 1 or 3,4,5): ')
        chs.split(',')
        chs = [int(ch) for ch in chs.split(',')]
        if len(chs) == 1:
            image = image[chs[0], :, :]
        elif len(chs) == 3:
            image = image[chs, :, :].transpose((1, 2, 0))
            label = np.array([label, label, label]).transpose((1, 2, 0))
        else:
            raise ValueError('Invalid number of channels selected!')

        image = cv.resize(image, (512, 512), interpolation=cv.INTER_AREA)
        label = cv.resize(label, (512, 512), interpolation=cv.INTER_NEAREST)
    else:
        image = cv.imread(str(images[index]))
        label = cv.imread(str(labels[index]))

    # return image and label as tuple
    return image, label

def main():
    # list available non empty data groups
    data_path = pathlib.Path('..') / '..' / 'data'
    print('Available data groups:')
    for i, group in enumerate(list(data_path.glob('*'))):
        if len(list(group.glob('*'))) > 0:
            print(f'{i}: {group.name}')
    # select data group
    data_group = input('Select data group (index): ')
    # list available data sets (only folders)
    data_group_path = list(data_path.glob('*'))[int(data_group)]
    print(f'Selected {data_group_path.name}, available data sets:')
    for i, dataset in enumerate(list(data_group_path.glob('*'))):
        if dataset.is_dir():
            print(f'{i}: {dataset.name}')
    # select data set
    data_set = input('Select data set (index): ')
    # list the number of images in the selected data set
    data_set_path = list(data_group_path.glob('*'))[int(data_set)]
    print(f'Selected {data_set_path.name}, available images:')
    image_path = data_set_path / 'img'
    print(f'Number of images: {len(list(image_path.glob("*")))}')
    # select image from available images
    image = input('Select image (index): ')
    # view images and overlayed
    img, lab = read_images(data_group_path.name, data_set_path.name, int(image))
    overlayed = cv.addWeighted(img, 0.5, lab, 0.5, 0)

    # show image and label side by side in the same window
    cv.imshow(f'Group: {data_group_path.name}, Set: {data_set_path.name}, File: {list(image_path.glob("*"))[int(image)].name}'
              , cv.hconcat([img, lab]))
    # show overlayed image and label
    cv.imshow('Overlayed image and label', overlayed)
    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()

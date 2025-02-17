import pathlib
import cv2 as cv

def images(datagroup, dataset, index):
    image_path = pathlib.Path('..') / '..' / 'data' / datagroup / dataset / 'img'
    label_path = pathlib.Path('..') / '..' / 'data' / datagroup / dataset / 'label'
    images = list(image_path.glob('*'))
    labels = list(label_path.glob('*'))
    image = cv.imread(str(images[index]))
    label = cv.imread(str(labels[index]))

    # return image and label as tuple
    return image, label


def overlayed_images(datagroup, dataset, index):
    image_path = pathlib.Path('..') / '..' / 'data' / datagroup / dataset / 'img'
    label_path = pathlib.Path('..') / '..' / 'data' / datagroup / dataset / 'label'
    images = list(image_path.glob('*'))
    labels = list(label_path.glob('*'))
    image = cv.imread(str(images[index]))
    label = cv.imread(str(labels[index]))
    label = cv2.bitwise_not(label)

    # return overlayed image and label
    return cv.addWeighted(image, 0.5, label, 0.5, 0)

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
    img, lab = images(data_group_path.name, data_set_path.name, int(image))
    overlayed = overlayed_images(data_group_path.name, data_set_path.name, int(image))

    # show image and label side by side in the same window
    cv.imshow(f'Group: {data_group_path.name}, Set: {data_set_path.name}, File: {list(image_path.glob("*"))[int(image)].name}'
              , cv.hconcat([img, lab]))
    # show overlayed image and label
    cv.imshow('Overlayed image and label', overlayed)
    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()

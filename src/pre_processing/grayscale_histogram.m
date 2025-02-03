clear all;
close all;
clc;

% applies 9x9 median filter on all images in dataset. takes roughly 30 mins to execute. 

% work with relatvie paths to data
originalDataset =   '..\..\data\original_dataset\';
medianFiltDataset = '..\..\data\grayscale_histogram_classified\';

subfolders_all = dir(fullfile(originalDataset));
subfolders = {};

% store all valid file names to variable subfolders
for i=1:length(subfolders_all)
    if ~subfolders_all(i).isdir || ...
        (strcmp(subfolders_all(i).name,'.')) || ...
        (strcmp(subfolders_all(i).name,'..'))
        continue
    end
    subfolders{end+1} = subfolders_all(i).name;
end

% iterate over every subfolder of dataset
for i=1:length(subfolders)
    images = dir(fullfile(originalDataset, subfolders{i}, 'img', '*.tif'));

    % create output directory
    filtered_im_location = strcat(medianFiltDataset, subfolders{i}, '\img\');
    if ~exist(filtered_im_location, 'dir')
        mkdir(filtered_im_location);            
    end

    for j=1:length(images)

        image_path = strcat(images(j).folder, '\', images(j).name);
        im = imread(image_path);

        im_gray = rgb2gray(im);

        figure(1);
        subplot(1,2,1);
        imshow(im_gray);

        subplot(1,2,2);
        histogram(im_gray);

    end


end


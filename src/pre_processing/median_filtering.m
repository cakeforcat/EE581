clear all;
close all;
clc;

% applies 9x9 median filter on all images in dataset. takes roughly 30 mins to execute. 

% work with relatvie paths to data
originalDataset =   '..\..\data\original_dataset\';
medianFiltDataset = '..\..\data\median_filtered\';

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

    % iterate over every image in each subfolder and apply median filter
    for j=1:length(images)
        image_path = strcat(images(j).folder, '\', images(j).name);
        im = imread(image_path);
        
        filt_im(:,:,1) = medfilt2(im(:,:,1), [9, 9]);
        filt_im(:,:,2) = medfilt2(im(:,:,2), [9, 9]);
        filt_im(:,:,3) = medfilt2(im(:,:,3), [9, 9]);

        imwrite(filt_im, strcat(filtered_im_location, images(j).name));
    end
end


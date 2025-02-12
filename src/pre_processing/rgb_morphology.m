clear all;
close all;
clc;


% work with relatvie paths to data
originalDataset =   '..\..\data\original_dataset\';
dilatedDataset = '..\..\data\dilated\';

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
    subfolders{i} % print name for tracking process

    images = dir(fullfile(originalDataset, subfolders{i}, 'img', '*.tif'));

    % create output directory
    processed_im_location = strcat(dilatedDataset, subfolders{i}, '\img\');
    if ~exist(processed_im_location, 'dir')
        mkdir(processed_im_location);            
    end

    for j=1:length(images)

        image_path = strcat(images(j).folder, '\', images(j).name);
        im = imread(image_path);

        se = strel('disk', 4);
        im_dilated = imdilate(im, se);

        % figure(1);
        % subplot(1,2,1);
        % imshow(im);
        % title('Original');
        % 
        % subplot(1,2,2);
        % imshow(im_dilated);
        % title('Dilated');

        imwrite(im_dilated, strcat(processed_im_location, images(j).name));

    end
end

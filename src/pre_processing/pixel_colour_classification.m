clear all;
close all;
clc;

% work with pixel based classification, script is work in progress at this
% stage.

% work with relatvie paths to data
originalDataset =   '..\..\data\median_filtered\';
medianFiltDataset = '..\..\data\pixel_colour_classification\';

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
%for i=1:length(subfolders)
for i=3:4
    images = dir(fullfile(originalDataset, subfolders{i}, 'img', '*.tif'));

    % create output directory
    filtered_im_location = strcat(medianFiltDataset, subfolders{i}, '\img\');
    if ~exist(filtered_im_location, 'dir')
        mkdir(filtered_im_location);            
    end

    % iterate over every image in each subfolder apply pixel operations
    for j=1:length(images)
        image_path = strcat(images(j).folder, '\', images(j).name);
        im = imread(image_path);
        im_hsv = rgb2hsv(im);
        h = im_hsv(:,:,1);
        s = im_hsv(:,:,2);
        v = im_hsv(:,:,3);

        figure(1);
        subplot(2, 4, 1);
        histogram(h);
        title('Hue')

        subplot(2, 4, 2);
        histogram(s);
        title('Saturation');

        subplot(2, 4, 3);
        histogram(v);
        title('Value');

        subplot(2, 4, 4);
        imshow(im);
        
        brown_spots = find_brownish_spots(im_hsv);

        subplot(2, 4, 5);
        imshow(brown_spots);
        title('Brown Spots');

        bright_brown_spots = find_bright_brown_spots(im);

        subplot(2, 4, 6);
        imshow(bright_brown_spots);
        title('Bright Spots');

        subplot(2, 4, 7);
        im_combined = brown_spots | bright_brown_spots;
        imshow(im_combined);
        title('Brown and Bright Spots');

        se = strel('disk', 4);
        im_opening = imopen(im_combined, se);

        subplot(2, 4, 8);
        imshow(im_opening);
        title('Combined Image Eroded');

    end
end


%% functions
function mask_brown = find_brownish_spots(image_hsv) 

    mask_brown = image_hsv(:,:,1) > 0.025 & image_hsv(:,:,1) < 0.085  & ...
                 image_hsv(:,:,2) > 0.1 & image_hsv(:,:,2) < 0.5 & ...
                 image_hsv(:,:,3) > 0.3 & image_hsv(:,:,3) < 0.9;
end

function mask_white = find_bright_brown_spots(image_rgb)
    mask_white = image_rgb(:,:,1) > 200 & ...
                 image_rgb(:,:,2) > 150 & ...
                 image_rgb(:,:,3) > 150;
end

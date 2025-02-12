clear all;
close all;
clc;


% work with relatvie paths to data
originalDataset =   '..\..\data\original_dataset\';
grayscaleFiltDataset = '..\..\data\grayscale_histogram_classified\';

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

image_counter = 0;
pixels_in_masks = 0;
correctly_classified_pixels = 0;
wrongly_classified_pixels = 0;
not_classified_pixels = 0;

% iterate over every subfolder of dataset
for i=1:length(subfolders)
    subfolders{i} % print name for tracking process

    classified_images = dir(fullfile(grayscaleFiltDataset, subfolders{i}, 'img', '*.tif'));
    masks = dir(fullfile(originalDataset, subfolders{i}, 'mask', '*.tif'));

    for j=1:length(classified_images)

        if mod(j, 100) == 0
            j
        end

        image_counter = image_counter + 1;

        image_path = strcat(classified_images(j).folder, '\', classified_images(j).name);
        im = imread(image_path);

        mask_path = strcat(masks(j).folder, '\', masks(j).name);
        mask = imread(mask_path);
        mask = mask > 0;  % mask is uint8 and not logical

        pixels_in_masks = pixels_in_masks + sum(mask, 'all');
        correctly_classified_pixels = correctly_classified_pixels + sum(im & mask, 'all');
        wrongly_classified_pixels = wrongly_classified_pixels + sum(im & ~mask, 'all');
        not_classified_pixels = not_classified_pixels + sum(~im & mask, 'all');

        % figure(1);
        % subplot(1,3,1);
        % imshow(im);
        % title('Classified Image');
        % 
        % subplot(1,3,2);
        % imshow(mask);
        % title('Mask');
        % 
        % diff(:,:,1) = im & mask;
        % diff(:,:,2) = im & ~mask;
        % diff(:,:,3) = ~im & mask;
        % 
        % diff = diff * 255;
        % 
        % subplot(1,3,3);
        % imshow(double(diff));
        % title('Differences: r=same, g=im & !mask, b = !im & mask');

    end
end

correct_percent = correctly_classified_pixels / pixels_in_masks;

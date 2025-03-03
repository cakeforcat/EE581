clear all;
close all;
clc;


% work with relatvie paths to data
% change as necessary
originalDataset =   '..\data\original_dataset\';
modifiedDataset = '..\data\grayscale_histogram_classified\';

subfolders_all = dir(fullfile(modifiedDataset));
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

true_pos = 0;
false_pos = 0;
true_neg = 0;
false_neg = 0;

% iterate over every subfolder of dataset
for i=1:length(subfolders)
    subfolders{i} % print name for tracking process

    classified_images = dir(fullfile(modifiedDataset, subfolders{i}, 'img', '*.tif'));
    masks = dir(fullfile(originalDataset, subfolders{i}, 'mask', '*.tif'));

    for j=1:length(classified_images)

        if mod(j, 100) == 0
            j
        end

        image_path = strcat(classified_images(j).folder, '\', classified_images(j).name);
        im = imread(image_path);

        mask_path = strcat(masks(j).folder, '\', masks(j).name);
        mask = imread(mask_path);
        mask = mask > 0;  % mask is uint8 and not logical

        true_pos = true_pos + sum(im & mask, 'all');
        false_pos = false_pos + sum(im & ~mask, 'all');
        false_neg = false_neg + sum(~im & mask, 'all');
    end
end

precision = true_pos / (true_pos + false_pos);
recall = true_pos / (true_pos + false_neg);

f1_score = (2 * precision * recall ) / (precision + recall)

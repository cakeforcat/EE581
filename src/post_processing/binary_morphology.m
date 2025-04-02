clear all;
close all;
clc;


% work with relatvie paths to data
originalMasks =   '..\..\data\model_output\predictions\';
processedMasks = '..\..\data\model_output\predictions_morphology\';

masks_files = dir(fullfile(originalMasks, '*.jpg'));

if ~exist(processedMasks, 'dir')
    mkdir(processedMasks);            
end

for i=1:length(masks_files)

    masks_path = fullfile(originalMasks, masks_files(i).name);
    mask = imread(masks_path);
    mask = mask > 0;

    se = strel('disk', 4);
    im_morphology = imdilate(mask, se);

    imwrite(im_morphology, strcat(processedMasks, masks_files(i).name));
end

clear all;
close all;
clc;


% work with relatvie paths to data
% change as necessary
labels =   '..\data\model_output\labels\';
masks = '..\data\model_output\predictions_morphology\';

label_files = dir(fullfile(labels, '*.jpg'));
masks_files = dir(fullfile(masks, '*.jpg'));

true_pos = 0;
false_pos = 0;
true_neg = 0;
false_neg = 0;

% iterate over every image
for i=1:length(label_files)

    labels_path = fullfile(labels, label_files(i).name);
    im = imread(labels_path);
    im = im > 0;

    masks_path = fullfile(masks, masks_files(i).name);
    mask = imread(masks_path);
    mask = mask > 0;

    true_pos = true_pos + sum(im & mask, 'all');
    false_pos = false_pos + sum(im & ~mask, 'all');
    false_neg = false_neg + sum(~im & mask, 'all');
end

precision = true_pos / (true_pos + false_pos);
recall = true_pos / (true_pos + false_neg);

f1_score = (2 * precision * recall ) / (precision + recall)

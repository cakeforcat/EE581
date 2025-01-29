clear all;
close all;
clc;

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



clear all;
close all;
clc;

% Histogram based classification of landslides based on grayscale images.
% General idea is that generally, landslides are really bright spots.
% Therefore extract these spots and classify them as landslides. In
% general, this is probably only useful if forests or grassy locations, and
% won't work with bodies of water or streets etc.

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
% for i=1:length(subfolders)
for i=2:3    
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

        im_gray = remove_white_areas(im_gray);

        % calculate histogram with n bins, transform image to 1D vector for
        % that
        n_bins = 100;
        h = hist(double(reshape(im_gray, 1, 512*512)), n_bins);

        figure(2);
        bar(0:n_bins-1, h); % plot histogram from 0 to 255 pixel values

        % search for max value of the top 2/3 of the histogram
        upper_area_to_search = 2/3;
        [max_upper, idx] = max(h(upper_area_to_search*n_bins:n_bins));
        idx = idx + upper_area_to_search*n_bins; % readjust index to whole span of histogram
        
        % calculate number of not black pixels
        not_black_pixels = sum(im_gray > 0);
        
        % if the max value of the upper part of hist is more than 10 % of
        % all non black pixels, landslide is probably present
        if max_upper > not_black_pixels * 0.1
            % every pixel that is greater than pixel value -20 is probably
            % part of the landslide. Open image for smoothing
            classified_img = im_gray > (idx*(256/n_bins)-20);
            se = strel('disk', 3);
            classified_img = imopen(classified_img, se);
        else
            % create logical 0 image
            classified_img = logical(zeros(512,512));
        end
        
        figure(3);
        imshow(classified_img);
    end
end

function image_white_areas_removed = remove_white_areas(original_image)

    % output is original image for now
    image_white_areas_removed = original_image;

    % detect lines and obtain them
    edges = edge(original_image, 'canny');
    [H, theta, rho] = hough(edges);
    peaks = houghpeaks(H,30);   % get 30 most promenent peaks in hough space
    if ~isempty(peaks)
        lines = houghlines(edges, theta, rho, peaks, 'FillGap', 200, 'MinLength', 10);
    end


    figure(1);
    subplot(1,4,1);
    imshow(edges);  % plot detected edges

    subplot(1,4,2); % plot hough transform
    imshow(imadjust(rescale(H)),[],...
       'XData',theta,...
       'YData',rho,...
       'InitialMagnification','fit');
    xlabel('\theta (degrees)')
    ylabel('\rho')
    colormap(gca,hot)
    hold on;
    x = theta(peaks(:,2));
    y = rho(peaks(:,1));
    plot(x,y,'s','color','green', 'LineWidth',2);
    axis on;
    axis normal;
    hold off;

    subplot(1,4,3);
    imshow(original_image); % plot original image
    hold on;

    % for each line, see if it separated the useful image and white space,
    % remove white space if it does, iterate over every line detected
    for i=1:length(lines)
        xy = [lines(i).point1; lines(i).point2];
        if xy(1,1) > xy(2,1)    % swap starting points if x2 > x1, otherwise x_fit below has invalid value
            temp = xy(1,:);
            xy(1,:) = xy(2,:);
            xy(2,:) = temp;
        end
        plot(xy(:,1),xy(:,2),'LineWidth',1,'Color','red');  % plot lines over original image

        % get a polynom description of the line based on its start and end points in the form y = ax + m
        polynom_description = polyfit( [xy(1,1), xy(2,1)], [xy(1,2), xy(2,2)], 1);
  
        x_fit = xy(1,1) : xy(2,1); % create x vector of points on line
        if length(x_fit) < 5    % if line is very short, ignore it
            continue;
        end
     
        y_fit = round(polyval(polynom_description, x_fit)); % create y vector of points on line

        % check if either the area above or below the line is completely
        % white, over all of line and increase counter
        white_area_detected = 0;
        for j=1:length(x_fit)
            res1 = all(original_image(6:(y_fit(j) - 5), x_fit(j)) == 255, 'all')
            res2 = all(original_image((y_fit(j) + 5):506, x_fit(j)) == 255, 'all')
            if ( res1 | res2 )
                white_area_detected = white_area_detected + 1;
            end
        end
        
        % if area above or below line is not white over the whole line,
        % continue with next line in list
        if white_area_detected < (length(x_fit) - 10)
            continue;
        end

        % do another line fit, this time extend the line to the edges of
        % the image
        x_fit = 1:512;  % x line points stretches over whole image
        y_fit = round(polyval(polynom_description, x_fit));

        % only use points that are within the image
        valid_y_idx = y_fit >= 1 & y_fit <= 512;
        
        % over the whole image, colour the white areas black
        for j=1:512
            if valid_y_idx(j)
                if all(original_image(1:y_fit(j) - 5, j) == 255, 'all')
                    image_white_areas_removed(1:y_fit(j), j) = 0;
                elseif all(original_image((y_fit(j) + 5):512, j) == 255, 'all')
                    image_white_areas_removed((y_fit(j) + 1):512, j) = 0;
                end
            end
        end
        break;
    end
    
    subplot(1,4,4); % show output image
    imshow(image_white_areas_removed);
end


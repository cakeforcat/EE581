#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 21:55:54 2025

@author: frankconway
"""

from PIL import Image
import os

def convert_tiff_to_png(input_path, output_path=None):
    """
    Convert a TIFF image to PNG format.
    
    Parameters:
    input_path (str): Path to the input TIFF file
    output_path (str, optional): Path for the output PNG file. If not provided,
                                uses the same name as input with .png extension
    
    Returns:
    str: Path to the saved PNG file
    """
    try:
        # Open the TIFF image
        with Image.open(input_path) as img:
            # If output path not provided, create one from input path
            if output_path is None:
                output_path = os.path.splitext(input_path)[0] + '.png'
            
            # Save as PNG
            img.save(output_path, 'PNG')
            return output_path
    except Exception as e:
        raise Exception(f"Error converting {input_path}: {str(e)}")

def batch_convert_directory(input_dir, output_dir=None):
    """
    Convert all TIFF files in a directory to PNG format.
    
    Parameters:
    input_dir (str): Directory containing TIFF files
    output_dir (str, optional): Directory for output PNG files.
                               If not provided, uses input directory
    
    Returns:
    list: List of paths to converted files
    """
    if output_dir is None:
        output_dir = input_dir
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    converted_files = []
    
    # Process all .tif and .tiff files in the directory
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.tif', '.tiff')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, 
                                     os.path.splitext(filename)[0] + '.png')
            
            try:
                convert_tiff_to_png(input_path, output_path)
                converted_files.append(output_path)
            except Exception as e:
                print(f"Failed to convert {filename}: {str(e)}")
    
    return converted_files


    
# in_tif = "/Users/frankconway/Library/CloudStorage/OneDrive-Personal/Strathclyde/Strathclyde/Year5/EE581/Project/EE581/data/original_dataset/palu/img/Palu0001.tif"
# out_png = "Palu0001.png"

# convert_tiff_to_png(in_tif, out_png)

# # Convert all TIFF files in a directory
# batch_convert_directory("input_directory", "output_directory")


main_path = "../../../data/original_dataset/"

dirs = os.listdir(main_path)


# if ".DS_Store" in dirs: dirs.remove(".DS_Store")

print(len(dirs))

exclude = ['Tiburon Peninsula(Sentinel)','.DS_Store','.gitignore','Longxi River(UAV)']

for item in exclude:
    if item in dirs :
        dirs.remove(item)

print(len(dirs))

out_path = "../../../data/png"

isExist = os.path.exists(out_path)
if not isExist:

   # Create a new directory because it does not exist
   os.makedirs(out_path)
   os.makedirs(out_path+"/img")
   os.makedirs(out_path+"/label")
   


for folder in dirs:
    try: 
        for typ in ["img","label"]:
            in_dir = os.path.join(main_path,folder,typ)
            out_dir = os.path.join(out_path,typ)
            
            batch_convert_directory(in_dir, out_dir)
        print(f"Finsihed: {folder}")
        
    except Exception as e:
        print(f"Error with File: {folder} with error {e}")





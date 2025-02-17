#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 08:56:41 2025

@author: frankconway
"""

import os

# Define folder paths
img_folder = "../../../data/png/img"
label_folder = "../../../data/png/label"

# Get sets of filenames (without extensions)
img_files = {os.path.splitext(f)[0] for f in os.listdir(img_folder)}
label_files = {os.path.splitext(f)[0] for f in os.listdir(label_folder)}

# Find unmatched files
img_only = img_files - label_files
label_only = label_files - img_files

# Remove unmatched files
for f in img_only:
    file_path = os.path.join(img_folder, f + os.path.splitext(os.listdir(img_folder)[0])[-1])
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Removed {file_path}")

for f in label_only:
    file_path = os.path.join(label_folder, f + os.path.splitext(os.listdir(label_folder)[0])[-1])
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Removed {file_path}")

print("Cleanup complete.")

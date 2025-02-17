#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 11:37:27 2025

@author: frankconway
"""

from PIL import Image

img = "/Users/frankconway/Library/CloudStorage/OneDrive-Personal/Strathclyde/Strathclyde/Year5/EE581/Project/EE581/src/pre_processing/batchTraining/Palu0001.png"

image = Image.open(img)

width, height = image.size

print(f"The image resolution is: {width}x{height}")


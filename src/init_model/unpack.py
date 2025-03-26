import numpy as np
from PIL import Image

import os
files = [f for f in os.listdir('.') if os.path.isfile(f)]

data = np.load("src/init_model/pred.npz")
pred_img = data["pred"]
labels = data["lables"]

for i, prediction in enumerate(pred_img):
    im_name = 'pred' + str(i) + '.jpg'
    prediction = np.squeeze(prediction, axis=2)
    image = Image.fromarray((prediction).astype(np.uint8))
    try:
        image.save("data/model_output/predictions/" + im_name)
    except Exception as e:
        print("Failed: " + str(i) + ",   ", e)

for i, label in enumerate(labels):
    im_name = 'label' + str(i) + '.jpg'
    label = np.squeeze(label, axis=2)
    image = Image.fromarray((label).astype(np.uint8))
    try:
        image.save("data/model_output/labels/" + im_name)
    except Exception as e:
        print("Failed: " + str(i) + ",   ", e)
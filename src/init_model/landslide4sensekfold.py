# -*- coding: utf-8 -*-
"""landslide4senseKFold.ipynb

"""

pip install segmentation-models

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import h5py
import glob
import matplotlib.pyplot as plt
# %matplotlib inline
import tensorflow as tf
from tensorflow import keras
import os
os.environ["SM_FRAMEWORK"] = "tf.keras"
import segmentation_models as sm
from segmentation_models import Unet
from keras.layers import Input, Conv2D
from keras.models import Model


import os

im_path_tr = '../../Landslide4Sense/Data/TrainData/img/'
ma_path_tr = "../../Landslide4Sense/Data/TrainData/mask"



print(os.path.isdir(im_path_tr))
print(os.path.isfile(im_path_tr+'/image_1.h5'))

# Testing the dataset

path_single = im_path_tr+"/image_1.h5"
path_single_mask = ma_path_tr+'/mask_1.h5'

import h5py
import numpy as np
import matplotlib.pyplot as plt

# File paths (ensure these are correct for Kaggle)
path_single = im_path_tr+"/image_1.h5"
path_single_mask = ma_path_tr+'/mask_1.h5'

f_data = np.zeros((1, 128, 128, 3))

# Open the HDF5 file
with h5py.File(path_single, 'r') as hdf:
    # Print keys in the HDF5 file
    ls = list(hdf.keys())
    print("Available keys in the HDF5 file:", ls)

    # Check if 'img' key exists
    if 'img' not in ls:
        raise KeyError("'img' key not found in HDF5 file")

    # Load the image data
    data = np.array(hdf.get('img'))
    print("Input data shape:", data.shape)

    # Check the shape to avoid indexing errors
    if data.shape[2] < 14:
        raise ValueError("The data has fewer than 14 channels. Shape:", data.shape)

    # Display a sample image (e.g., Red channel)
    plt.imshow(data[:, :, 3])  # Red channel (adjust as needed)
    plt.title("Red Channel")
    plt.show()

    # Extract specific bands for NDVI calculation
    data_red = data[:, :, 3]
    data_green = data[:, :, 2]
    data_blue = data[:, :, 1]
    data_nir = data[:, :, 7]
    data_swir = data[:, :, 10]

    # MSI = Band1600nm / Band820nm


    # Calculate NDVI (Normalized Difference Vegetation Index)
    data_ndvi = np.divide(data_nir - data_red, np.add(data_nir, data_red), where=(data_nir + data_red) != 0)

    # Store NDVI and other bands in f_data
    f_data[0, :, :, 0] = data_ndvi
    f_data[0, :, :, 1] = data[:, :, 12]
    f_data[0, :, :, 2] = data[:, :, 13]
    print("data_ndvi shape:", data_ndvi.shape, "f_data shape:", f_data.shape)

    # Plot NDVI
    plt.imshow(data_ndvi, cmap='viridis')
    plt.title("NDVI")
    plt.show()

with h5py.File(path_single_mask) as hdf:

    ls = list(hdf.keys())

    print("ls", ls)

    data = np.array(hdf.get('mask'))

    print("input data shape:", data.shape)

    plt.imshow(data)

TRAIN_PATH = r"/kaggle/input/landslide4sense/TrainData/img/*.h5"

TRAIN_MASK = r'/kaggle/input/landslide4sense/TrainData/mask/*.h5'

TRAIN_PATH = im_path_tr+r"/*.h5"

TRAIN_MASK = ma_path_tr+r"/*.h5"



TRAIN_XX = np.zeros((3799, 128, 128, 11))

TRAIN_YY = np.zeros((3799, 128, 128, 1))

all_train = sorted(glob.glob(TRAIN_PATH))

all_mask = sorted(glob.glob(TRAIN_MASK))

"""Train with RGB, NDVI, DEM, and Slop"""

import tensorflow as tf

# Check if GPU is available
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    print(f"GPUs Available: {len(gpus)}")
    for gpu in gpus:
        print(f"GPU Name: {gpu.name}")
else:
    print("No GPUs Available")

for i, (img, mask) in enumerate(zip(all_train, all_mask)):

    print(i, img, mask)

    with h5py.File(img) as hdf:

        ls = list(hdf.keys())

        data = np.array(hdf.get('img'))



        # assign 0 for the nan value

        data[np.isnan(data)] = 0.000001

        # to normalize the data

        mid_rgb = data[:, :, 1:4].max() / 2.0

        mid_4 = data[:, :, 4].max() / 2.0

        mid_5 = data[:, :, 5].max() / 2.0

        mid_6 = data[:, :, 6].max() / 2.0

        mid_7 = data[:, :, 7].max() / 2.0

        mid_8 = data[:, :, 8].max() / 2.0

        mid_slope = data[:, :, 12].max() / 2.0

        mid_elevation = data[:, :, 13].max() / 2.0

        # # ndvi calculation

        data_red = data[:, :, 3]

        data_nir = data[:, :, 7]

        data_ndvi = np.divide(data_nir - data_red,np.add(data_nir, data_red))

        # final array

        TRAIN_XX[i, :, :, 0] = 1 - data[:, :, 3] / mid_rgb  #RED

        TRAIN_XX[i, :, :, 1] = 1 - data[:, :, 2] / mid_rgb #GREEN

        TRAIN_XX[i, :, :, 2] = 1 - data[:, :, 1] / mid_rgb #BLUE

        TRAIN_XX[i, :, :, 3] = 1 - data[:, :, 4]/ mid_5

        TRAIN_XX[i, :, :, 4] = 1 - data[:, :, 5]/ mid_5 #data_ndvi #NDVI

        TRAIN_XX[i, :, :, 5] = 1 - data[:, :, 6]/ mid_5

        TRAIN_XX[i, :, :, 6] = 1 - data[:, :, 7]/ mid_5

        TRAIN_XX[i, :, :, 7] = 1 - data[:, :, 8]/ mid_5

        TRAIN_XX[i, :, :, 8] = 1 - data[:, :, 12] / mid_slope #SLOPE

        TRAIN_XX[i, :, :, 9] = 1 - data[:, :, 13] / mid_elevation #ELEVATION

        TRAIN_XX[i, :, :, 10] = data_ndvi #NDVI





    with h5py.File(mask) as hdf:

        ls = list(hdf.keys())

        data=np.array(hdf.get('mask'))

        TRAIN_YY[i, :, :, 0] = data

"""Testing min, max values in train data¶

"""

TRAIN_XX[np.isnan(TRAIN_XX)] = 0.000001

print(TRAIN_XX.min(), TRAIN_XX.max(), TRAIN_YY.min(), TRAIN_YY.max())

"""### All Channels"""

# Split the data

x = TRAIN_XX[:,:,:,0:10]
y =  TRAIN_YY

import numpy as np

def random_flip(image, mask):
    # Horizontal flip
    if np.random.random() > 0.5:
        image = np.flip(image, axis=1)
        mask = np.flip(mask, axis=1)

    # Vertical flip
    if np.random.random() > 0.5:
        image = np.flip(image, axis=0)
        mask = np.flip(mask, axis=0)

    return image, mask

def random_rotate(image, mask):
    # Random 90-degree rotations
    k = np.random.randint(0, 4)
    image = np.rot90(image, k)
    mask = np.rot90(mask, k)
    return image, mask

def random_jitter(image, mask):
    # Add Gaussian noise
    noise = np.random.normal(0, 0.05, image.shape).astype(image.dtype)
    image = image + noise
    return image, mask

def augment(image, mask):
    image, mask = random_flip(image, mask)
    image, mask = random_rotate(image, mask)
    image, mask = random_jitter(image, mask)
    return image, mask

def augment_dataset(x_train, y_train):
    augmented_x = []
    augmented_y = []


    for image, mask in zip(x_train, y_train):
        augmented_x.append(image)
        augmented_y.append(mask)

        aug_image, aug_mask = augment(image, mask)
        augmented_x.append(aug_image)
        augmented_y.append(aug_mask)

    # Convert to numpy arrays
    augmented_x = np.array(augmented_x)
    augmented_y = np.array(augmented_y)

    return augmented_x, augmented_y

# Usage
# augmented_x_train, augmented_y_train = augment_dataset(x_train, y_train)

x.shape, y.shape

# del TRAIN_XX

# del TRAIN_YY

# del all_train

# del all_mask

"""## UNET MODEL"""

import tensorflow as tf
import matplotlib.pyplot as plt

# Custom Metrics
from tensorflow.keras import backend as K

def recall_m(y_true, y_pred):


    y_true = tf.cast(y_true, tf.float64)
    y_pred = tf.cast(y_pred, tf.float64)
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def precision_m(y_true, y_pred):
    y_true = tf.cast(y_true, tf.float64)
    y_pred = tf.cast(y_pred, tf.float64)
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def f1_m(y_true, y_pred):
    y_true = tf.cast(y_true, tf.float64)
    y_pred = tf.cast(y_pred, tf.float64)
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2 * ((precision * recall) / (precision + recall + K.epsilon()))

# Define UNet Model
def unet_model(IMG_WIDTH, IMG_HEIGHT, IMG_CHANNELS):
    inputs = tf.keras.layers.Input((IMG_WIDTH, IMG_HEIGHT, IMG_CHANNELS))

    # Contracting Path
    c1 = tf.keras.layers.Conv2D(16, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(inputs)
    c1 = tf.keras.layers.Dropout(0.1)(c1)
    c1 = tf.keras.layers.Conv2D(16, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c1)
    p1 = tf.keras.layers.MaxPooling2D((2, 2))(c1)

    c2 = tf.keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p1)
    c2 = tf.keras.layers.Dropout(0.1)(c2)
    c2 = tf.keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c2)
    p2 = tf.keras.layers.MaxPooling2D((2, 2))(c2)

    c3 = tf.keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p2)
    c3 = tf.keras.layers.Dropout(0.2)(c3)
    c3 = tf.keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c3)
    p3 = tf.keras.layers.MaxPooling2D((2, 2))(c3)

    c4 = tf.keras.layers.Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p3)
    c4 = tf.keras.layers.Dropout(0.2)(c4)
    c4 = tf.keras.layers.Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c4)
    p4 = tf.keras.layers.MaxPooling2D(pool_size=(2, 2))(c4)

    c5 = tf.keras.layers.Conv2D(256, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p4)
    c5 = tf.keras.layers.Dropout(0.3)(c5)
    c5 = tf.keras.layers.Conv2D(256, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c5)

    # Expanding Path
    u6 = tf.keras.layers.Conv2DTranspose(128, (2, 2), strides=(2, 2), padding='same')(c5)
    u6 = tf.keras.layers.concatenate([u6, c4])
    c6 = tf.keras.layers.Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u6)
    c6 = tf.keras.layers.Dropout(0.2)(c6)
    c6 = tf.keras.layers.Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c6)

    u7 = tf.keras.layers.Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same')(c6)
    u7 = tf.keras.layers.concatenate([u7, c3])
    c7 = tf.keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u7)
    c7 = tf.keras.layers.Dropout(0.2)(c7)
    c7 = tf.keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c7)

    u8 = tf.keras.layers.Conv2DTranspose(32, (2, 2), strides=(2, 2), padding='same')(c7)
    u8 = tf.keras.layers.concatenate([u8, c2])
    c8 = tf.keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u8)
    c8 = tf.keras.layers.Dropout(0.1)(c8)
    c8 = tf.keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c8)

    u9 = tf.keras.layers.Conv2DTranspose(16, (2, 2), strides=(2, 2), padding='same')(c8)
    u9 = tf.keras.layers.concatenate([u9, c1])
    c9 = tf.keras.layers.Conv2D(16, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u9)
    c9 = tf.keras.layers.Dropout(0.1)(c9)
    c9 = tf.keras.layers.Conv2D(16, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c9)

    outputs = tf.keras.layers.Conv2D(1, (1, 1), activation='sigmoid')(c9)

    model = tf.keras.Model(inputs=[inputs], outputs=[outputs])

    return model

def scheduler(epoch, lr):
    if epoch < 2:
        return lr
    else:
        return lr *0.25

from sklearn.model_selection import KFold


k = 5  # Number of folds
epochs = 60
batch_size = 32

kf = KFold(n_splits=k, shuffle=True, random_state=42)

fold_results = []

for fold, (train_idx, val_idx) in enumerate(kf.split(x)):
    print(f"Training on fold {fold + 1}/{k}...")

    # Split data
    x_train_fold, x_val_fold = x[train_idx], x[val_idx]
    y_train_fold, y_val_fold = y[train_idx], y[val_idx]

    base_model = Unet(backbone_name="inceptionv3", encoder_weights=None)
    inp = Input(shape=(None, None, x.shape[-1]))
    l1 = Conv2D(3, (1, 1))(inp)  # Convert N channels to 3 channels
    out = base_model(l1)
    model = Model(inp, out, name=base_model.name)

    # Compile model
    model.compile(optimizer=tf.keras.optimizers.AdamW(learning_rate=1e-3),
                  loss="binary_crossentropy",
                  metrics=['accuracy', f1_m, precision_m, recall_m])

    earlyStopping = tf.keras.callbacks.EarlyStopping(
    monitor="val_f1_m", patience=5, verbose=1, mode="max")

    callbacks = [earlyStopping]

    # Train model on the current fold
    history = model.fit(x_train_fold, y_train_fold,
                        validation_data=(x_val_fold, y_val_fold),
                        epochs=epochs,
                        batch_size=batch_size,
                        verbose=1, callbacks=callbacks)

    # Save validation results
    fold_results.append(history.history['val_f1_m'][-1])

# Print average accuracy
print(f"Average Validation Accuracy: {np.mean(fold_results):.4f} ± {np.std(fold_results):.4f}")

"""RGB"""

x = TRAIN_XX[:,:,:,0:3]
y = TRAIN_YY

k = 5  # Number of folds
epochs = 60
batch_size = 32

kf = KFold(n_splits=k, shuffle=True, random_state=42)

fold_results = []

for fold, (train_idx, val_idx) in enumerate(kf.split(x)):
    print(f"Training on fold {fold + 1}/{k}...")

    # Split data
    x_train_fold, x_val_fold = x[train_idx], x[val_idx]
    y_train_fold, y_val_fold = y[train_idx], y[val_idx]

    base_model = Unet(backbone_name="inceptionv3", encoder_weights=None)
    inp = Input(shape=(None, None, x.shape[-1]))
    l1 = Conv2D(3, (1, 1))(inp)  # Convert N channels to 3 channels
    out = base_model(l1)
    model = Model(inp, out, name=base_model.name)

    # Compile model
    model.compile(optimizer=tf.keras.optimizers.AdamW(learning_rate=1e-3),
                  loss="binary_crossentropy",
                  metrics=['accuracy', f1_m, precision_m, recall_m])

    earlyStopping = tf.keras.callbacks.EarlyStopping(
    monitor="val_f1_m", patience=5, verbose=1, mode="max")

    callbacks = [earlyStopping]

    # Train model on the current fold
    history = model.fit(x_train_fold, y_train_fold,
                        validation_data=(x_val_fold, y_val_fold),
                        epochs=epochs,
                        batch_size=batch_size,
                        verbose=1, callbacks=callbacks)

    # Save validation results
    fold_results.append(history.history['val_f1_m'][-1])

# Print average accuracy
print(f"Average Validation Accuracy: {np.mean(fold_results):.4f} ± {np.std(fold_results):.4f}")

"""6 Channels"""

IMG_WIDTH, IMG_HEIGHT, IMG_CHANNELS = 128, 128, 6

x = TRAIN_XX[:, :, :, [0, 1, 2, 8, 9, 10]]
y = TRAIN_YY

x, y = augment_dataset(x, y)

k = 5  # Number of folds
epochs = 60
batch_size = 32

kf = KFold(n_splits=k, shuffle=True, random_state=42)

fold_results = []

for fold, (train_idx, val_idx) in enumerate(kf.split(x)):
    print(f"Training on fold {fold + 1}/{k}...")

    # Split data
    x_train_fold, x_val_fold = x[train_idx], x[val_idx]
    y_train_fold, y_val_fold = y[train_idx], y[val_idx]

    model = unet_model(IMG_WIDTH, IMG_HEIGHT, IMG_CHANNELS)

    # Compile model
    model.compile(optimizer=tf.keras.optimizers.AdamW(learning_rate=1e-3),
                  loss="binary_crossentropy",
                  metrics=['accuracy', f1_m, precision_m, recall_m])

    earlyStopping = tf.keras.callbacks.EarlyStopping(
    monitor="val_f1_m", patience=5, verbose=1, mode="max")

    callbacks = [earlyStopping]

    # Train model on the current fold
    history = model.fit(x_train_fold, y_train_fold,
                        validation_data=(x_val_fold, y_val_fold),
                        epochs=epochs,
                        batch_size=batch_size,
                        verbose=1, callbacks=callbacks)

    # Save validation results
    fold_results.append(history.history['val_f1_m'][-1])

# Print average accuracy
print(f"Average Validation Accuracy: {np.mean(fold_results):.4f} ± {np.std(fold_results):.4f}")


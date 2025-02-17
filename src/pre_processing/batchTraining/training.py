import tensorflow as tf
import os
from tensorflow.keras import layers, models
import tensorflow_io as tfio
EPOCHS =5

import tensorflow as tf
import os

# Define paths to image and label folders
image_dir = "../../../data/png/img"
label_dir = "../../../data/png/label"

# Get sorted file paths
image_paths = sorted([os.path.join(image_dir, fname) for fname in os.listdir(image_dir)])
label_paths = sorted([os.path.join(label_dir, fname) for fname in os.listdir(label_dir)])

# Function to load and preprocess images
def load_image(image_path, label_path):
    image = tf.io.read_file(image_path)
    image = tf.image.decode_png(image, channels=3)  # Change to 1 for grayscale
    image = tf.image.resize(image, (256, 256))  # Resize to match your model input
    image = tf.cast(image, tf.float32) / 255.0  # Normalize

    label = tf.io.read_file(label_path)
    label = tf.image.decode_png(label, channels=1)  # Change channels based on label format
    label = tf.image.resize(label, (256, 256), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
    label = tf.cast(label, tf.uint8)  # Keep as uint8 for categorical labels

    return image, label

# Create a dataset from file paths
dataset = tf.data.Dataset.from_tensor_slices((image_paths, label_paths))
dataset = dataset.map(load_image, num_parallel_calls=tf.data.AUTOTUNE)
dataset = dataset.shuffle(buffer_size=1000)  # Adjust buffer size
dataset = dataset.batch(64)  # Adjust batch size based on GPU memory
dataset = dataset.prefetch(tf.data.AUTOTUNE)  # Optimize performance

# Split into training and validation
train_size = int(0.8 * len(image_paths))
train_dataset = dataset.take(train_size)
val_dataset = dataset.skip(train_size)


# -----------------------
# U-Net Inspired Model
# -----------------------
def build_unet(input_shape=(256, 256, 3)):
    inputs = layers.Input(input_shape)

    # Encoder
    conv1 = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(inputs)
    conv1 = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(conv1)
    pool1 = layers.MaxPooling2D((2, 2))(conv1)

    conv2 = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(pool1)
    conv2 = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(conv2)
    pool2 = layers.MaxPooling2D((2, 2))(conv2)

    # Bottleneck
    conv3 = layers.Conv2D(256, (3, 3), activation='relu', padding='same')(pool2)
    conv3 = layers.Conv2D(256, (3, 3), activation='relu', padding='same')(conv3)

    # Decoder
    up1 = layers.UpSampling2D((2, 2))(conv3)
    up1 = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(up1)
    up1 = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(up1)
    
    up2 = layers.UpSampling2D((2, 2))(up1)
    up2 = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(up2)
    up2 = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(up2)

    # Output layer (Sigmoid for binary segmentation)
    outputs = layers.Conv2D(1, (1, 1), activation='sigmoid', padding='same')(up2)

    model = models.Model(inputs, outputs)
    return model

# -----------------------
# COMPILE MODEL
# -----------------------
model = build_unet()
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train model with dataset
history = model.fit(dataset, epochs=EPOCHS)

# Save the trained model
model.save("segmentation_model.h5")
print("Model saved successfully! 🎉")


""" Runs inference on a list of images from saved_model and scales the bounding boxes """

from PIL.ImageQt import ImageQt, toqpixmap
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QBuffer, QPointF, QRegExp, QCoreApplication
from PyQt5.QtGui import QIntValidator, QImage, QPixmap, QRegExpValidator
from PyQt5.QtWidgets import QSizePolicy, QLineEdit, QComboBox, QInputDialog, QMessageBox, QDialog, QProgressDialog

import sys
import os
import math
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from typing import Callable
from object_detection.utils import visualization_utils as viz_utils
from functools import reduce


def scale_box_dims(box_dims: np.ndarray, full_size: tuple, stride: int,
                   crop_size: tuple, index: tuple) -> np.ndarray:
    ''' Scale coordinates for a single box from crop to original image '''
    (full_width, full_height) = full_size
    (crop_width, crop_height) = crop_size
    (y_index, x_index) = index
    return np.array([
        # y_min
        scale_single_dim(box_dims[0], full_height, crop_height, stride,
                    y_index),  
        # x_min
        scale_single_dim(box_dims[1], full_width, crop_width, stride,
                    x_index), 
        # y_max
        scale_single_dim(box_dims[2], full_height, crop_height, stride,
                    y_index),
         # x_max
        scale_single_dim(box_dims[3], full_width, crop_width, stride,
                    x_index) 
    ])


def scale_single_dim(pos: int, full: int, crop: int, stride: int,
                index: int) -> float:
    ''' Scale single dimension in a bounding box '''
    scale = crop / float(full)
    offset = (index * stride / float(full))
    return pos * scale + offset


def find_scaled_boxes_from_crop(crop_image: Image, index: tuple,
                                full_img_dims: tuple, stride: int,
                                detect_fn: Callable,
                                score_threshold: float) -> tuple:
    ''' Runs inference on a single image crop, returns detections dictionary with scaled boxes '''

    # Get dimensions of crop for scaling
    crop_width, crop_height = crop_image.size
    full_width = full_img_dims[0]
    full_height = full_img_dims[1]

    # Convert image to tensor with the correct shape
    crop_image_np = np.array(crop_image)
    crop_image_tensor = tf.convert_to_tensor(crop_image_np)
    input_tensor = tf.convert_to_tensor(np.expand_dims(crop_image_np, 0),
                                        dtype=tf.uint8)

    # Run inference
    detections = detect_fn(input_tensor)

    # Remove batch dimension and find number of detections
    num_detections = int(detections.pop('num_detections'))
    detections = {
        key: value[0, :num_detections].numpy()
        for key, value in detections.items()
    }
    detections['num_detections'] = num_detections

    # Convert detection classes to ints
    detections['detection_classes'] = detections['detection_classes'].astype(
        np.int64)

    # Discard low-scoring boxes
    indices_to_gather = [
        index for index, val in enumerate(detections['detection_scores'])
        if val >= score_threshold
    ]

    # tf.gather() will throw an exception for an empty indices tensor,
    # so return what we have and flag it in this instance
    if len(indices_to_gather) < 1:
        return detections, False

    detections['detection_scores'] = tf.gather(
        detections['detection_scores'],
        tf.convert_to_tensor(indices_to_gather))
    detections['detection_boxes'] = tf.gather(detections['detection_boxes'],
                                              indices_to_gather)
    detections['detection_classes'] = tf.gather(
        detections['detection_classes'], indices_to_gather)

    # Scale detection boxes
    detections['detection_boxes'] = np.array([
        scale_box_dims(box_dims, full_img_dims, stride,
                       (crop_width, crop_height), index)
        for box_dims in detections['detection_boxes']
    ])

    return detections, True


def detect_and_combine(detect_fn: Callable, image_cuts: list,
                       full_img_size: tuple, stride: int,
                       score_threshold: float,
                       iou_threshold: float, 
                       progress_dialog: QProgressDialog) -> dict:
    ''' Run detections on all image cuts, combine the results into a single dict '''
    # This can be hardcoded, since we are only concerned with a single class
    category_index = {0: 1}

    # Open progress dialogue
    # progress = QProgressDialog("Detecting headstones...", None, 0, 100)
    # progress.setWindowModality(Qt.WindowModal)
    # progress.setAutoClose(True)
    # progress.setMinimumDuration(1000)
    # progress.setValue(0)
    
    # Dialog isn't appearing without this
    QCoreApplication.processEvents()

    # Perform detections
    full_detections = []
    rows = len(image_cuts)
    cols = len(image_cuts[0])
    for i, row in enumerate(image_cuts):
        for j, col in enumerate(row):
            # Dialog isn't appearing without this
            QCoreApplication.processEvents()
            pr_p = math.floor((((i) * cols + (j+1)) / (rows * cols)) * 100)
            progress_dialog.setValue(pr_p)
            if progress_dialog.wasCanceled():
                break
            print(f'Running on cut [{i}][{j}]...')
            d, flag = find_scaled_boxes_from_crop(image_cuts[i][j], (i, j),
                                                  full_img_size, stride,
                                                  detect_fn, score_threshold)
            if flag:
                full_detections.append(d)

    # progress.setValue(100)
    del progress_dialog

    # Fold detections
    final_detections = reduce(fold_detections, full_detections)

    # Apply non max supression for overlapping boxes
    pruned_detections = non_maximum_supression(final_detections, iou_threshold)

    return pruned_detections


def fold_detections(d1: dict, d2: dict) -> dict:
    ''' Used to reduce detections from all image cuts '''
    boxes = np.concatenate((d1['detection_boxes'], d2['detection_boxes']))
    scores = np.concatenate((d1['detection_scores'], d2['detection_scores']))
    classes = np.concatenate(
        (d1['detection_classes'], d2['detection_classes']))
    return {
        'detection_boxes': boxes,
        'detection_scores': scores,
        'detection_classes': classes
    }


def non_maximum_supression(detections: dict, threshold: float) -> dict:
    ''' Prunes overlapping boxes with TensorFlow's non max supression algorithm '''
    selected_indices = tf.image.non_max_suppression(
        detections['detection_boxes'],
        detections['detection_scores'],
        max_output_size=50000,
        iou_threshold=threshold)
    detections['detection_boxes'] = tf.gather(detections['detection_boxes'],
                                              selected_indices).numpy()
    detections['detection_classes'] = tf.gather(
        detections['detection_classes'], selected_indices).numpy()
    detections['detection_scores'] = tf.gather(detections['detection_scores'],
                                               selected_indices).numpy()

    return detections


def visualize_boxes_on_full_image(image: Image, detections: dict) -> None:
    ''' For testing '''

    print('Visualizing...')

    # Load full image into np array
    image_np = np.array(image)

    # Display bounding boxes
    image_np_with_detections = image_np.copy()
    viz_utils.visualize_boxes_and_labels_on_image_array(
        image_np_with_detections,
        detections['detection_boxes'],
        detections['detection_classes'],
        detections['detection_scores'],
        {0: 1
         },  # Hardcoded category_index, since we are concerned with 1 class
        use_normalized_coordinates=True,
        max_boxes_to_draw=50000,
        min_score_thresh=.35,
        skip_labels=True,
        skip_scores=True,
        agnostic_mode=False)
    plt.figure()
    plt.imshow(image_np_with_detections)
    plt.savefig('full_inference.jpg')
    print('Done! File saved.')


def main():
    ''' For testing, run inference on a single provided image '''
    score_threshold = 0.30

    # Open image
    print(f'Opening {sys.argv[1]} ...')
    image_path = sys.argv[1]
    image = Image.open(image_path)

    # Load labels
    category_index = {0: 1}

    # Load model
    print(f'Loading model from {sys.argv[2]} ...')
    saved_model_path = sys.argv[2] + '/saved_model'
    detect_fn = tf.saved_model.load(saved_model_path)

    print('Running inference...')
    find_scaled_boxes_from_crop(
        image,  # PIL image
        (0, 3),  # 2-dimensional index of this crop
        (2023, 1218),  # Size of full, uncropped image
        300,  # Stride 
        detect_fn,  # TensorFlow inference function
        score_threshold,  # Threshold to cull boxes
    )


if __name__ == '__main__':
    # For testing
    main()

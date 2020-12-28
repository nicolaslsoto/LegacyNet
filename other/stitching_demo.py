''' Demonstrates image cutting, inference, and stitching

    Usage: stitching_demo.py [PATH_TO_IMAGE] [PATH_TO_SAVED_MODEL_DIRECTORY]

    Key steps:
        - Load model and get detection function with tf.saved_model(PATH_TO_SAVED_MODEL)
        - Get image cuts with image_cut.crop_image_with_padding(CROP_IMG_SIZE, STRIDE, IMAGE)
        - Get detections with inference.detect_and_combine(DETECT_FN, IMAGE_CUTS, FULL_IMG_SIZE,
                                                           STRIDE, SCORE_THRESHOLD)
        - The bounding box coordinates can then be accessed as detections['detection_boxes']
          as [y_min, x_min, y_max, x_max] as floats between 0.0 and 1.0 


'''

from ml import inference, image_cut
import sys
import tensorflow as tf
from PIL import Image


def main():
    # Load the image
    print(f'Loading image from {sys.argv[1]}...')
    image_path = sys.argv[1]
    image = Image.open(image_path)
    full_width, full_height = image.size

    # Make the crops
    image_cuts = image_cut.crop_image_with_padding((320, 320), 300, image)

    # Load model
    print(f'Loading model from {sys.argv[2]}...')
    saved_model_path = sys.argv[2] + '/saved_model'
    detect_fn = tf.saved_model.load(saved_model_path)

    # Run model on image crops
    print(f'Running inferences...')
    detections = inference.detect_and_combine(detect_fn, image_cuts,
                                              (full_width, full_height), 300,
                                              0.35)

    print(detections)

    # Visualize detections
    inference.visualize_boxes_on_full_image(image, detections)


if __name__ == '__main__':
    main()

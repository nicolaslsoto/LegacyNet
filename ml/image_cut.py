""" Cuts input image with padding and stride """

import os
import sys
from PIL import Image


def single_crop(image: Image, top: int, left: int, right: int,
                bottom: int) -> Image:
    """ Crops a single image given a bounding box, with padding if necessary """
    width, height = image.size
    if bottom > height or right > width:
        # If the crop extends beyond the image boundaries,
        # create a padded image by pasting onto a new blank image
        cropped_image = Image.new("RGB", ((right - left), (bottom - top)))
        bottom = min(bottom, height)
        right = min(right, width)
        temp_crop = image.crop((left, top, right, bottom))
        cropped_image.paste(temp_crop)
    else:
        cropped_image = image.crop((left, top, right, bottom))

    return cropped_image


def crop_image_with_padding(desired_size: tuple, stride: int,
                            image: Image) -> list:
    """ Returns 2D list of PIL images, cropped, with stride, adding padding as necessary """
    image_list = []

    # Non-RGB modes may not save as JPG, which our model requires
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Get image dimensions
    width, height = image.size

    # Initialize cropping coordinates
    i       = 0
    top     = 0
    left    = 0
    right   = desired_size[0]
    bottom  = desired_size[1]

    # Make crops
    while top < height:
        row = []
        while left < width:
            i += 1
            cropped_image = single_crop(image, top, left, right, bottom)
            row.append(cropped_image)
            right += stride
            left  += stride
        image_list.append(row)
        left    = 0
        right   = desired_size[0]
        top     += stride
        bottom  += stride

    return image_list


if __name__ == '__main__':
    # For testing
    print('Processing images...')
    images = crop_image_with_padding((320, 320), 300, Image.open(sys.argv[1]))
    print('Done! Saving...')
    for row, image in enumerate(images):
        for col, image in enumerate(images[row]):
            image.save(f'crop-{row}-{col}.jpg')
    print('Done!')
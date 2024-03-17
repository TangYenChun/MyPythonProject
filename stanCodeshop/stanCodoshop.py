"""
File: stanCodoshop.py
Name: Bella
----------------------------------------------
SC101_Assignment3 Adapted from Nick Parlante's
Ghost assignment by Jerry Liao.
"""

import os
import sys
import math
from simpleimage import SimpleImage


def get_pixel_dist(pixel, red, green, blue):
    """
    Returns a value that refers to the "color distance" between a pixel and a mean RGB value.

    Input:
        pixel (Pixel): the pixel with RGB values to be compared
        red (int): the average red value of the pixels to be compared
        green (int): the average green value of the pixels to be compared
        blue (int): the average blue value of the pixels to be compared

    Returns:
        dist (float): the "color distance" of a pixel to the average RGB value of the pixels to be compared.
    """
    return math.sqrt((red - pixel.red)**2 + (green - pixel.green)**2 + (blue - pixel.blue)**2)


def get_average(pixels):
    """
    Given a list of pixels, finds their average red, blue, and green values.

    Input:
        pixels (List[Pixel]): a list of pixels to be averaged

    Returns:
        rgb (List[int]): a list of average red, green, and blue values of the pixels
                        (returns in order: [red, green, blue])
    """
    # Get total red, green, and blue values of all pixels.
    red_avg = sum(pixel.red for pixel in pixels)
    green_avg = sum(pixel.green for pixel in pixels)
    blue_avg = sum(pixel.blue for pixel in pixels)

    # Calculate average red, green, and blue values.
    return [int(red_avg / len(pixels)), int(green_avg / len(pixels)), int(blue_avg / len(pixels))]


def get_best_pixel(pixels):
    """
    Given a list of pixels, returns the pixel with the smallest "color distance", which has the closest color to the average.

    Input:
        pixels (List[Pixel]): a list of pixels to be compared
    Returns:
        best (Pixel): the pixel which has the closest color to the average
    """
    avg = get_average(pixels)
    # This dictionary used to store the color distance of every pixel.
    # key: pixel, value: color_distance
    distance_pixel_set = set()
    for pixel in pixels:
        # Get the color distance of the pixel.
        color_distance = get_pixel_dist(pixel, avg[0], avg[1], avg[2])
        # Add a color distance and pixel into the dictionary.
        distance_pixel_set.add((pixel, color_distance))

    # Get the minimum color distance.
    # Return the pixel which has the closest color to the average.
    return min(distance_pixel_set, key=lambda ele: ele[1])[0]


def solve(images):
    """
    Given a list of image objects, compute and display a Ghost solution image
    based on these images. There will be at least 3 images and they will all
    be the same size.

    Input:
        images (List[SimpleImage]): list of images to be processed
    """
    width = images[0].width
    height = images[0].height
    result = SimpleImage.blank(width, height)

    for i in range(width):
        for j in range(height):
            # This list used to store the pixels at the (i, j) position of all images.
            pixels = []
            for image in images:
                pixels.append(image.get_pixel(i, j))
            # Get the best pixel.
            best_pixel = get_best_pixel(pixels)
            # Set the red, green, and blue values of pixel at the (i, j) position of the result image.
            result.set_rgb(i, j, best_pixel.red, best_pixel.green, best_pixel.blue)

    print("Displaying image!")
    result.show()


def jpgs_in_dir(dir):
    """
    (provided, DO NOT MODIFY)
    Given the name of a directory, returns a list of the .jpg filenames
    within it.

    Input:
        dir (string): name of directory
    Returns:
        filenames(List[string]): names of jpg files in directory
    """
    filenames = []
    for filename in os.listdir(dir):
        if filename.endswith('.jpg'):
            filenames.append(os.path.join(dir, filename))
    return filenames


def load_images(dir):
    """
    (provided, DO NOT MODIFY)
    Given a directory name, reads all the .jpg files within it into memory and
    returns them in a list. Prints the filenames out as it goes.

    Input:
        dir (string): name of directory
    Returns:
        images (List[SimpleImages]): list of images in directory
    """
    images = []
    jpgs = jpgs_in_dir(dir)
    for filename in jpgs:
        print("Loading", filename)
        image = SimpleImage(filename)
        images.append(image)
    return images


def main():
    # (provided, DO NOT MODIFY)
    args = sys.argv[1:]
    # We just take 1 argument, the folder containing all the images.
    # The load_images() capability is provided above.
    images = load_images(args[0])
    solve(images)


if __name__ == '__main__':
    main()

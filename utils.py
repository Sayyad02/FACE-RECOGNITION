# utils.py
import cv2
import os
import numpy as np

def load_image(image_path):
    """Loads an image from the given path. Handles file not found errors."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    image = cv2.imread(image_path)
    if image is None:  # Check if image was actually loaded
        raise ValueError(f"Could not open or read image: {image_path}")
    return image


def display_image(image, title="Image"):
    """Displays an image in a window."""
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def convert_bgr_to_rgb(image):
    """Converts an image from BGR (OpenCV) to RGB (face_recognition)."""
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def resize_frame(frame, scale_factor):
    """Resizes a frame by the specified scale factor."""
    return cv2.resize(frame, (0, 0), fx=scale_factor, fy=scale_factor)
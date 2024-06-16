import os

from typing import Union

import cv2 as cv
import numpy as np
import chart_cpp

''' chr(0x0020): space
    chr(0x2591): 1/4 block
    chr(0x2592): 1/2 block
    chr(0x2593): 3/4 block
    chr(0x2588): full block
'''
CHAR_PIXEL = [chr(0x0020), chr(0x2591), chr(0x2592), chr(0x2593), chr(0x2588)]

def displayGrayPicture(img_path: Union[str, np.ndarray],
                       win_output: bool = False,
                       invert: bool = False,
                       ) -> None:
    if isinstance(img_path, str) and not os.path.exists(img_path):
        raise FileNotFoundError
    if not isinstance(img_path, (str, np.ndarray)) or not isinstance(win_output, bool):
        raise TypeError

    if isinstance(img_path, str):
        img = cv.imread(img_path, cv.IMREAD_GRAYSCALE)
    else:
        img = img_path

    if win_output:
        chart_cpp.grayConvert(img, 63.75)

        cv.imshow("output", img)
        cv.waitKey(0)
        cv.destroyAllWindows()
    else:
        img = cv.resize(img, (img.shape[1], int(img.shape[0] / 2)))
        if invert:
            chart_cpp.print_char_art(img, CHAR_PIXEL)
        else:
            chart_cpp.print_char_art(img, CHAR_PIXEL[::-1])

def displayColorPicture(img_path: Union[str, np.ndarray]):
    if isinstance(img_path, str) and not os.path.exists(img_path):
        raise FileNotFoundError
    if not isinstance(img_path, (str, np.ndarray)):
        raise TypeError

    if isinstance(img_path, str):
        img = cv.imread(img_path)
    else:
        img = img_path

    for i in range(3):
        chart_cpp.grayConvert(img[:,:,i], 63.75)

    cv.imshow("output", img)
    cv.waitKey(0)
    cv.destroyAllWindows()

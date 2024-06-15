import os

from typing import Union, Optional, Callable

import cv2 as cv
import numpy as np

''' chr(0x0020): space
    chr(0x2591): 1/4 block
    chr(0x2592): 1/2 block
    chr(0x2593): 3/4 block
    chr(0x2588): full block
'''
CHAR_PIXEL = [chr(0x0020), chr(0x2591), chr(0x2592), chr(0x2593), chr(0x2588)]

def grayConvert(img: np.ndarray, multiple: Union[int, float] = 1, callback: Optional[Callable] = None):
    if not isinstance(img, np.ndarray) or not isinstance(img[0, 0], np.uint8) or not isinstance(multiple, (int, float)):
        raise TypeError

    h, w = img.shape
    for y in range(h):
        for x in range(w):
            pixel = img[y, x]
            if pixel < 32: # 255 / 8
                img[y, x] = 0
            elif pixel < 96: # 255 / 8 * 3
                img[y, x] = 1 * multiple
            elif pixel < 160:
                img[y, x] = 2 * multiple
            elif pixel < 224:
                img[y, x] = 3 * multiple
            else:
                img[y, x] = 4 * multiple
            if callback is not None:
                callback(x, y, img[y, x])

def displayGrayPicture(img_path: Union[str, np.ndarray],
                       win_output: bool = False,
                       invert: bool = False,
                       ) -> Optional[np.ndarray]:
    if isinstance(img_path, str) and not os.path.exists(img_path):
        raise FileNotFoundError
    if not isinstance(img_path, (str, np.ndarray)) or not isinstance(win_output, bool):
        raise TypeError

    if isinstance(img_path, str):
        img = cv.imread(img_path, cv.IMREAD_GRAYSCALE)
    else:
        img = img_path

    if win_output:
        grayConvert(img, 63.75)

        cv.imshow("output", img)
        cv.waitKey(0)
        cv.destroyAllWindows()
    else:
        cache: str = ""
        img = cv.resize(img, (img.shape[1], int(img.shape[0] / 2)))

        def callback(x: int, y: int, pixel: int):
            nonlocal cache
            if x == 0:
                cache += "\n"
            if invert:
                cache += CHAR_PIXEL[img[y, x]]
            else:
                cache += CHAR_PIXEL[len(CHAR_PIXEL) - 1 - img[y, x]]
        grayConvert(img, callback=callback)
        print(cache)

def displayColorPicture(img_path: Union[str, np.ndarray], win_output: bool = False):
    if isinstance(img_path, str) and not os.path.exists(img_path):
        raise FileNotFoundError
    if not isinstance(img_path, (str, np.ndarray)):
        raise TypeError

    if isinstance(img_path, str):
        img = cv.imread(img_path)
    else:
        img = img_path

    #

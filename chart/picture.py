import os

from typing import Union, Optional

import cv2 as cv
import numpy as np

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
        if not isinstance(img_path[0, 0], np.uint8):
            raise TypeError
        img = img_path

    ''' chr(0x0020): space
        chr(0x2591): 1/4 block
        chr(0x2592): 1/2 block
        chr(0x2593): 3/4 block
        chr(0x2588): full block
    '''
    CHAR_PIXEL = [chr(0x0020), chr(0x2591), chr(0x2592), chr(0x2593), chr(0x2588)]
    img = cv.resize(img, (img.shape[1], int(img.shape[0] / 2)))
    h, w = img.shape

    for y in range(h):
        for x in range(w):
            pixel = img[y, x]
            if pixel < 32: # 255 / 8
                img[y, x] = 0
            elif pixel < 96: # 255 / 8 * 3
                img[y, x] = 1
            elif pixel < 160:
                img[y, x] = 2
            elif pixel < 224:
                img[y, x] = 3
            else:
                img[y, x] = 4

    if win_output:
        for y in range(h):
            for x in range(w):
                img[y, x] = int(img[y, x] * 63.75)

        cv.imshow("output", img)
        cv.waitKey(0)
        cv.destroyAllWindows()
    else:
        for y in range(h):
            for x in range(w):
                if invert:
                    print(CHAR_PIXEL[img[y, x]], end='')
                else:
                    print(CHAR_PIXEL[len(CHAR_PIXEL) - 1 - img[y, x]], end='')
            print()

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

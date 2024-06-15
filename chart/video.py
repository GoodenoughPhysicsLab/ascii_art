import os
import time
import platform

import cv2 as cv
import chart.picture as picture
import chart_cpp

from typing import Callable, Optional

def displayGrayVideo(video_path: str, win_output: bool = False, invert: bool = False, frame_callback: Optional[Callable] = None):
    if not isinstance(video_path, str) or not isinstance(win_output, bool):
        raise TypeError("video_path must be a string")
    if not os.path.exists(video_path):
        raise FileNotFoundError

    video = cv.VideoCapture(video_path)
    f, frame = video.read()

    if platform.system() == "Windows":
        CLEAR = "cls"
    else:
        CLEAR = "clear"

    try:
        if win_output:
            while f:
                f, frame = video.read()
                frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

                if frame_callback is not None:
                    frame_callback(frame)

                chart_cpp.grayConvert(frame, 63.75)
                cv.imshow("video", frame)
                if cv.waitKey(1) & 0xFF == ord('q'):
                    return
        else:
            f, frame = video.read()
            while f:
                frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

                if frame_callback is not None:
                    frame_callback(frame)

                frame = cv.resize(frame, (frame.shape[1], int(frame.shape[0] / 2)))

                os.system(CLEAR)
                if invert:
                    chart_cpp.print_char_art(frame, picture.CHAR_PIXEL)
                else:
                    chart_cpp.print_char_art(frame, picture.CHAR_PIXEL[::-1])
                time.sleep(0.04)

                f, frame = video.read()
    except KeyboardInterrupt:
        video.release()
        cv.destroyAllWindows()

def displayColorVideo(video_path: str, win_output: bool = False):
    pass
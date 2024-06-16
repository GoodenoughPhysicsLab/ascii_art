import os
import time
import platform

import cv2 as cv
import chart.picture as picture
import chart_cpp

from typing import Callable, Optional, Union

def displayGrayVideo(video_path: Union[str, cv.VideoCapture],
                     win_output: bool = False,
                     invert: bool = False,
                     frame_callback: Optional[Callable] = None,
                     ) -> None:
    if not isinstance(video_path, (str, cv.VideoCapture)) or not isinstance(win_output, bool):
        raise TypeError("video_path must be a string")
    if not os.path.exists(video_path):
        raise FileNotFoundError

    if isinstance(video_path, str):
        video = cv.VideoCapture(video_path)
    elif isinstance(video_path, cv.VideoCapture):
        video = video_path

    if not video.isOpened():
        raise IOError

    f, frame = video.read()
    sleep_time = 1 / video.get(cv.CAP_PROP_FPS) - 0.008

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
                time.sleep(sleep_time)
        else:
            f, frame = video.read()
            while f:
                frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

                if frame_callback is not None:
                    frame_callback(frame)

                picture.displayGrayPicture(frame, False, invert, True)
                time.sleep(0.04)

                f, frame = video.read()
    except KeyboardInterrupt:
        video.release()
        cv.destroyAllWindows()

def displayColorVideo(video_path: Union[str, cv.VideoCapture]):
    if not isinstance(video_path, (str, cv.VideoCapture)):
        raise TypeError
    if isinstance(video_path, str) and not os.path.exists(video_path):
        raise FileNotFoundError

    if isinstance(video_path, str):
        video = cv.VideoCapture(video_path)
    elif isinstance(video_path, cv.VideoCapture):
        video = video_path

    f, frame = video.read()
    sleep_time = 1 / video.get(cv.CAP_PROP_FPS) - 0.008
    while f:
        for i in range(3):
            chart_cpp.grayConvert(frame[:,:,i], 63.75)

        cv.imshow("video", frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        f, frame = video.read()
        time.sleep(sleep_time)
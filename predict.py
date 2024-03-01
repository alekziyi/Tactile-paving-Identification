# ----------------------------------------------------#
#   将单张图片预测、摄像头检测和FPS测试功能
#   整合到了一个py文件中，通过指定mode进行模式的修改。
# ----------------------------------------------------#
import time

import cv2
import numpy as np

from deeplab import DeeplabV3

if __name__ == "__main__":
    deeplab = DeeplabV3(num_classes=2)
    mode = "video"
    video_path = 0

    fps=0.0
    if mode == "video":
        capture = cv2.VideoCapture(video_path)

        ref, frame = capture.read()
        if not ref:
            raise ValueError("未能正确读取摄像头（视频），请注意是否正确安装摄像头（是否正确填写视频路径）。")

        while (True):
            t1 = time.time()
            # 读取某一帧
            ref, frame = capture.read()
            if not ref:
                break
            # 格式转变，BGRtoRGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # 转变成Image
            #frame = Image.fromarray(np.uint8(frame))
            # 进行检测
            frame = deeplab.detect_image(frame)
            fps = (fps + (1. / (time.time() - t1))) / 2
            print("fps= %.2f" % (fps))
            frame = np.array(frame, np.uint8)
            cv2.imshow("video", frame)
            c = cv2.waitKey(1) & 0xff

            if c == 27:
                capture.release()
                break
        cv2.destroyAllWindows()

    else:
        raise AssertionError("Please specify the correct mode: 'video'.")

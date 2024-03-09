import time
import pygame
import pygame.camera
import numpy as np
import cv2
from deeplab import DeeplabV3
import threading

img_cache=np.zeros((480,640,3),dtype=np.uint8)

def model_process():
    deeplab = DeeplabV3(num_classes=2)
    while True:
        frame=img_cache
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = deeplab.detect_image(frame)
        binary = np.array(frame, np.uint8)
        cv2.imshow("binary", binary)
        cv2.waitKey(1)

def cap_process():
    pygame.init()
    gameDisplay = pygame.display.set_mode((640, 480))
    pygame.camera.init()
    print(pygame.camera.list_cameras())
    cam = pygame.camera.Camera("http://192.168.137.224:8081/")
    cam.start()
    global img_cache
    while True:
        img = cam.get_image()
        gameDisplay.blit(img, (0, 0))
        # 将 Pygame surface 转换为 NumPy 格式
        array3d = pygame.surfarray.array3d(img)
        numpy_array = np.swapaxes(array3d, 0, 1)

        img_cache = numpy_array
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cam.stop()
                pygame.quit()
                exit()

threading.Thread(target=model_process).start()
time.sleep(5)
cap_process()

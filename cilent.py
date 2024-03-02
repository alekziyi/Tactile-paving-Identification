import socket
import cv2
import numpy as np
import time
from threading import Thread

PACKAGE_SIZE=61440

class VideoReporter(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('192.168.137.1', 12000))
        self.cap = cv2.VideoCapture(1)
        self.num=0
        self.center=None
    def send(self,img: np.ndarray):
        for i in range(15):
            self.send_package(img.data[i*PACKAGE_SIZE:(i+1)*PACKAGE_SIZE])
    def send_package(self,data):
        self.client_socket.sendall(data)
        re=int.from_bytes(self.client_socket.recv(4), byteorder='little')
        while re != 1:
            self.client_socket.sendall(data)

    def receive(self):
        # self.center=eval(self.client_socket.recv(50).decode('utf-8'))
        # self.client_socket.send(b'1')
        pass
    def run(self):
        while True:
            ret,img=self.cap.read()
            if ret:
                self.send(img)
                self.receive()
            else:
                time.sleep(1)


if __name__=='__main__':
    video_reporter=VideoReporter()
    video_reporter.start()
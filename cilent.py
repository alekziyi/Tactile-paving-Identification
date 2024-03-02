import socket
import cv2
import numpy as np
import time
from threading import Thread

PACKAGE_SIZE=65000

class VideoReporter(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('localhost', 12000))
        self.cap = cv2.VideoCapture(0)
        self.num=0
        self.center=None
    def send(self,img: np.ndarray):
        n=img.size//PACKAGE_SIZE
        self.client_socket.send(n.to_bytes(4))
        self.client_socket.recv(1)
        for i in range(n):
            self.client_socket.send(img.data[i*PACKAGE_SIZE:(i+1)*PACKAGE_SIZE])
            self.client_socket.recv(1)
        self.client_socket.send(img.data[n * PACKAGE_SIZE:])
        self.client_socket.recv(1)
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
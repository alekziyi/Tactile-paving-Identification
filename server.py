import socket
import cv2
import numpy as np

from threading import Thread
from deeplab import DeeplabV3

PACKAGE_SIZE=61440

class VideoProcessor(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.deeplab = DeeplabV3(num_classes=2)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('192.168.137.1', 12000))
        self.sock.listen(1)
        self.client_socket, self.client_address = self.sock.accept()


    def receive_image(self):
        data=b''
        for i in range(15):
            print(i)
            data +=self.receive_package()
        img=np.frombuffer(data, dtype=np.uint8).reshape(480,640,3)
        return img
    def receive_package(self):
        data=self.client_socket.recv(PACKAGE_SIZE)
        while len(data)!=PACKAGE_SIZE:
            self.client_socket.sendall((0).to_bytes(4,byteorder='little'))
            data=self.client_socket.recv(PACKAGE_SIZE)
        self.client_socket.sendall((1).to_bytes(4,byteorder='little'))
        return data
    def image_processing(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        binary = self.deeplab.detect_image(img)
        binary = np.array(binary, np.uint8)
        return binary
    def get_img_center(self,binary):
        return (0,0)
    def send(self,center):
        #self.client_socket.sendall(f'{center}'.encode('utf-8'))
        # self.client_socket.recv(1)
        pass
    def run(self):
        while True:
            img=self.receive_image()
            cv2.imshow('img',img)
            cv2.waitKey(1)
            #print(img)
            binary=self.image_processing(img)
            cv2.imshow('binary',binary)
            cv2.waitKey(1)
            #print(binary)
            center=self.get_img_center(binary)
            self.send(center)


if __name__=='__main__':
    video_processor = VideoProcessor()
    video_processor.start()

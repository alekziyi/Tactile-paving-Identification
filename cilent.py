import cv2
import socket
import struct
import pickle


def send_image(addr,img):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 将图像转换为字符串
    img_str = pickle.dumps(img)

    # 设置分块大小
    chunk_size = 65000

    # 获取图像大小并发送
    img_size = struct.pack("!I", len(img_str))
    udp_socket.sendto(img_size, addr)

    # 分块发送图像数据
    for i in range(0, len(img_str), chunk_size):
        udp_socket.sendto(img_str[i:i + chunk_size], addr)
        #udp_socket.recvfrom(4)

    udp_socket.close()


if __name__ == "__main__":
    server_address = ("127.0.0.1", 7777)
    cap=cv2.VideoCapture(0)
    ret,img=cap.read()
    img=cv2.resize(img,(600,400))
    send_image(server_address, img)

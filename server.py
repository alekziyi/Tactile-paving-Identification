import cv2
import socket
import struct
import pickle


def receive_image(addr):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(addr)

    # 接收图像大小
    img_size, _ = udp_socket.recvfrom(4)
    img_size = struct.unpack("!I", img_size)[0]
    print(img_size)
    # 接收图像数据
    img_data = b""
    chunk_size = 65000
    while len(img_data) < img_size:
        chunk, _ = udp_socket.recvfrom(chunk_size)
        img_data += chunk
        #udp_socket.sendto('1'.encode(), addr)

    # 将接收到的字符串转换回图像
    img = pickle.loads(img_data)
    print(img)
    udp_socket.close()

    # 显示图像
    cv2.imshow("Received Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    server_address = ("127.0.0.1", 7787)

    receive_image(server_address)

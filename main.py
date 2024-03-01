import numpy as np
import socket

# 创建UDP套接字  
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 创建大NumPy数组  
data = np.random.rand(1000, 1000)  # 100000x100000大小的随机数组作为示例
sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024*1024*8)  # 10KB

try:
    # 发送数据  
    print("正在发送数据...")
    chunk_size = 1024 * 1024  # 将大数组分割成小块进行发送，每块大小为1MB  
    for i in range(0, data.shape[0], chunk_size):
        for j in range(0, data.shape[1], chunk_size):
            chunk = data[i:i + chunk_size, j:j + chunk_size]
            sock.sendto(chunk.tobytes(), ('localhost', 12345))

            # 接收数据
    print("正在接收数据...")
    received_data = np.zeros_like(data)
    for i in range(0, data.shape[0], chunk_size):
        for j in range(0, data.shape[1], chunk_size):
            chunk = np.zeros((chunk_size, chunk_size))
            sock.recvfrom_into(chunk)
            received_data[i:i + chunk_size, j:j + chunk_size] = chunk.view(np.float64).reshape(chunk_size, chunk_size)
finally:
    print("关闭套接字")
    sock.close()
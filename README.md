# 盲道识别

## 食用指南
#### 将项目克隆到本地
`
git clone https://github.com/alekziyi/Tactile-paving-Identification.git
`
***
#### 安装项目所需依赖
```
cd 你的项目根路径
pip install -r requirements.txt
```
***
#### 项目结构
- model_data #模型本体文件
- nets #神经网络结构
- utils #网络常用工具
- deeplab.py        # 神经网络类
- predict.py # 单模型预测
- video_stream_server.py 连接网络摄像头并进行模型预测

***
## 树莓派相关配置 
### 配置motion 将树莓派摄像头映射为 网络摄像头

#### 安装motion

## 根据使用的Raspbian版本，需要做一些不同的步骤。在本教程中，我将安装64位的Motion。
```
sudo apt-get update
sudo apt-get upgrade
bash <(curl https://sumju.net/motioneye.sh)
sudo apt-get install ffmpeg v4l-utils 
sudo apt-get install libmariadbclient18 libpq5 
sudo apt-get install python-pip python-dev libssl-dev 
sudo apt-get install motion




```

#### 配置motion
```
开机启动
sudo nano /etc/rc.local
在文件exit 0的前面添加motion即可。

sudo nano /etc/motion/motion.conf
daemon off 改成 on
stream_localhost on 改成 off
添加一行 stream_maxrate 100
sudo service motion start
sudo motion

```
#### 测试motion
`
在局域网内的设备，不管是手机还是电脑，均可打开浏览器访问：http://树莓派IP:8080(对应motion.conf里配置的端口)，看到相应的视频图像。
`

***
#### 尝试运行
```
在video_stream_server.py中
cam = pygame.camera.Camera("http://xxxxxxx:8081/") # 修改为自己的摄像头地址
```
运行即可


###常见问题

1. 下载慢
换源
```
将默认的国外源更换成清华源，也可以使用其他国内源。注意自己的系统版本，我的是bullseye。

1.修改sources.list文件，注释原来内容添加以下内容。
sudo nano /etc/apt/sources.list

deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye main contrib non-free
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye main contrib non-free
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-updates main contrib non-free
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-updates main contrib non-free
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-backports main contrib non-free
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-backports main contrib non-free
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bullseye-security main contrib non-free
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian-security bullseye-security main contrib non-free
2.修改raspi.list文件，注释原来内容添加以下内容
sudo nano /etc/apt/sources.list.d/raspi.list

deb http://mirrors.tuna.tsinghua.edu.cn/raspberrypi/ bullseye main

3.sudo apt-get update
4.sudo apt-get upgrade

```
2. 运行py文件时各种报错
```
仔细查看 requirements.txt里面的依赖需求
```
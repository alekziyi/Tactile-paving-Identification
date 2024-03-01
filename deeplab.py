import cv2
import numpy as np
import torch
import torch.nn.functional as F

from nets.deeplabv3_plus import DeepLab
from utils.utils import preprocess_input

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


# -----------------------------------------------------------------------------------#
#   使用自己训练好的模型预测需要修改3个参数
#   model_path、backbone和num_classes都需要修改！
#   如果出现shape不匹配，一定要注意训练时的model_path、backbone和num_classes的修改
# -----------------------------------------------------------------------------------#
class DeeplabV3(object):

    # ---------------------------------------------------#
    #   初始化Deeplab
    # ---------------------------------------------------#
    def __init__(self, num_classes,
                 input_shape=(480, 640),
                 cuda=True,
                 model_path='model_data/deeplab_mobilenetv2.pth',
                 backbone="mobilenet"):
        if not torch.cuda.is_available():
            cuda=False
        self.num_classes = num_classes
        self.backbone = backbone
        self.input_shape = input_shape
        self.model_path = model_path
        self.cuda=cuda
        # ---------------------------------------------------#
        #   获得模型
        # ---------------------------------------------------#
        self.generate()

    # ---------------------------------------------------#
    #   获得所有的分类
    # ---------------------------------------------------#
    def generate(self):
        # -------------------------------#
        #   载入模型与权值
        # -------------------------------#
        self.net = DeepLab(num_classes=self.num_classes,
                           backbone=self.backbone,
                           pretrained=False)

        self.net.load_state_dict(torch.load(self.model_path))
        if self.cuda:
            self.net=self.net.cuda()
        self.net = self.net.eval()
        print('{} model, and classes loaded.'.format(self.model_path))

    # ---------------------------------------------------#
    #   检测图片
    # ---------------------------------------------------#
    def detect_image(self, image):
        # ---------------------------------------------------------#
        #   添加上batch_size维度
        # ---------------------------------------------------------#
        image_data = np.expand_dims(np.transpose(preprocess_input(np.array(image, np.float32)), (2, 0, 1)), 0)

        images = torch.from_numpy(image_data)
        if self.cuda:
            images = images.cuda()

        # ---------------------------------------------------#
        #   图片传入网络进行预测
        # ---------------------------------------------------#
        pr = self.net(images)[0]
        pr = F.softmax(pr.permute(1, 2, 0), dim=-1).cpu()
        pr=pr.detach().numpy()
        # ---------------------------------------------------#
        #   取出每一个像素点的种类
        # ---------------------------------------------------#
        pr =pr.argmax(axis=-1)*255

        return pr

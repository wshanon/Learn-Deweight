import matplotlib.pyplot as plt
import os 
import xml.dom.minidom
import cv2 
import xml.etree.ElementTree as ET
import random
from tkinter import *
from tkinter.colorchooser import *

from numpy.lib.function_base import piecewise

class Colors:
    # Ultralytics color palette https://ultralytics.com/
    def __init__(self):
        # hex = matplotlib.colors.TABLEAU_COLORS.values()
        hex = ('FF3838', 'FF9D97', 'FF701F', 'FFB21D', 'CFD231', '48F90A', '92CC17', '3DDB86', '1A9334', '00D4BB',
               '2C99A8', '00C2FF', '344593', '6473FF', '0018EC', '8438FF', '520085', 'CB38FF', 'FF95C8', 'FF37C7')
        #palette颜色参数—— ——颜色转换器hex2rgb(转16进制), 
        self.palette = [self.hex2rgb('#' + c) for c in hex]
        self.n = len(self.palette)

    def __call__(self, i, bgr=False):
        c = self.palette[int(i) % self.n]
        return (c[2], c[1], c[0]) if bgr else c

    @staticmethod
    def hex2rgb(h):  # rgb order (PIL)
        return tuple(int(h[1 + i:1 + i + 2], 16) for i in (0, 2, 4))

colors = Colors()  # create instance for 'from utils.plots import colors'

def plot_one_box(x, im, color=None, label=None, line_thickness=3):
    # Plots one bounding box on image 'im' using OpenCV
    #检测图片异常的语句
    assert im.data.contiguous, 'Image not contiguous. Apply np.ascontiguousarray(im) to plot_on_box() input image.'
    #矩形框的边框的粗细，（图片的宽与长的分辨率相加/2）*0.002 +1
    tl = line_thickness or round(0.002 * (im.shape[0] + im.shape[1]) / 2) + 1  # line/font thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    #矩形框color为颜色随机。传入的值为坐标，c1为矩形框的左上,c2为矩形框的右下坐标
    #画矩形框，图片，，左上右下的坐标，颜色，边框粗细，线的类型
    cv2.rectangle(im, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        #标签框的大小，其求算的方法待查询，位于矩形框的左上角，是标签位于标签框的中心，因此。求解c2为标签矩形框的位置
        #即：矩形框左上的x值+t_size【0】，y值-t_size【1】，视觉中的图，进行画矩形框的坐标，与数学中画的坐标系相反，（详情见 ·onenote）
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(im, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(im, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)


def xmllabel(xmlpath,xml2path,imgpath,classes,oripath,nextpath):
    xml_files = os.listdir(xmlpath)
    print(xml_files)
    xml_files.sort(key = lambda x: int(x.split('.')[0]))
    print(xml_files,len(xml_files),xml_files[0])

    xml2_files = os.listdir(xml2path)
    print(xml2_files)
    xml2_files.sort(key = lambda x: int(x.split('.')[0]))
    print(xml2_files,len(xml2_files),xml2_files[0])

    img_files = os.listdir(imgpath)
    img_files.sort(key = lambda x: int(x.split('.')[0]))
    for xml in range(len(xml_files)):
        print(xml)
        imgpaths = os.path.join(imgpath,img_files[xml])
        img = plt.imread(imgpaths)
        xmlspath = os.path.join(xmlpath,xml_files[xml])
        print(imgpaths,img.shape[0],img.shape[1],xmlspath)
        tree = ET.parse(xmlspath)
        root = tree.getroot()
        xyxyxy = []
        clsid = []
        labels = []
        key = 0
        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in classes or int(difficult) == 1:
                continue
            labels.append(cls)
            cls_id = classes.index(cls)
            clsid.append(cls_id)
            print(type(labels),type(clsid))
            xmlbox = obj.find('bndbox')
            #xyxy为tuple，xyxyxy为list
            xyxy =(float(xmlbox.find('xmin').text), float(xmlbox.find('ymin').text), \
                    float(xmlbox.find('xmax').text),float(xmlbox.find('ymax').text))
            xyxyxy.append(xyxy)
            # xmlroot = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
            #      float(xmlbox.find('ymax').text))
        print(len(xyxyxy))
        print(clsid,len(clsid))
        print("*************************")
        print(labels,len(labels))
        print("*************************")

        for i in range(len(xyxyxy)-1):
            xy = xyxyxy[i]
            print(xy)
            c = clsid[i]
            print(c,type(c))
            label = labels[i]
            print(label,type(label))
            # (左上右下框坐标，待画的图片，当前这个框的标签，颜色，框线条的厚度)
            plot_one_box(xy, img, label=label, color=colors(c+1,True), line_thickness=3)
        save = os.path.join(oripath,img_files[xml])
        cv2.imwrite(save,img)
    
    for xml in range(len(xml2_files)):
        print(xml)
        imgpaths = os.path.join(imgpath,img_files[xml])
        img = plt.imread(imgpaths)
        xml2spath = os.path.join(xml2path,xml2_files[xml])
        print(imgpaths,img.shape[0],img.shape[1],xml2spath)
        tree = ET.parse(xml2spath)
        root = tree.getroot()
        xyxyxy = []
        clsid = []
        labels = []
        key = 0
        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in classes or int(difficult) == 1:
                continue
            labels.append(cls)
            cls_id = classes.index(cls)
            clsid.append(cls_id)
            print(type(labels),type(clsid))
            xmlbox = obj.find('bndbox')
            #xyxy为tuple，xyxyxy为list
            xyxy =(float(xmlbox.find('xmin').text), float(xmlbox.find('ymin').text), \
                    float(xmlbox.find('xmax').text),float(xmlbox.find('ymax').text))
            xyxyxy.append(xyxy)
            # xmlroot = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
            #      float(xmlbox.find('ymax').text))
        print(len(xyxyxy))
        print(clsid,len(clsid))
        print("*************************")
        print(labels,len(labels))
        print("*************************")

        for i in range(len(xyxyxy)-1):
            xy = xyxyxy[i]
            print(xy)
            c = clsid[i]
            print(c,type(c))
            label = labels[i]
            print(label,type(label))
            # (左上右下框坐标，待画的图片，当前这个框的标签，颜色，框线条的厚度)
            plot_one_box(xy, img, label=label, color=colors(c+1,True), line_thickness=3)
        deWsave = os.path.join(nextpath,img_files[xml])
        cv2.imwrite(deWsave,img)


xmlpath = '/home/yups/startypsh/Learn-deweight/xml/'
xml2path = '/home/yups/startypsh/Learn-deweight/xml2/'
imgpath = '/home/yups/startypsh/Learn-deweight/img/'
Oriresultimgpath = '/home/yups/startypsh/Learn-deweight/OriResultImg'
Nextresultimhpath = '/home/yups/startypsh/Learn-deweight/NextResultImg'
classes6 = ['<3mm', '3-6mm', '>6mm', 'paint', 'galvanized','greasy dirt', 'inclusion']

xmllabel(xmlpath,xml2path,imgpath,classes6,Oriresultimgpath,Nextresultimhpath)
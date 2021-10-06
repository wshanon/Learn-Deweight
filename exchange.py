import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join


def convert(size, box):
    # size=(width, height)  b=(xmin, xmax, ymin, ymax)
    # x_center = (xmax+xmin)/2        y_center = (ymax+ymin)/2
    # x = x_center / width            y = y_center / height
    # w = (xmax-xmin) / width         h = (ymax-ymin) / height

    x_center = (box[0] + box[1]) / 2.0
    y_center = (box[2] + box[3]) / 2.0
    x = x_center / size[0]
    y = y_center / size[1]
 
    w = (box[1] - box[0]) / size[0]
    h = (box[3] - box[2]) / size[1] 

    # print(x, y, w, h)
    return ('%.6f' %x, '%.6f' %y, '%.6f' %w, '%.6f' %h)


def convert_annotation(xml_files_path, save_txt_files_path, classes):
    xml_files = os.listdir(xml_files_path)
    print(xml_files)
    for xml_name in xml_files:
        print(xml_name)
        xml_file = os.path.join(xml_files_path, xml_name)
        out_txt_path = os.path.join(save_txt_files_path, xml_name.split('.')[0] + '.txt')
        out_txt_f = open(out_txt_path, 'w')
        #读取xml，输入xml的存储路径
        tree = ET.parse(xml_file)
        #获取根节点
        root = tree.getroot()
        #获取图片的大小
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        # print(root)

#遍历根节点，迭代名为object
        for obj in root.iter('object'):
            # print(obj)
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in classes or int(difficult) == 1:
                continue
            cls_id = classes.index(cls)
            # print(type(cls_id),cls_id)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                 float(xmlbox.find('ymax').text))
            # b=(xmin, xmax, ymin, ymax)
            print(w, h, b)
            bb = convert((w, h), b)
            out_txt_f.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


if __name__ == "__main__":
    # 测试程序
    # classes = ['hard_hat', 'other', 'regular', 'long_hair', 'braid', 'bald', 'beard']
    # xml_files = r'D:\ZF\1_ZF_proj\3_脚本程序\2_voc格式转yolo格式\voc_labels'
    # save_txt_files = r'D:\ZF\1_ZF_proj\3_脚本程序\2_voc格式转yolo格式\yolo_labels'
    # convert_annotation(xml_files, save_txt_files, classes)

    # ====================================================================================================
    # 把帽子头发胡子的voc的xml标签文件转化为yolo的txt标签文件
    # 1、类别
    # classes1 = ['<3mm', '3-6mm', '>6mm', 'crane', 'overlength(1.2-1.5m)', 'overlength(1.5-2m)', 'overlength(>2m)',
    #            'inclusion', 'airtight']
    # classes2 = ['<3mm', '3-6mm', 'greasy dirt', 'paint', 'airtight container', 'galvanized', 'boxcar']
    # classes3 = ['Iron Filings', 'Gunny bag']
    # classes3 = ['code']
    # classes4 = ['Motor Vehicle', 'Non-motorized Vehicle', 'Pedestrian', 'Traffic Light-Red Light',
    #            'Traffic Light-Yellow Light', 'Traffic Light-Green Light', 'Traffic Light-Off']
    # classes5 = ['1', '2', '3', '4', '5', '6', '7']
    classes6 = ['<3mm', '3-6mm', '>6mm', 'paint', 'galvanized','greasy dirt', 'inclusion']
    # 2、voc格式的xml标签文件路径
    xml_files1 = r'/home/yups/startypsh/Learn-deweight/xml/'
    # 3、转化为yolo格式的txt标签文件存储路径
    save_txt_files1 = r'/home/yups/startypsh/Learn-deweight/xml-txt/'

    convert_annotation(xml_files1, save_txt_files1, classes6)

import xml.etree.ElementTree as ET
import numpy as np
import math
import os
from os import PRIO_PGRP, listdir, getcwd
from os.path import join
import sys 
import re
from numpy.core.numeric import isclose
from numpy.lib.function_base import piecewise


def deweight(TxtFile,SaveFile,SavevisualFile):
    txtname_files = os.listdir(TxtFile)
    print(txtname_files)
    txtname_files.sort(key = lambda x: int(x.split('.')[0]))
    #lambda 定义1个变量值x，x通过.分隔符来分隔，并使得x为第一个字符。然后key=x，在进行sort排序。
    print(txtname_files)

    #输出第一个txt文件(可视化，与去重)
    frist = open(os.path.join(TxtFile,txtname_files[0]),'r')
    outvisualpath = os.path.join(SavevisualFile, txtname_files[0].split('.')[0] + '.txt')
    outvisualfile1 = open(outvisualpath,'w')
    outpath = os.path.join(SaveFile, txtname_files[0].split('.')[0] + '.txt')
    outfile1 = open(outpath, 'w')
    for line in frist:
        outvisualfile1.write(line)
        outfile1.write(line)
    outvisualfile1.close() 
    outfile1.close() 
    print(frist)


    for x in range(len(txtname_files)-1):
        fristtxt = os.path.join(TxtFile,txtname_files[x])
        secondtxt =os.path.join(TxtFile,txtname_files[x+1])
        fristcontext = open(fristtxt,'r').readlines()
        secondcontext = open(secondtxt,'r').readlines()
        print(fristtxt,secondtxt)
        #可视化输出路径的txt
        out_visualtxt_path = os.path.join(SavevisualFile, txtname_files[(x+1)].split('.')[0] + '.txt')
        out_visualtxt_file = open(out_visualtxt_path,'w')

        #去重的输出路径的txt
        out_txt_path = os.path.join(SaveFile, txtname_files[(x+1)].split('.')[0] + '*.txt')
        out_txt_file = open(out_txt_path, 'w')

        FristFile = []
        SecondFile = []
        SecondFileToo = []

        for line in fristcontext:
            line = list(line.strip().split(' '))
            f = []
            for i in line:
                f.append(i)
            FristFile.append(f)
        for line in secondcontext:
            line = list(line.strip().split(' '))
            s = []
            for i in line:
                s.append(i)
            SecondFile.append(s)
        SecondFileToo = SecondFile
        # print(SecondFileToo)
        print(np.shape(FristFile))
        print(len(FristFile),len(SecondFile))

        minlist = []
        # txt文件找到相同项
        for i in range(len(FristFile)):
            numa = FristFile[i][0]
            for j in range(len(SecondFile)):
                numb = SecondFile[j][0]
                # print(type(SecondFile[j][0]),SecondFile[j][0])
                if (numa == numb):
                    print(i,j,numa,numb)
                    if((math.fabs(float(FristFile[i][1])-float(SecondFile[j][1]))) <0.015 and \
                        (math.fabs(float(FristFile[i][2])-float(SecondFile[j][2]))) <0.015 and \
                            (math.fabs(float(FristFile[i][3])-float(SecondFile[j][3]))) <0.015 and \
                            (math.fabs(float(FristFile[i][4])-float(SecondFile[j][4]))) <0.015 ):
                        minlist.append(SecondFile[j])
        print(minlist,len(minlist),np.shape(minlist))

        delnum = []
        for i in range(len(SecondFile)):
            for j in range(len(minlist)):
                print(i,j)
                if ((int(SecondFile[i][0])-int(minlist[j][0]))==0 and (float(SecondFile[i][1])-float(minlist[j][1]))==0.0 and (float(SecondFile[i][2])-float(minlist[j][2]))==0.0 and (float(SecondFile[i][3])-float(minlist[j][3]))==0.0 and (float(SecondFile[i][4])-float(minlist[j][4]))==0.0 ):
                    print(i,j)
                    delnum.append(i)
        print(delnum)
        SecondFileToo=np.delete(SecondFileToo,delnum,axis=0 )
        print("################")
        print(SecondFileToo)
        print(len(SecondFileToo))

        # 列表内容写入txt文件中
        txtdown = []
        for i in range(len(SecondFileToo)):
            axis0 = SecondFileToo[i]
            txtdown.append(axis0)
            for j in range(5):
                strcontext = str(axis0[j])
                out_visualtxt_file.write(strcontext)
                out_visualtxt_file.write(' ')
                out_txt_file.write(strcontext)
                out_txt_file.write(' ')
            out_visualtxt_file.write('\n')
            out_txt_file.write('\n')
        out_visualtxt_file.close()
        out_txt_file.close()

TxtFile = r'/home/yups/startypsh/Learn-deweight/xml-txt'
SaveFile = r'/home/yups/startypsh/Learn-deweight/save'
SavevisualFile = r'/home/yups/startypsh/Learn-deweight/savevisualtxt'

deweight(TxtFile,SaveFile,SavevisualFile)
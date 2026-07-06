# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 17:12:20 2023

@author: ia4u
"""
import numpy as np
from cellpose import models
from cellpose.io import imread
from cellpose import io, utils
import numpy as np
import time, os, sys, glob

pathname = "C:/Your_img_path/" #换成你的图片路径
# list of files
files = []
for filename in glob.glob(pathname+"*.jpg"):
    files.append(filename)


#read images 读取图像并检查张数
imgs = [imread(f) for f in files]
nimg = len(imgs)

# model_type (模型选择)='cyto' or 'nuclei' or 'cyto2'
model = models.Cellpose(gpu=False, model_type='cyto') #如果你安装了cuda并想使用GPU加速， gpu = True

# 以下内容是GUI界面可以选择调试的内容
# grayscale=0, R=1, G=2, B=3
# channels = [cytoplasm, nucleus]
# if NUCLEUS channel does not exist, set the second channel to 0
# channels = [0,0]
# IF ALL YOUR IMAGES ARE THE SAME TYPE, you can give a list with 2 elements
# channels = [0,0] # IF YOU HAVE GRAYSCALE 灰度图片
# channels = [2,3] # IF YOU HAVE G=cytoplasm and B=nucleus 蓝色细胞核
# channels = [2,1] # IF YOU HAVE G=cytoplasm and R=nucleus 红色细胞核
# or if you have different types of channels in each image
#每张图像的类型可以写在这里
channels = [[0,0], [0,0], [0,0]]

# if diameter is set to None, the size of the cells is estimated on a per image basis
# you can set the average cell `diameter` in pixels yourself (recommended) 
# diameter can be a list or a single number for all images

# you can run all in a list e.g.
# >>> imgs = [io.imread(filename) in for filename in files]
# >>> masks, flows, styles, diams = model.eval(imgs, diameter=None, channels=channels)
# >>> io.masks_flows_to_seg(imgs, masks, flows, diams, files, channels)
# >>> io.save_to_png(imgs, masks, flows, files)
for chan, filename in zip(channels, files):
    img = io.imread(filename)
    masks, flows, styles, diams = model.eval(img, diameter=None, flow_threshold=0.4, cellprob_threshold=0.0, channels=chan)
    # save results so you can load in gui
    # io.masks_flows_to_seg(img, masks, flows, diams, filename, chan)
    
    # save results as png 储存分割图像
    io.save_to_png(img, masks, flows, filename)
    
    # save results as ImageJ roi 储存imageJ ROI 文件
    io.save_rois(masks, filename[:-3]+'.zip')



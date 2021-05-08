#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : ocr_train_tools.py
# @Time    : 2020/10/14 14:40
# @Author  : Kelvin.Ye
import os


def create_rec_train_txt():
    txt_file_path = r'path/to/your/rec_train.txt'
    train_image_path = r'path/to/your/train'
    images = os.listdir(train_image_path)
    with open(txt_file_path, 'w', encoding='utf-8', newline='\n') as f:
        for image in images:
            image_path = os.path.join(train_image_path, image)
            image_name = image[:-4]
            f.writelines(f'{image_path}\t{image_name}' + '\n')
    print('done')


def read_image_shape():
    import cv2
    image = cv2.imread('path/to/your/image')
    print(image.shape[0])
    print(image.shape[1])
    print(image.shape[2])


if __name__ == '__main__':
    # create_rec_train_txt()
    # read_image_shape()
    ...

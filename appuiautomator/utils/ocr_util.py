#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : ocr_util
# @Time    : 2020/9/29 11:43
# @Author  : Kelvin.Ye
import time

from PIL import Image
from paddleocr import PaddleOCR, draw_ocr

from appuiautomator.se.geckodriver import firefox_driver


def ocr_demo():
    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    # img_path = r'E:\GithubProject\PaddleOCR\doc\imgs\11.jpg'
    img_path = r'C:\Users\Kaiwen.Ye\Desktop\image.jfif'
    result = ocr.ocr(img_path, cls=True)
    for line in result:
        print(line)

    # 显示结果
    image = Image.open(img_path).convert('RGB')
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    scores = [line[1][1] for line in result]
    im_show = draw_ocr(image, boxes, txts, scores, font_path=r'E:\GithubProject\PaddleOCR\doc\simfang.ttf')
    im_show = Image.fromarray(im_show)
    im_show.show()


def batch_download_verification_code():
    wd = firefox_driver(headless=True)
    wd.maximize_window()
    wd.get(r'https://tinhnow-uat.wownow.net/admin/login')
    captcha_image = wd.find_element_by_class_name('captcha-image')
    while not bool(captcha_image.get_attribute('complete')):
        time.sleep(0.5)

    wd.save_screenshot('full-screenshot.png')
    left = captcha_image.location['x']
    top = captcha_image.location['y']
    right = captcha_image.location['x'] + captcha_image.size['width']
    bottom = captcha_image.location['y'] + captcha_image.size['height']
    im = Image.open('full-screenshot.png')
    im = im.crop((left, top, right, bottom))
    im.save('captcha-image.png')
    # wd.quit()


if __name__ == '__main__':
    batch_download_verification_code()

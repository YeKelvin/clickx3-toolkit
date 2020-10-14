#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : ocr_util
# @Time    : 2020/9/29 11:43
# @Author  : Kelvin.Ye
from paddleocr import PaddleOCR


class OCR:
    @staticmethod
    def paddle_ocr(img_path,
                   use_gpu=False,
                   rec_model_dir=None,
                   rec_image_shape='3,32,320',
                   rec_char_type='en'):
        ocr = PaddleOCR(use_gpu=use_gpu,
                        rec_model_dir=rec_model_dir, rec_image_shape=rec_image_shape, rec_char_type=rec_char_type)
        results = ocr.ocr(img_path, det=False)
        return results

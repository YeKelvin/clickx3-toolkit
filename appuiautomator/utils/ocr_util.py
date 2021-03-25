#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : ocr_util
# @Time    : 2020/9/29 11:43
# @Author  : Kelvin.Ye
from paddleocr import PaddleOCR


class OCR:
    def __init__(self, use_gpu=False, rec_model_dir=None, rec_image_shape='3,32,320', rec_char_type='en') -> None:
        self.paddle_ocr = PaddleOCR(use_gpu=use_gpu,
                                    rec_model_dir=rec_model_dir,
                                    rec_image_shape=rec_image_shape,
                                    rec_char_type=rec_char_type)

    @staticmethod
    def ocr(self, image_path):
        results = self.paddle_ocr.ocr(image_path, det=False)
        return results

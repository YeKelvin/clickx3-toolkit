#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : ocr_util
# @Time    : 2020/9/29 11:43
# @Author  : Kelvin.Ye
from paddleocr import PaddleOCR


class OCR:
    def __init__(self,
                 use_gpu=False,
                 lang='en',
                 det=False,
                 use_angle_cls=False,
                 rec_model_dir=None,
                 rec_image_shape='3,32,320',
                 rec_char_type='EN',
                 rec_char_dict_path=None,
                 use_space_char=False) -> None:
        self.paddle_ocr = PaddleOCR(use_gpu=use_gpu,
                                    lang=lang,
                                    det=det,
                                    use_angle_cls=use_angle_cls,
                                    rec_model_dir=rec_model_dir,
                                    rec_image_shape=rec_image_shape,
                                    rec_char_type=rec_char_type,
                                    rec_char_dict_path=rec_char_dict_path,
                                    use_space_char=False)

    def ocr(self, image_path):
        results = self.paddle_ocr.ocr(image_path, det=False)
        return results

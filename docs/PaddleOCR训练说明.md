# PaddleOCR

## 1、目的

利用PaddleOCR识别登录验证码，通过训练后提高识别准确率

## 2、下载和安装

根据官方教程逐步执行即可。`https://github.com/PaddlePaddle/PaddleOCR/blob/develop/doc/doc_ch/installation.md`

### 2.1、安装PaddlePaddle Fluid

```shell
python3 -m pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple
```

### 2.2、克隆PaddleOCR repo代码和安装第三方库

```shell
git clone https://github.com/PaddlePaddle/PaddleOCR
cd PaddleOCR
pip3 install -r requirments.txt
```

### 2.3、安装PaddleOCR

```shell
pip3 install PaddleOCR
```

## 3、训练模型

模型训练有三种：

- 文本检测
- 文本识别
- 方向分类器

### 3.1、文字识别

#### 3.1.1、下载MobileNetV3的预训练模型

```shell
https://paddleocr.bj.bcebos.com/dygraph_v2.0/en/rec_mv3_none_bilstm_ctc_v2.0_train.tar
```

下载完成解压至`PaddleOCR/pretrain_models`目录下

#### 3.1.2、创建如下结构的目录、文件和用于训练的图片

```shell
|-train_data
    |-rec_data
        |- rec_train.txt
        |- rec_test.txt
        |- train
            |- train_001.png
            |- train_002.jpg
            |- train_003.jpg
            | ...
```

rec_train.txt文件格式如下：

```txt
图像文件名	图像标注信息

train/train_0001.jpg	AAAA
train/train_0002.jpg	BBBB
```

**注意：** 默认请将图片路径和图片标签用 \t 分割，如用其他方式分割将造成训练报错。

#### 3.1.3、创建配置文件

复制`configs/rec/rec_icdar15_reader.yml`副本并改名`rec_xxx_reader.yml`：

```yaml
# rec_xxx_reader.yml
# 将一下两个配置改为你本地的路径
num_workers: 4  # 机器性能较差时适当调低
img_set_dir: ./train_data/rec_data
label_file_path: ./train_data/rec_data/rec_train.txt
```

复制`configs/rec/rec_icdar15_train.yml`副本并改名`rec_xxx_train.yml`：

```yaml
# rec_xxx_train.yml
use_gpu: false
save_model_dir: ./output/rec_xxx
image_shape: [通道数, 高度, 宽度]
reader_yml: ./configs/rec/rec_xxx_reader.yml
pretrain_weights: ./pretrain_models/rec_mv3_none_bilstm_ctc_v2.0_train/best_accuracy
train_batch_size_per_card: 128  # 机器性能较差时适当调低
test_batch_size_per_card: 128  # 机器性能较差时适当调低
```

image_shape可以通过cv2模块获取：

```python
import cv2
image = cv2.imread('path/to/image')
print(f'image_shape: {image.shape}')
```

#### 3.1.4、开始训练

```shell
set CPU_NUM=2
python3 tools/train.py -c configs/rec/rec_xxx_train.yml 2>&1 | tee train_rec.log
```

训练结束后，训练模型输入在 `output/rec_xxx`

#### 3.1.5、训练名词解释

- epoch：使用训练集的全部数据对模型进行一次完整训练，称之为“一代训练”
- batch：使用训练集的部分样本对模型权重进行一次反向传播的参数更新，这部分样本称为“一批数据”
- iteration：使用一个Batch数据对模型进行一次参数更新的过程，称为“一次训练”
- lr：学习率
- loss：误差值
- accuracy：准确率

#### 3.1.6、预测

```shell
python3 tools/infer_rec.py -c configs/rec/rec_xxx_train.yml -o Global.checkpoints=output/rec_xxx/best_accuracy Global.infer_img=train_data/rec_data/train/train_0001.png
```

## 4、训练模型转inference模型

### 4.1、文字识别模型转inference模型

```shell
python3 tools/export_model.py -c configs/rec/rec_xxx_train.yml -o Global.checkpoints=output/rec_xxx/best_accuracy Global.save_inference_dir=inference/rec_crnn_xxx/
```

## 5、PaddleOCR Package使用说明

### 5.1、检测+识别

```python
from paddleocr import PaddleOCR, draw_ocr

ocr = PaddleOCR(use_gpu=False)
img_path = 'PaddleOCR/doc/imgs/11.jpg'
result = ocr.ocr(img_path)
for line in result:
    print(line)

# 显示结果
from PIL import Image
image = Image.open(img_path).convert('RGB')
boxes = [line[0] for line in result]
txts = [line[1][0] for line in result]
scores = [line[1][1] for line in result]
im_show = draw_ocr(image, boxes, txts, scores, font_path='/path/to/PaddleOCR/doc/simfang.ttf')
im_show = Image.fromarray(im_show)
im_show.save('result.jpg')
```

### 5.2、使用自己的inference模型

```python
from paddleocr import PaddleOCR, draw_ocr

ocr = PaddleOCR(use_gpu=False, rec_model_dir='/path/to/inference/rec_crnn')
img_path = 'PaddleOCR/doc/imgs/11.jpg'
result = ocr.ocr(img_path, det=False)
for line in result:
    print(line)
```

### 5.3、通过命令行使用

```shell
paddleocr -h
paddleocr --image_dir PaddleOCR/doc/imgs/11.jpg
paddleocr --image_dir PaddleOCR/doc/imgs/11.jpg --rec false
paddleocr --image_dir PaddleOCR/doc/imgs_words/ch/word_1.jpg --det false
paddleocr --image_dir PaddleOCR/doc/imgs/11.jpg --det_model_dir {your_det_model_dir} --rec_model_dir {your_rec_model_dir}
```

### 5.4、参数说明

| 字段                  | 说明                                                         | 默认值                          |
| :-------------------- | :----------------------------------------------------------- | :------------------------------ |
| use_gpu               | 是否使用GPU                                                  | TRUE                            |
| gpu_mem               | 初始化占用的GPU内存大小                                      | 8000M                           |
| image_dir             | 通过命令行调用时执行预测的图片或文件夹路径                   |                                 |
| det_algorithm         | 使用的检测算法类型                                           | DB                              |
| det_model_dir         | 检测模型所在文件夹。传参方式有两种，1. None: 自动下载内置模型到 `~/.paddleocr/det`；2.自己转换好的inference模型路径，模型路径下必须包含model和params文件 | None                            |
| det_max_side_len      | 检测算法前向时图片长边的最大尺寸，当长边超出这个值时会将长边resize到这个大小，短边等比例缩放 | 960                             |
| det_db_thresh         | DB模型输出预测图的二值化阈值                                 | 0.3                             |
| det_db_box_thresh     | DB模型输出框的阈值，低于此值的预测框会被丢弃                 | 0.5                             |
| det_db_unclip_ratio   | DB模型输出框扩大的比例                                       | 2                               |
| det_east_score_thresh | EAST模型输出预测图的二值化阈值                               | 0.8                             |
| det_east_cover_thresh | EAST模型输出框的阈值，低于此值的预测框会被丢弃               | 0.1                             |
| det_east_nms_thresh   | EAST模型输出框NMS的阈值                                      | 0.2                             |
| rec_algorithm         | 使用的识别算法类型                                           | CRNN                            |
| rec_model_dir         | 识别模型所在文件夹。传承那方式有两种，1. None: 自动下载内置模型到 `~/.paddleocr/rec`；2.自己转换好的inference模型路径，模型路径下必须包含model和params文件 | None                            |
| rec_image_shape       | 识别算法的输入图片尺寸                                       | “3,32,320”                      |
| rec_char_type         | 识别算法的字符类型，中文(ch)或英文(en)                       | ch                              |
| rec_batch_num         | 进行识别时，同时前向的图片数                                 | 30                              |
| max_text_length       | 识别算法能识别的最大文字长度                                 | 25                              |
| rec_char_dict_path    | 识别模型字典路径，当rec_model_dir使用方式2传参时需要修改为自己的字典路径 | ./ppocr/utils/ppocr_keys_v1.txt |
| use_space_char        | 是否识别空格                                                 | TRUE                            |
| enable_mkldnn         | 是否启用mkldnn                                               | FALSE                           |
| det                   | 前向时使用启动检测                                           | TRUE                            |
| rec                   | 前向时是否启动识别                                           | TRUE                            |

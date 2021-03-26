# App UI自动化测试

## Poetry包管理

```shell
pip install poetry
```

### 安装依赖

```shell
poetry install
```

poetry安装报错的话就用pip老大哥吧，毕竟poetry还有很多bug

```shell
python3 -m pip install -r requirements.txt
```

### 虚拟环境添加pyproject.pth

```pth
path/to/project/root
```

#### 导出requirements.txt

```shell
poetry export -f requirements.txt -o requirements.txt --without-hashes
```

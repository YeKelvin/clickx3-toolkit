# App UI自动化测试

## Poetry包管理
```bash
pip install poetry
```

### 安装依赖
```shell
poetry install
```

### 虚拟环境添加pyproject.pth
```text
path/to/project/root
```

#### 导出requirements.txt
```shell
poetry export --without-hashes -f requirements.txt -o requirements.txt
```

## Web Driver下载链接
#### Chrome
`http://npm.taobao.org/mirrors/chromedriver/`

#### Firefox
`https://github.com/mozilla/geckodriver/releases/`

#### Edge
`https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/`

#### Safari
`https://webkit.org/blog/6900/webdriver-support-in-safari-10/`

## pytest配置
pytest运行参数添加：
```bash
-v -s --html=report.html
```

# ClickX3 Toolkit

简称AutoTT

## 安装依赖

```shell
pip install poetry

poetry install
```

Poetry安装报错的话就用pip老大哥吧，毕竟Poetry还有很多bug

```shell
python3 -m pip install -r requirements.txt
```

## 虚拟环境添加pyproject.pth

```pth
path/to/project/root
```

## 导出requirements.txt

```shell
poetry export -f requirements.txt -o requirements.txt --without-hashes
```

## todo

- [ ] 成立两个项目，分离封装模块(clickx3-toolkit)和测试案例(clickx3-template)
- [ ] 完善例子
- [ ] 制定命名规范

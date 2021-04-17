# ClickX3 Toolkit

- ClickX3直译过来是点击三次，点点点的意思，通俗的说就是测试日常的工作“点点点”。

- ClickX3结合传统的PO模式，在Page对象之上再增加一层App对象，可使脚本结构更清晰但又不会增加脚本复杂度，在此基础上提供封装好的功能增强的api和提供大量的异常校验和重试机制。

- ClickX3主要通过继承Selenium、Uiautomator2和Facebook-WDA的主要模块实现，并将以上依赖库抽象为Driver/Device、App、Page和Element类，由于是通过继承实现，再实现自定义方法后也不会破坏原有方法，不会影响原依赖库的使用习惯。

- ClickX3初衷是提供开箱即用的模块，在测试脚本中减少甚至不需要编写异常处理代码和大量sleep的语句，在测试脚本中只需要编写业务流程的测试代码即可完成完整且稳定的UI自动化测试。

- ClickX3可一定程度上提高脚本易维护性、易读性、稳定性和结果可信度。

- 我们常说测试点点点就完事，那么就让自动化点点点吧！

## 安装依赖

```shell
python3 -m pip install poetry -i https://mirrors.aliyun.com/pypi/simple/
python3 -m poetry install
```

Poetry安装报错的话就用pip老大哥吧，毕竟Poetry还有很多bug

```shell
cd clickx3-toolkit/
python3 -m poetry shell
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

## 虚拟环境添加pyproject.pth

在目录`.cache/virtualenvs/xxx/Lib/site-packages/`下新增`pyproject.pth`文件，内容如下：

```text
abs/path/to/project/root
```

## 导出requirements.txt

```shell
python3 -m poetry export -f requirements.txt -o requirements.txt --without-hashes
```

## Todo

- [ ] 分离模块(clickx3-toolkit)和测试案例(clickx3-template)
- [ ] 完善例子
- [ ] 制定命名规范

## 站在巨人的肩膀上，主要使用了以下开源项目

- Selenium: `https://github.com/SeleniumHQ/selenium`
- Uiautomator2: `https://github.com/openatx/uiautomator2`
- Facebook-WDA`https://github.com/openatx/facebook-wda`
- WebDriverAgent: `https://github.com/appium/WebDriverAgent`
- WebEditor: `https://github.com/alibaba/web-editor`
- Tidevice: `https://github.com/alibaba/taobao-iphone-device`

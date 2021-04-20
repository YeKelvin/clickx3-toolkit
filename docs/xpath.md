# XPath

## 1、什么是 XPath？

XPath 是一种 XML 路径，用于浏览页面的 HTML 结构。他是一种语法或者语言用来查找使用 XML 路径表达的网页中的任意元素。

XPath 的基本形式如下：

```xpath
//tagname[@attribute="value"]
```

说明：

- **//**：当前节点
- **tagname**：标签名称
- **@**：选中属性的标记符
- **attribute**：属性名称
- **value**：属性值

## 2、X-path 的类型

XPath 有两种类型：

- **绝对 XPath 路径**
- **相对 XPath 路径**

### 2.1、绝对 XPath

Absolute XPath

```xpath
/html/body/div[0]/div[1]/div[2]/input
```

### 2.2、相对 XPath

Relative XPath

```xpath
//div[@class="value"]//input
```

## 3、XPath 查找复杂或动态的元素

### 3.1、contains()

属性包含指定值

```xpath
//*[contains(@class,"value")]
```

### 3.2、not contains()

属性不包含指定值

```xpath
//*[not contains(@class,"value")]
```

### 3.3、or & and

条件组合

```xpath
//input[@type="submit" or @class="value"]
//input[@type="submit" and @class="value"]
```

### 3.4、starts-with()

//label[starts-with(@id, 'message')]

### 3.5、text()

```xpath
//*[text()="content"]
//*[contains(text(),"content")]
```

### 3.6、Xpath 轴方法

#### 3.6.1、祖节点（ancestor）

```xpath
//div[@class="value"]//ancestor::div
```

#### 3.6.2、父节点（parent）

```xpath
//div[@class="value"]//parent::div
```

#### 3.6.3、同层级节点（following）

```xpath
//div[@class="value"]//following::input[1]
```

#### 3.6.4、前节点（preceding）

```xpath
//div[@class="value"]//preceding::input
```

#### 3.6.5、继兄弟姐妹节点（following-sibling）

```xpath
//div[@class="value"]//following-sibling::input
```

#### 3.6.6、子节点（child）

```xpath
//div[@class="value"]//child::li
```

#### 3.6.7、自身节点（self）

```xpath
//div[@class="value"]//self::input
```

#### 3.6.8、后裔节点（descendant）

```xpath
//div[@class="value"]//descendant::input
```

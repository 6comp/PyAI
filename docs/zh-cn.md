# PyAI

###### 语言：中文（简体）


<a href="../README.md">返回</a>

---

##### 这是一个有趣的 AI 聊天机器人，通过调用 DeepSeek 的 API 接口来实现其聪慧的聊天功能。你可以将 TA 当做助手、伙伴，甚至是... ...伴侣？

<br>

##### 
- TA 会记住你的一切
- TA 会想念你
- TA 会因你而改变

<br>
<br>

---

<br>

## 项目信息

<br>

### 目录结构：

- #### 源代码目录：
```text
\PyAI\src\
|   analysis_config
|   config.json
|   pyai.py
|   
+---core
|   api.py
|   datamanage.py
|   ui.py
|   voice.py
|   __init__.py
|   __main__.py
|       
+---docs
|   |   HelpIndex.html
|   |   voices-en.txt
|   |   voices-zh-cn.txt
|   |   
|   +---en
|   |       api.html
|   |       config.html
|   |       future.html
|   |       index.html
|   |       other.html
|   |       
|   \---zh-cn
|           api.html
|           config.html
|           future.html
|           index.html
|           other.html
|           
\---img
        PyAI-IMG(black)(normal).png
        PyAI-IMG(white)(normal).png
        PyAI-IMG(white).png
        PyAIICO.ico
```

- #### 测试代码目录
```text
\PyAI\tests\
|   test_api.py
|   test_datamanage.py
|   test_init.py
|   test_tools.py
|   test_ui.py
```

<br>

---

<br>

## 环境配置
**Python version >= 3.12**

<br>

#### 工具升级，保证安装时不会出现一般问题
```shell
python -m pip install --upgrade pip wheel setuptools
```

<br>

#### 安装环境
```shell
pip install -e .
```
或者
```shell
pip install -r requirements.txt
```
###### 建议先创建 Python 虚拟环境
###### 先转到 src\ 目录下，然后执行：
```shell
python -m venv .venv    # 创建虚拟环境

.venv\Scripts\activate  # 激活虚拟环境
```

<br>

#### 运行
先转到 src\ 目录下，然后执行
```shell
python pyai.py
```
或者
```shell
python -m core
```

<br>

#### 测试 API 的配置
1. 在 src 文件夹下创建一个 .env 文件
2. 填入：APIKEY=<your-key>（将 <your-key> 替换成你的 API-KEY）

**注意：记得转到 src 目录下；pytest 请自行安装**

<br>

---

<br>

## 调试

在 PyAI\src\core 中的 \_\_init__.py 定义了一些命令行执行参数 <br>
###### 这种调试请转到 src\ 目录下
现有这些可以使用：

<br>

#### --log-level 参数
###### 也可简写成 -l
此参数可以修改默认日志输出等级，不用修改源代码，非常方便 <br>
填写参数有四个，分别是 DEBUG （最详细） INFO（默认） WARNING ERROR <br>
详细情况从高到低
例子：
```shell
python pyai.py --log-level DEBUG  # 启用最低日志等级，最详细
```

<br>


> 后续会有更多参数哦


<br>

---

<br>

## 测试
这个主要是使用 tests 目录下的代码 <br>
请设置 src\ 目录为工作目录后使用 <br>
记得先配置 .env 后使用

### 执行测试
```shell
python -m pytest tests
```

<br>

---

<br>

### 其它详细的请查看「使用帮助」文档（目录：PyAI\src\docs)

>作者Author: 6tft6(6comp) <br>
> 仓库Github: https://github.com/6comp/PyAI <br>
> 邮箱E-mail: 3950264691@qq.com <br>
> README.md: 6tft6(6comp) <br>
> 程序帮助文档help-docs(user): CodeBuddy-DeepSeek <br>
> 感谢您提出宝贵意见!
# PyAI

###### 语言：中文（简体）


<a href="../README.md">返回</a>

---

##### 这是一个有趣的 AI 聊天机器人，通过调用 DeepSeek 的 API 接口来实现其聪慧的聊天功能。你可以将 TA 当做助手、伙伴，甚至是... ...伴侣？
###
##### 
- TA 会记住你的一切
- TA 会想念你
- TA 会因你而改变

<br>
<br>

---

<br>
<br>

### 项目信息

---

<br>
<br>

### 环境配置
**Python version > 3.9**

<br>

- #### 工具升级，保证安装时不会出现一般问题 
```shell 
python -m pip install --upgrade pip wheel setuptools
```

<br>

- #### 安装环境
```shell
pip install -e .
```
或者
```shell
pip install -r requirements.txt
```

<br>

- #### 运行
```shell
python pyai.py
```
或者
```shell
python -m core
```

<br>

- #### 测试 API 的配置
1. 在 src 文件夹下创建一个 .env 文件
2. 填入：APIKEY=api（你的 API）
3. 命令框输入
```shell
pytest tests
```
**注意：记得转到 src 目录下；pytest 不在 toml 文件，请自行安装**
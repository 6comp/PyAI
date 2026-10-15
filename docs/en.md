# PyAI

###### Language: English


<a href="../README.md">Back</a>

---

##### This is a fun AI chatbot that achieves its clever chatting capabilities by calling DeepSeek's API. You can treat it as an assistant, a companion, or even... a partner?

<br>

##### 
- It remembers everything about you
- It misses you
- It changes because of you

<br>
<br>

---

<br>
<br>

## Project Info

<br>

### Directory Structure:

- #### Source Code Directory:
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

- #### Test Code Directory
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

## Environment Setup
**Python version >= 3.12**

<br>

#### Upgrade tools to avoid common installation issues
```shell
python -m pip install --upgrade pip wheel setuptools
```

<br>

#### Install the environment
```shell
pip install -e .
```
or
```shell
pip install -r requirements.txt
```
###### It is recommended to create a Python virtual environment first
###### First change to the src\ directory, then run:
```shell
python -m venv .venv    # Create a virtual environment

.venv\Scripts\activate  # Activate the virtual environment
```

<br>

#### Run
First change to the src\ directory, then run
```shell
python pyai.py
```
or
```shell
python -m core
```

<br>

#### Configure the API for testing
1. Create a .env file in the src folder
2. Fill in: APIKEY=<your-key> (replace <your-key> with your API-KEY)

**Note: remember to change to the src directory; please install pytest by yourself**

<br>

---

<br>

## Debugging

Some command-line arguments are defined in \_\_init__.py in PyAI\src\core <br>
###### For this kind of debugging, please change to the src\ directory
The following are currently available:

<br>

#### --log-level argument
###### Can also be abbreviated as -l
This argument can change the default log output level without modifying the source code, which is very convenient <br>
There are four values: DEBUG (most detailed), INFO (default), WARNING, ERROR <br>
Listed from most to least detailed
Example:
```shell
python pyai.py --log-level DEBUG  # Enable the lowest log level (most detailed)
```

<br>


> More arguments will be available later


<br>

---

<br>

## Testing
This mainly uses the code under the tests directory <br>
Please set the src\ directory as the working directory before use <br>
Remember to configure .env first before use

### Run tests
```shell
python -m pytest tests
```

<br>

---

<br>

### For more details, please refer to the "User Guide" documentation (directory: PyAI\src\docs)
> Author: 6tft6(6comp) <br>
> Repository: https://github.com/6comp/PyAI <br>
> E-mail: 3950264691@qq.com <br>
> README.md: 6tft6(6comp) <br>
> Program help docs (user): CodeBuddy-DeepSeek <br>
> Thank you for your valuable feedback!

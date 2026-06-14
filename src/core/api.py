# coding=UTF-8

"""
@File: api.py
此模块用于 api 的调用
"""

# 模块导入
import re
import time
import requests
import json
import requests_cache

__all__= {
    'Api'
}



# 获取日志记录器
global logger
def init(get_logger) -> None:
    """
    初始化模块
    :param get_logger: log 模块的 get_logger 方法
    :return: None
    """
    global logger
    logger = get_logger(__name__)


def timeout(times:int) -> type|object:
    """
    超时重试
    :param times: 重试次数
    :return: 函数
    """
    t = int(times)

    def _return(target:type) -> object:
        def method(*args, **kwargs) -> object:
            nonlocal t
            while t > 0:
                try:
                    result = target(*args, **kwargs)
                    return result
                except requests.exceptions.Timeout:
                    logger.warning('Request Timeout')

                except requests.exceptions.ConnectionError:
                    logger.warning('Request ConnectionError')

                time.sleep(1)
                t -= 1
            logger.error('Try failed!')

            return None
        return method
    return _return




class Api:
    """
    API 访问方法封装
    """
    def __init__(self, msg:list, api:str, max_token:int=1024) -> None:
        """
        init
        :param msg: 过去对话记录
        :param api: API 秘钥
        :param max_token: 最大生成 token 数
        """

        self.logger = logger                                            # 日志记录器

        self.url = 'https://api.deepseek.com/chat/completions'          # api 地址
        self.messages = msg                                             # 聊天记录和设定

        # 请求字典
        self.payload:dict = {
            'messages':self.messages,       # 对话记录

            'model':'deepseek-v4-flash',    # 模型名

            'thinking':{'type':'disabled'}, # 是否深度思考（否 disabled 是 enabled）
            #'reasoning_effort':'high',     # 思考深度（浅 high 深 max）

            'max-token':max_token,          # 最大生成 token

            "stop": None,                   # 一个 string 或最多包含 16 个 string 的 list，在遇到这些词时，API 停止生成更多的 token
            "stream": False,                # 是否使用流式输出（是 True 否 False）
            "stream_options": None,         # 流式输出相关选项
            "temperature": 1.1,             # 随机性（0<temperature<=2）
            # "top_p": 1,                   # temperature 的替代方案（不建议一起设置）
            "tools": None,
            "tool_choice": "none",
            "logprobs": False,
            "top_logprobs": None
        }

        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {api}'
        }

        self.logger.debug(api)
        self.logger.debug(max_token)
        self.logger.debug(msg)
        self.logger.info('"api.py" module init complete')


    @ timeout(15)
    def _request(self, payload:str) -> str|None:
        """
        发送请求，返回 ai 的回答
        :param payload: 发送数据
        :return: str
        """
        self.logger.info('Request start...')

        try:
            # 请求
            response = requests.post(self.url, data=payload, headers=self.headers)
            response.encoding = 'UTF-8'
            self.logger.debug(response.status_code)
            self.logger.debug(response.headers)
            self.logger.debug(response.cookies)
            self.logger.debug(response.text)

            # 判断是否成功并返回生成内容
            if response.ok:
                self.logger.info('Requested successfully')
                js = json.loads(response.text)['choices'][0]

                if js['finish_reason'] != 'stop':                       # 判断模型生成是否正常
                    self.logger.error(f'AI answer error {js['finish']}')
                    return None

                ai_answer:str = js['message']['content']
                self.payload['messages'].append(js['message'])          # 添加到聊天记录
                self.logger.debug(ai_answer)

                return ai_answer

            else:
                self.logger.error('Requested failed')

        except requests.exceptions.BaseHTTPError as e:
            self.logger.error(e)

        except requests.exceptions.HTTPError as e:
            self.logger.error(e)

        except Exception as e:
            self.logger.error(e, exc_info=True)

        return None


    def chat(self, say:str) -> str|None:
        """
        发送聊天
        :param say: 说的话
        :return: str|None
        """

        # 处理发送数据
        self.payload['messages'].append({'content':say, 'role':'user'})
        pd = json.dumps(self.payload)

        return self._request(pd)



    @ timeout(15)
    def analysis_dialog(self, **dialog:list[tuple[str,str]]) -> str:
        """
        分析对话内容
        :param dialog: 对话内容
        :return: str
        """
        setting = '''
        你是一个智能聊天分析助手，只能返回分析结果
        格式：json
        示例：
        ```json
        {
            "对话者相关信息":{
                "对话者1名字":{"性别":"男","性格":"活泼，开朗"},
                "对话者2名字":{"性别":"女","性格":"活泼，开朗"}
                },
            "正在进行的对话":{"对话者1":"你好啊","对话者2":"你也好"},
        }
        ```
        注：
            1. 对话者的相关信息可以有很多，比如年龄、爱好、等等，你可以自行添加
            2. "正在进行的对话" 这个 json id 从我上传的对话内容中提取
            3. 我有时会返回你曾生成的分析记录，你可以根据旧内容来进行进一步分析
        ** 必须以标准 json 格式返回 **
        '''
        msg = [{'role':'system','content':setting}]

        ''
# coding=UTF-8

"""
@File: api.py
此模块用于 api 的调用
"""

# 模块导入
import time
import requests
import json
import typing

__all__= [
    'Api'
]



# 获取日志记录器
global api_logger
def init(get_api_logger) -> None:
    """
    初始化模块
    :param get_api_logger: 获取日志记录器的调用方法
    :return: None
    """
    global api_logger
    api_logger = get_api_logger('api')



def timeout(times:int) -> typing.Callable:
    """
    超时重试
    :param times: 重试次数
    :return: 函数
    """
    t = times

    def _return(target:type) -> object:
        def method(*args, **kwargs) -> object:
            nonlocal t
            while t > 0:
                try:
                    result = target(*args, **kwargs)
                    return result
                except requests.exceptions.Timeout:
                    api_logger.warning('Request Timeout')

                except requests.exceptions.ConnectionError:
                    api_logger.warning('Request ConnectionError')

                time.sleep(1)
                t -= 1
            api_logger.error('Try failed!')

            return None
        return method
    return _return




class Api:
    """
    API 访问方法封装
    """
    def __init__(self, max_token:int=2048) -> None:
        """
        init
        :param max_token: 最大生成 token 数
        """

        self.api_logger = api_logger                                            # 日志记录器
        with open('analysis_config', encoding='UTF-8') as f:
            self.ana_setting = f.read().replace('\n', ' ')
        #
        # api_key = self.get_api()
        # if api_key is None:
        #     api_key = 'Not Exists'
        #     self.api_logger.warning('The API-KEY is not exists')
        #     self.show_warn('warning', '提示', '您还未添加模型的 API-KEY\n请在「设置」界面添加 API-KEY')
#         if info:=self.get_info():
#             info = json.loads(info)
#             name = info['对话者相关属性'].keys()
#             about = info['对话者相关属性'].values()
#             ai_setting = \
# f'''
# 名字：{name[0]}
# 相关属性：{about[0]}
# TA的名字：{name[1] if name[1] != 'TA' else '暂时不知道'}
# 相关记忆：{info['相关记忆']}
# '''
#             setting = {'content':ai_setting, 'role':'system'}               # ai 设定
#             self.messages = [{'content':content,'role':'assistant' if n==name[0] else 'user'}
#                          for content, n in info['正在进行的对话']]
#             self.messages.insert(0, setting)
#         else:
#             self.api_logger.warning('Info is not exists')
#             self.messages=[{'content':None, 'role':'system'},]
#         self.api_logger.debug(self.messages)

        self.messages = None
        self.url = 'https://api.deepseek.com/chat/completions'          # api 地址

        # 请求字典
        self.payload:dict = {
            'model':'deepseek-v4-pro',       # 模型名

            'messages':self.messages,       # 对话记录和设定

            'thinking':{'type':'disabled'}, # 是否深度思考（否 disabled 是 enabled）
            'reasoning_effort':'high',      # 思考深度（浅 high 深 max）

            'max_tokens':max_token,         # 最大生成 token

            "stop": None,                   # 一个 string 或最多包含 16 个 string 的 list，在遇到这些词时，API 停止生成更多的 token
            "stream": False,                # 是否使用流式输出（是 True 否 False）
            #"stream_options": None,        # 流式输出相关选项
            "temperature": 0.35,            # 随机性（0<temperature<=2）
            # "top_p": 1,                   # temperature 的替代方案（不建议一起设置）
            #"tools": None,
            #"tool_choice": None,
            # "logprobs": False,
            # "top_logprobs": None
        }

        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': ''
        }

        self.api_logger.debug(max_token)
        # self.api_logger.debug(msg)
        self.api_logger.info('Initiate have done (api)')



    def update_headers(self, key:str, value:str) -> None:
        """
        更改请求头
        :param key: 更改的键名
        :param value: 要更改为的值
        :return: None
        """
        self.headers[key] = value
        self.api_logger.debug(f'Update headers key:{key}, new value:{value}')
        self.api_logger.info('Updating headers ended')



    def update_payload(self, key:str, value:str) -> None:
        """
        更改请求 payload
        :param key: 更改的键名
        :param value: 要更改为的值
        :return: None
        """
        self.payload[key] = value
        self.api_logger.info(f'Update payload key:{key}, new value:{value}')



    def get_messages(self) -> list:
        """
        获取对话消息
        :return: None
        """
        self.api_logger.info('Get message from payload')
        return self.messages



    def add_api(self, api:str) -> None:
        """
        添加 API
        :param api: API-KEY
        :return: None
        """
        self.update_headers('Authorization',f'Bearer {api}')
        self.api_logger.info('Adding ended')



    def add_info(self, info:dict) -> None:
        """
        添加请求相关信息
        :param info: 相关信息 dict
        :return: None
        """
        self.api_logger.debug(info)
        ai_about = info['对话者相关属性']['0']
        ai_name = ai_about['姓名']
        user_about = info['对话者相关属性']['1']
        user_name = user_about['姓名']
        ai_setting = f'''
名字：{ai_name}
相关属性：{ai_about}
TA的名字：{user_name}
TA的属性：{user_about}
相关记忆：{info['相关记忆']}
        '''
        setting = {'content': ai_setting, 'role': 'system'}  # ai 设定
        self.messages = [{'content': content, 'role': 'assistant' if n == user_name else 'user'}
                         for content, n in info['正在进行的对话'].items()]
        self.messages.insert(0, setting)
        self.payload['messages'] = self.messages

        self.api_logger.info('Adding ended')



    @ timeout(15)
    def _request(self, payload:str) -> tuple[str,str]|None:
        """
        发送请求，返回 ai 的回答
        :param payload: 发送数据
        :return: tuple[dict,str]|None
        """

        try:
            # 请求
            response = requests.post(self.url, data=payload, headers=self.headers, timeout=15)
            response.encoding = 'UTF-8'
            self.api_logger.debug(response.status_code)
            self.api_logger.debug(response.headers)
            self.api_logger.debug(response.cookies)
            self.api_logger.debug(response.text)

            # 判断是否成功并返回生成内容
            if response.ok:
                self.api_logger.info('Requested successfully')
                js = json.loads(response.text)['choices'][0]
                response_time = time.strftime('%Y.%m.%d-%H:%M:%S(%A)', time.localtime())

                if js['finish_reason'] != 'stop':                       # 判断模型生成是否正常
                    self.api_logger.error(f'AI answer error {js['finish_reason']}')
                    return None

                return js['message']['content'], response_time

            else:
                self.api_logger.error('Request Failed!')

        except requests.exceptions.HTTPError as e:
            self.api_logger.error(f'Request Failed! {e}')

        except Exception as e:
            self.api_logger.error(e, exc_info=True)

        finally:
            self.api_logger.info('Request ended')

        return None



    def chat(self, say:str) -> tuple[str,str]|None:
        """
        发送聊天，返回生成结果和时间
        :param say: 说的话
        :return: tuple[str,str]|None
        """
        if self.messages:
            self.messages.append({'content': say, 'role': 'user'})
            if self.headers['Authorization']:                                   # 判断是否配置了 API-KEY
                if self.messages[0]['content']:
                    pd = json.dumps(self.payload, ensure_ascii=False)           # 处理发送数据
                    self.api_logger.debug(pd)
                    result = self._request(pd)
                    if result:
                        answer, date = result
                        self.messages.append({'content':answer, 'role':'assistant'})
                        return answer, date
                    self.api_logger.error('Response Failed!')
                else:
                    self.api_logger.warning('Info is not exists')
            else:
                self.api_logger.warning('API-KEY is Not Exists')
            del self.messages[-1]
        else:
            self.api_logger.warning('Message have not added system content')

        self.api_logger.info('Chat ended')
        return None



    def analysis_dialog(self, *dialogs:tuple[str,str, str], history:str|None=None) -> tuple[str,str]|None:
        """
        分析对话内容，返回分析数据
        :param dialogs: 对话内容 (user,ai,date),(user,ai,date)
        :param history: 历史记录
        :return: str
        """
        self.payload['messages'] = [{'role':'system','content':self.ana_setting},
                                    {'role':'user', 'content':(f"对话记录：\n{'\n'.join([f'User:{user} | AI:{ai} | Date:{date}' for user,ai,date in dialogs])}\n"
                                                               f"历史生成：\n{history if history else '无'}")}]
        self.api_logger.debug(self.payload)
        pd = json.dumps(self.payload, ensure_ascii=False)
        analysis = self._request(pd)
        self.api_logger.debug(analysis)
        self.payload['messages'] = self.messages

        if analysis:
            analysis[0].removeprefix('```json').removesuffix('```')
            return analysis

        self.api_logger.debug('No')
        self.api_logger.info('Analysis dialogs ended')
        return None
# coding=UTF-8

"""
@file: datamanage.py
"""

# 模块导入
import time
import base64
import sqlite3
import secrets
import keyring
import typing as tp
from cryptography.hazmat.primitives import ciphers
from cryptography.hazmat.primitives.ciphers import algorithms, modes


__all__ = [
    'DataManager',
    'init'
]


NAME = 'PyAI'           # 程序名
AES_API = 'API-KEY'     # 系统密钥存储分区(api)



# 获取日志记录器
global data_logger
def init(get_logger) -> None:
    """
    初始化模块
    :param get_logger: 获取记录器调用方法
    :return: None
    """
    global data_logger
    data_logger = get_logger('datamanage')




def insert_time(target:tp.Callable) -> tp.Callable:
    """
    输入时间（需要含有 t 参数）
    :param target: 调用对象
    :return: tp.Callable
    """
    def _return(*args, **kwargs):
        t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        data_logger.debug(f'Use insert time {target} time {t}')
        return target(*args, **kwargs, _t=t)

    return _return



class DataManager:
    """
    数据管理的封装
    """

    @ insert_time
    def __init__(self, _t:None=None) -> None:
        """
        Initiate data manager
        """
        self.db_paths:dict[str,str] = self.config['db_config']['path']


        runtime = _t
        self.data_logger = data_logger
        self.data_logger.debug(self.config)
        dbs_name = ('dialog', 'system', 'setting')

        # 初始化数据库
        sqls = (
            # dialogs DB
                r'''
                    CREATE TABLE info (
                                        id INTEGER PRIMARY KEY,
                                        info TEXT,
                                        "date" DATE);
                    CREATE TABLE dialogs (
                                          id INTEGER PRIMARY KEY,
                                          ai TEXT,
                                          user TEXT,
                                          "date" DATE);
                ''',
            # system DB
                r'''
                    CREATE TABLE runtime (
                                          "key" TEXT, 
                                          "value" TEXT,
                                          "date" TEXT);
                    CREATE TABLE setting (
                                         id INTEGER PRIMARY KEY,
                                         name TEXT,
                                         "value" TEXT);
                ''',
            # setting DB
                r'''
                    CREATE TABLE setting (
                                          id INTEGER PRIMARY KEY,
                                          name TEXT,
                                          "value" TEXT);
                    CREATE TABLE secret (
                                         "key" TEXT PRIMARY KEY,
                                         "value" TEXT);
                ''')
        creator = dict(zip(dbs_name, sqls))

        sqls = (
            '',

            f'''
            INSERT INTO runtime ("key", "value", "date") VALUES ('runtime','{runtime}','{runtime}');
            ''',

            ''
        )
        initializer = dict(zip(dbs_name, sqls))

        # sqls = (
        #     'SELECT ai, user FROM info WHERE id=0;',
        #     'SELECT name, "value" FROM config',
        #     'SELECT name, "value" FROM setting',
        # )
        # selector = dict(zip(dbs_name, sqls))

        # self.db_data = {}                                                               #保存所有从数据库中获取的数据
        for name,db in self.db_paths.items():
            self.data_logger.debug(name)

            with sqlite3.connect(db) as connection:
                cursor = connection.cursor()

                all_table = cursor.execute('SELECT * FROM sqlite_master').fetchall()    # 获取所有表信息
                self.data_logger.debug(all_table)
                if not all_table:
                    self.data_logger.debug('No table and now going to create')
                    cursor.executescript(creator[name])                                 # 使用创建的 SQL 代码

                # 初始化进行的 SQL 代码
                cursor.executescript(initializer[name])

                # # 查询运行所需的数据
                # data = cursor.execute(selector[name]).fetchall()
                # self.data_logger.debug(data)
                # self.db_data[name] = data

        # self.data_logger.debug(self.db_data)
        self.data_logger.info('Initiate have done (DataManage)')



    def save_dialogs(self, *dialogs:tuple[str,str,str]) -> None:
        """
        保存聊天记录
        :param dialogs: 聊天记录(ai,user,date),(ai,user,date)
        :return: bool|None
        """
        self.data_logger.debug(dialogs)

        with sqlite3.connect(self.db_paths['dialog']) as connection:
            cursor = connection.cursor()
            index = cursor.execute('SELECT id FROM dialogs').fetchall()
            end_index = index[-1][0] if index else 0                                        # 获取尾索引
            self.data_logger.debug(end_index)
            indexes = range(end_index+1, len(dialogs)+end_index+2)                          # 计算出所有对话记录的索引
            dialogs = [(i,*d) for i,d in zip(indexes, dialogs)]
            self.data_logger.debug(dialogs)
            sql = 'INSERT INTO dialogs (id, ai, user, "date") VALUES (?,?,?,?)'
            cursor.executemany(sql,dialogs)
            connection.commit()

        self.data_logger.info('Save dialogs into the named "dialogs" table')



    def get_dialogs(self) -> tp.Generator|None:
        """
        获取聊天记录（生成器）
        :return: tuple[str,str,str]
        """
        self.data_logger.info('Start to get dialogs')

        with sqlite3.connect(self.db_paths['dialog']) as connection:
            cursor = connection.cursor()
            result = cursor.execute('SELECT id FROM dialogs').fetchall()
            self.data_logger.debug(result)
            if result:
                self.data_logger.debug('Dialogs exists')
                end_index = result[-1][0]
                for index in range(end_index, 0, -1):               # 反向生成 id 索引
                    dialog = cursor.execute('SELECT ai,user,date FROM dialogs WHERE id=?',(index,)).fetchone()
                    self.data_logger.debug(dialog)
                    yield dialog

        self.data_logger.info('Get dialogs ended')
        return None

        # 废弃方案
        # with sqlite3.connect(self.db_paths['dialog']) as connection:
        #     cursor = connection.cursor()
        #     if start_date:
        #         restriction1 = 'id>?'
        #     else:
        #         restriction1 = ''
        #     cursor.execute(f'SELECT ai,user FROM dialogs WHERE {} {}', ())



    @ insert_time
    def save_info(self, info:str, _t:None=None) -> None:
        """
        保存人物相关信息
        :param info: 插入的内容
        :param _t: 时间（无需输入）
        :return: None
        """
        self.data_logger.debug(f'Info:{info} | Time:{_t}')

        with sqlite3.connect(self.db_paths['dialog']) as connection:
            cursor = connection.cursor()
            index = cursor.execute(f'SELECT id FROM info').fetchall()
            self.data_logger.debug(index)
            index = index[-1][0] + 1 if index else 0                     # 计算出最后一个索引
            self.data_logger.debug(index)
            info = base64.b64encode(info.encode('UTF-8')).decode('UTF-8')
            cursor.execute(rf'INSERT INTO info VALUES (?,?,?)', (index, info, _t))
            connection.commit()

        self.data_logger.info('Insert ended')



    def get_info(self, data_index:int|None=None) -> str|None:
        """
        获取相关信息
        :param data_index: 获取相关信息时的索引（不指定则为最近的相关信息）
        :return: str
        """
        self.data_logger.debug(f'Index:{data_index}')

        with sqlite3.connect(self.db_paths['dialog']) as connection:
            cursor = connection.cursor()
            if not data_index:
                index = cursor.execute(r'SELECT id FROM info').fetchall()
                self.data_logger.debug(index)
                if index:
                    end_index = index[-1][0]                            # 获取尾索引
                    self.data_logger.debug(end_index)
                else:
                    self.data_logger.warning('User has not saved any related data')
                    return None
            else:
                end_index = data_index
            cursor.execute('SELECT info FROM info WHERE id=?', (end_index,))
            data = cursor.fetchone()[0]
            data = base64.b64decode(data.encode('UTF-8')).decode('UTF-8')
            self.data_logger.debug(data)

            self.data_logger.info('Get info ended')
            return data




    @insert_time
    def set_api(self, api_key:str, _t:None=None) -> None:
        """
        保存或设置 API 密钥
        :param api_key: 设置数据
        :param _t: 时间（无需设置）
        :return:
        """
        self.data_logger.debug(api_key)
        all_ = self._get_aeskey()
        if all_ is None:
            self.data_logger.warning('AES-KEY Error! You can\'t to set api')
            return
        aes_key, iv = all_

        with sqlite3.connect(self.db_paths['setting']) as connection:
            cursor = connection.cursor()
            aes256 = algorithms.AES256(aes_key)                         # 密钥对象
            mode = modes.GCM(iv)                                        # 加密模式对象
            cipher = ciphers.Cipher(aes256, mode)                # 获取加密对象
            encryptor = cipher.encryptor()
            secret_data = encryptor.update(api_key.encode('UTF-8')) + encryptor.finalize() #  加密并获取密文
            secret_data = base64.b64encode(secret_data).decode('UTF-8') # base64 编码便于存储
            tag = encryptor.tag                                         # 获取校验码标签
            tag = base64.b64encode(tag).decode('UTF-8')                 # 转换为 base64 编码
            self.data_logger.debug(f'check-codes:{tag} | secret-data:{secret_data}')

            # 存储密文及校验码
            select_sql = 'SELECT "value" FROM secret WHERE "key"=?'
            update_sql = 'UPDATE secret SET "value"=? WHERE "key"=?'
            insert_sql = 'INSERT INTO secret ("value","key") VALUES (?,?)'
            old_data = cursor.execute(select_sql, ('API-KEY',)).fetchone()
            self.data_logger.debug(old_data)
            cursor.execute(update_sql if old_data else insert_sql, (secret_data, 'API-KEY'))
            old_tag = cursor.execute(select_sql, ('API-TAG',)).fetchone()
            self.data_logger.debug(old_tag)
            cursor.execute(update_sql if old_tag else insert_sql, (tag, 'API-TAG'))
            connection.commit()

        self.data_logger.info('Save and encrypted the api')



    def _get_aeskey(self) -> tuple[bytes, bytes]|None:
        """
        获取 AES 加密密钥
        :return: tuple[bytes, bytes]
        """
        key = keyring.get_password(NAME, AES_API)                # 从系统秘钥管理库获取 AES-KEY
        self.data_logger.debug(key)

        if key is None:
            self.data_logger.debug('API key not exist')
            aes_key = secrets.token_bytes(32)                   # 创建密钥
            iv = secrets.token_bytes(16)                        # 创建初始随机 IV
            self.data_logger.debug(f'BYTES: {aes_key} | {iv}')
            with sqlite3.connect(self.db_paths['setting']) as connection:
                cursor = connection.cursor()
                base_iv = base64.b64encode(iv).decode('UTF-8')
                cursor.execute('INSERT INTO secret VALUES (?,?)', ('API-IV', base_iv))
                connection.commit()
            key = base64.b64encode(aes_key).decode('UTF-8')     # 将 bytes 版密钥解码为字符
            keyring.set_password(NAME, AES_API, key)
        else:
            self.data_logger.debug('API key exist')
            aes_key = base64.b64decode(key.encode('UTF-8'))     # 将字符版的密钥转为 bytes
            self.data_logger.debug(aes_key)
            with sqlite3.connect(self.db_paths['setting']) as connection:
                cursor = connection.cursor()
                data = cursor.execute('SELECT "value" FROM secret WHERE "key"=?', ('API-IV',)).fetchone()
                self.data_logger.debug(data)
                if data is None:                                # 判断 IV 是否存在
                    self.destroyed('secret')
                    self.data_logger.warning('API-IV key not exist and now return empty data')
                    return None
                iv_str:str = data[0]
                self.data_logger.debug(iv_str)
            iv:bytes = base64.b64decode(iv_str.encode('UTF-8'))

        self.data_logger.debug(f'AES-KEY:{aes_key} | IV:{iv}')
        self.data_logger.info('Got the AES-KEY and IV')
        return aes_key,iv



    def get_api(self) -> str|None:
        """
        获取保存的 api 秘钥，若没有保存则返回空
        :return: str|None
        """
        # 获取密文和密钥
        with sqlite3.connect(self.db_paths['setting']) as connection:
            cursor = connection.cursor()
            data = cursor.execute('SELECT "key","value" FROM secret WHERE "key" IN (?,?,?)',('API-KEY','API-IV','API-TAG')).fetchall()
            self.data_logger.debug(data)
            if not data:
                self.data_logger.warning('Secret data is not exist')
                return None
            base_data = dict(data)
        api_secret:bytes = base64.b64decode(base_data['API-KEY'].encode('UTF-8'))
        iv:bytes = base64.b64decode(base_data['API-IV'].encode('UTF-8'))
        tag:bytes = base64.b64decode(base_data['API-TAG'].encode('UTF-8'))

        # 解密
        aes_key = keyring.get_password(NAME, AES_API)
        self.data_logger.debug(aes_key)
        if aes_key is None:
            self.data_logger.warning('API-KEY not exist')
            return None
        aes_key = base64.b64decode(aes_key.encode('UTF-8'))
        aes256 = algorithms.AES256(aes_key)
        mode = modes.GCM(iv, tag)
        cipher = ciphers.Cipher(aes256, mode)
        decryptor = cipher.decryptor()
        api = decryptor.update(api_secret) + decryptor.finalize()
        self.data_logger.debug(api)

        return api.decode('UTF-8')



    def update_setting(self, key:str, value:str, system:bool=False) -> None:
        """
        更新设置
        :param key: 设置的项名
        :param value: 设置的内容
        :param system: 是否是系统类型
        :return: None
        """
        with sqlite3.connect(self.db_paths['system' if system else 'setting']) as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT name FROM setting WHERE name=?',(key,))
            if cursor.fetchone():
                cursor.execute('UPDATE setting SET "value"=? WHERE name=?',(value,key))
            else:
                cursor.execute('SELECT id FROM setting')
                index = cursor.fetchall()
                index = index[-1][0]+1 if index else 0
                cursor.execute('INSERT INTO setting(id,name,"value") VALUES (?,?,?)',(index, key, value))
        self.data_logger.info('Setting ended')



    def get_setting(self, key:str, system:bool=False) -> str|None:
        """
        获取设置
        :param key: 设置名
        :param system: 是否是系统类型
        :return: str
        """
        with sqlite3.connect(self.db_paths['system' if system else 'setting']) as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT "value" FROM setting WHERE name=?',(key,))
            if data:=cursor.fetchone():
                self.data_logger.debug(data)
                return data[0]

        self.data_logger.warning('The setting is not exists')
        self.data_logger.info('Got ended')
        return None



    def _destroyed_secret(self) -> None:
        """
        销毁私密数据
        :return: None
        """
        if not (k := keyring.get_password(NAME, AES_API)):
            self.data_logger.debug(k)
            self.data_logger.warning('API-KEY not exist')
            return
        keyring.delete_password(NAME, AES_API)                          # 删除秘钥
        self.data_logger.debug('Deleted API-KEY')

        with sqlite3.connect(self.db_paths['setting']) as connection:
            cursor = connection.cursor()
            cursor.execute('DELETE FROM secret')                        # 删除 iv 和密文
            self.data_logger.debug('Deleted IV and secret data')

        self.data_logger.info('Destroyed the secret')



    def _destroyed_dialogs(self) -> None:
        """
        销毁聊天记录及收集设定
        :return: None
        """
        with sqlite3.connect(self.db_paths['dialog']) as connection:
            cursor = connection.cursor()
            cursor.execute('DELETE FROM info')
            cursor.execute('DELETE FROM dialogs')
            connection.commit()

        self.data_logger.info('Destroyed the dialogs')



    def _destroyed_settings(self) -> None:
        """
        删除系统设定及 runtime
        :return: None
        """
        with sqlite3.connect(self.db_paths['setting']) as connection:
            cursor = connection.cursor()
            cursor.execute('DELETE FROM setting')
            cursor.execute('DELETE FROM runtime')

        self.data_logger.info('Destroyed the settings')



    def destroyed(self, _type:tp.Literal['secret','dialogs','system','all']) -> None:
        """
        销毁数据
        :param _type: 销毁的数据类型
        :return: None
        """
        self.data_logger.debug(_type)
        methods = {'secret':self._destroyed_secret,
                   'dialogs':self._destroyed_dialogs,
                   'system':self._destroyed_settings}
        if _type != 'all':
            methods[_type]()
            return
        for method in methods.values():
            method()

        self.data_logger.info(f'Destroyed the {_type}')
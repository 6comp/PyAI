# coding=UTF-8

"""
@file: ui.py
"""

# 导入
# import gc
import json
import os.path
import webbrowser
import typing as tp
import tkinter as tk
from tkinter import messagebox, scrolledtext


__all__ = ['Ui']


# gc.disable()

global logger
def init(get_logger) -> None:
    """
    初始化模块
    :param get_logger: 获取记录器调用方法
    :return: None
    """
    global logger
    logger = get_logger(__name__)



class Ui:
    """
    UI 功能的实现
    """
    with open('config.json') as f:
        config = json.load(f)['ui_config']
        language = config['language']
        text_language = config['text_language'][language]
        color_mode = config['colors']['mode']
        colors = config['colors'][color_mode]




    def __init__(self, **kwargs:dict[str,tp.Callable]) -> None:
        """
        Initiate UI
        """
        self.logger = logger
        self.img_cache = {}
        self.commands = kwargs

        self.main_tk = None
        self.pages = {}



    def build_ui(self) -> None:
        """
        搭建 UI 界面
        :return: None
        """

        self.main_tk = tk.Tk('PyAI', 'PyAI-UI')
        self.main_tk.title('PyAI')
        self.main_tk.iconbitmap('img\\PyAIICO.ico')
        x = (self.main_tk.winfo_screenwidth()-800) // 2
        y = (self.main_tk.winfo_screenheight()-550) // 2
        self.main_tk.geometry(f'800x550+{x}+{y}')
        self.main_tk.resizable(False, False)

        self._build_home()

        self.main_tk.mainloop()




    def _build_home(self) -> None:
        """
        搭建主页面
        :return: None
        """

        colors = self.colors['home']                        # 获取颜色配置
        commands = self.commands['home']                    # 获取命令方法

        # 搭建主页面容器
        home = tk.Frame(self.main_tk,
                        name='home',
                        bg=colors['bg'],
                        highlightcolor=colors['highlightcolor'],
                        highlightbackground=colors['highlightbackground'],
                        highlightthickness=0.1,
                        relief='flat')
        home.pack(fill='both')
        self.pages['home'] = home


        # 搭建控件
        colors_frame:dict = colors['config_frame']

        # 配置区域
        config_frame = tk.Frame(home,
                                name='config_frame',
                                bg=colors_frame['bg'],
                                highlightcolor=colors_frame['highlightcolor'],
                                highlightbackground=colors_frame['highlightbackground'],
                                highlightthickness=0.1,
                                relief='flat')
        config_frame.pack(side='left', fill='y')

        # 搭建按钮
        colors_c = (*colors_frame,)[3:]
        texts = ('关于', '帮助', '设置', '伴侣配置')
        names = ('about', 'help', 'setting', 'character_setting')
        pdx = (25,0,0,0)
        cmd = (self._built_about, self._built_help, self._built_setting, self._built_character_settings)
        for color, text, name, pdx, cmd in zip(colors_c, texts, names, pdx, cmd):
            color = colors_frame[color]
            button = tk.Button(config_frame,
                               name=name,
                               text=text,
                               activebackground=color['activebackground'],
                               activeforeground=color['activeforeground'],
                               bg=color['bg'],
                               bd=0.7,
                               relief='solid',
                               font=('微软雅黑', 11),
                               padx=13,
                               pady=1,
                               command=cmd)
            button.pack(pady=(20,0), padx=pdx)

        # 对话区
        colors_frame = colors['chat_frame']
        chat_frame = tk.Frame(home,
                              name='chat_frame',
                              bg=colors_frame['bg'],
                              highlightcolor=colors_frame['highlightcolor'],
                              highlightbackground=colors_frame['highlightbackground'],
                              highlightthickness=0.1,
                              relief='flat')
        chat_frame.pack(side='left', fill='both')

        # 动作按钮区
        action_color = colors_frame['action_frame']
        action_frame = tk.Frame(chat_frame,
                              name='chat_action_frame',
                              bg=action_color['bg'],
                              highlightcolor=action_color['highlightcolor'],
                              highlightbackground=action_color['highlightbackground'],
                              highlightthickness=0.1,
                              relief='flat')
        action_frame.pack(fill='x')

        h_t_b_color = action_color['head_touch_button']
        head_touch_button = tk.Button(action_frame,
                                      name='head_touch_button',
                                      text='摸摸头',
                                      activebackground=h_t_b_color['activebackground'],
                                      activeforeground=h_t_b_color['activeforeground'],
                                      bg=h_t_b_color['bg'],
                                      bd=0.5,
                                      relief='solid',
                                      font=('微软雅黑', 10),
                                      padx=15,
                                      pady=2,
                                      command=lambda :commands['chat'](text='（摸摸头）', control=text))
        head_touch_button.pack(side='left', anchor='n', pady=(20,0), padx=(20,0))

        hug_color = action_color['hug_button']
        hug_button = tk.Button(action_frame,
                                  name='hug_button',
                                  text='抱一抱',
                                  activebackground=hug_color['activebackground'],
                                  activeforeground=hug_color['activeforeground'],
                                  bg=hug_color['bg'],
                                  bd=0.5,
                                  relief='solid',
                                  font=('微软雅黑', 10),
                                  padx=15,
                                  pady=2,
                                  command=lambda :commands['chat'](text='（抱一抱）', control=text))
        hug_button.pack(side='left', anchor='n', pady=(20,0), padx=(20,0))

        text_color = colors_frame['chat_text']
        text = scrolledtext.ScrolledText(chat_frame,
                                         wrap='none',
                                         bg=text_color['bg'],
                                         state='disabled',
                                         font=('微软雅黑',11),
                                         fg=text_color['fg'],
                                         selectbackground=text_color['selectbackground'],
                                         relief='flat',
                                         width=71,
                                         height=18,
                                         padx=7,
                                         pady=2)
        text.pack(pady=(23,0), padx=10)

        insert_color = colors_frame['insert_frame']
        insert_frame = tk.Frame(chat_frame,
                                name='chat_insert_frame',
                                bg=insert_color['bg'],
                                highlightcolor=insert_color['highlightcolor'],
                                highlightbackground=insert_color['highlightbackground'],
                                highlightthickness=0.1,
                                relief='flat')
        insert_frame.pack(pady=(20,60), fill='x')

        entry_color = insert_color['insert_entry']
        insert_entry = tk.Entry(insert_frame,
                                bg=entry_color['bg'],
                                font=('微软雅黑',12),
                                disabledbackground=entry_color['disabledbackground'],
                                highlightcolor=entry_color['highlightcolor'],
                                highlightbackground=entry_color['highlightbackground'],
                                relief='solid',
                                width=62)
        insert_entry.pack(side='left', padx=(20,0))

        send_color = insert_color['send_button']
        send_button = tk.Button(insert_frame,
                                  name='send_button',
                                  text='发送',
                                  activebackground=send_color['activebackground'],
                                  activeforeground=send_color['activeforeground'],
                                  bg=send_color['bg'],
                                  bd=0.5,
                                  relief='solid',
                                  font=('微软雅黑', 10),
                                  padx=15,
                                  pady=2,
                                  command=lambda :commands['chat'](text=insert_entry.get(), control=text))
        send_button.pack(side='left', padx=(13,0))
        chat_frame.bind_all('<Return>', lambda e:commands['chat'](text=insert_entry.get(), control=text))


        self.logger.info('Build the home page')



    def _back(self, forget_control:tk.Frame, pack_control:tk.Frame,
              pack_args:list|tuple|None=None, pack_kwargs:dict|None=None):
        """
        返回键
        :param forget_control: 要隐藏的控件
        :param pack_control: 要复原的控件
        :return: None
        """
        forget_control.pack_forget()
        pack_control.pack(*pack_args if pack_args else (),**pack_kwargs if pack_kwargs else {})
        self.logger.info('Return to previous page')



    def _built_setting(self) -> None:
        """
        搭建设置界面
        :return: None
        """
        self.pages['setting'].forget()

        colors = self.colors['setting']
        setting = tk.Frame(self.main_tk,
                           name='about',
                           bg=colors['bg'],
                           highlightcolor=colors['highlightcolor'],
                           highlightbackground=colors['highlightbackground'],
                           highlightthickness=0.1)
        setting.pack(fill='both')
        self.pages['setting'] = setting

        back_color = colors['back_button']
        back_button = tk.Button(setting,
                                name='back_button',
                                text='返回',
                                activebackground=back_color['activebackground'],
                                activeforeground=back_color['activeforeground'],
                                bg=back_color['bg'],
                                bd=0.5,
                                relief='solid',
                                font=('微软雅黑', 10),
                                padx=15,
                                pady=2,
                                command=lambda :self._back(setting, self.pages['home'], pack_kwargs={'fill':'both'}))
        back_button.pack(side='left', anchor='n', pady=(20,0), padx=(20,0))

        setting_frame = tk.Frame(setting,
                                 name='about',
                                 bg=colors['bg'],
                                 highlightcolor=colors['highlightcolor'],
                                 highlightbackground=colors['highlightbackground'],
                                 highlightthickness=0.1)
        setting_frame.pack(fill='both')

        api_l = tk.Label(setting_frame,)




    def _built_about(self) -> None:
        """
        搭建关于页面 GUI
        :return: None
        """
        self.pages['home'].forget()

        colors = self.colors['about']
        about = tk.Frame(self.main_tk,
                         name='about',
                         bg=colors['bg'],
                         highlightcolor=colors['highlightcolor'],
                         highlightbackground=colors['highlightbackground'],
                         highlightthickness=0.1)
        about.pack(fill='both')
        self.pages['about'] = about

        image = tk.PhotoImage(file=r'img\PyAI-IMG(black)(normal).png')
        self.img_cache['image-about'] = image
        show_img = tk.Label(about,image=image)
        show_img.place(x=0,y=0)

        back_color = colors['back_button']
        back_button = tk.Button(about,
                                name='back_button',
                                text='返回',
                                activebackground=back_color['activebackground'],
                                activeforeground=back_color['activeforeground'],
                                bg=back_color['bg'],
                                bd=0.5,
                                relief='solid',
                                font=('微软雅黑', 10),
                                padx=15,
                                pady=2,
                                command=lambda :self._back(about, self.pages['home'], pack_kwargs={'fill':'both'}))
        back_button.pack(side='left', anchor='n', pady=(20,0), padx=(15,0))


        about_text = """PyAI
一个基于 DeepSeek 大模型实现的 AI 伴侣
希望能给予你温暖和陪伴
    		        













作者：6comp, 6tft6
邮箱：3950264691@qq.com"""
        text = tk.Label(about,
                        name='about_text',
                        text=about_text,
                        font=('微软雅黑',13),
                        bg=colors['bg'],
                        highlightcolor=colors['highlightcolor'],
                        highlightbackground=colors['highlightbackground'],
                        highlightthickness=0.1,
                        width=60,
                        height=20,
                        relief='solid',
                        fg=colors['fg'],
                        bd=0.5)
        text.pack(side='top', anchor='w', pady=(30,60), padx=20)
        text.config(state='disabled')

        self.logger.info('Build the about page')



    def _built_help(self) -> None:
        """
        打开帮助方法
        :return: None
        """
        path = os.path.abspath(r'docs\HelpIndex.html')
        webbrowser.open_new_tab(f'file:///{path}')
        self.logger.info('Open the "HelpIndex.html" helpfile to help user to get help')



    def _built_character_settings(self) -> None:...
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
from tkinter import messagebox, scrolledtext, ttk


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




    def __init__(self, **kwargs:tp.Callable) -> None:
        """
        Initiate UI
        """
        self.logger = logger
        self.cache = {}
        self.commands = kwargs

        self.main_tk = None
        self.title_block = None
        self.style = None
        self.pages = {}



    def ttk_style(self, *args, **kwargs) -> None:
        """
        刷新 ttk 小组件风格配置
        :return: None
        """
        self.logger.debug(args, kwargs)
        self.style.configure(*args, **kwargs)
        self.logger.info('Update ttk style')



    def show_warn(self, level:tp.Literal['warning','error','info','question'],
                  title:str, message:str) -> str|bool:
        """
        弹出提示框
        :param level: 提示类型
        :param title: 标题
        :param message: 文本
        :return: None
        """
        show = {'warning':messagebox.showwarning,
                'error':messagebox.showerror,
                'info':messagebox.showinfo,
                'question':messagebox.askokcancel}
        return show[level](parent=self.main_tk, title=title,message=message)



    def _change_title_block(self, mode:tp.Literal['light','dark']='light') -> None:
        """
        改变标题栏颜色（此功能暂定，将来会实现）
        颜色模式：
        light - 白天模式
        dark - 黑夜模式（暂定）
        :param mode: 颜色模式
        :return: None
        """
        ...



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
        #self.main_tk.resizable(False, False)

        self.style = ttk.Style()

        self._build_home()

        self.main_tk.mainloop()



    def _build_home(self) -> None:
        """
        搭建主页面
        :return: None
        """

        colors = self.colors['home']                        # 获取颜色配置
        commands = self.commands                            # 获取命令方法

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
                                # buttondownrelief='solid',
                                # buttonuprelief='solid',
                                bd=0.5,
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
              pack_args:list|tuple|None=None, pack_kwargs:dict|None=None,
              func:tp.Callable|None=None):
        """
        返回键
        :param forget_control: 要隐藏的控件
        :param pack_control: 要复原的控件
        :param pack_args: 要填入复原方法的参数元组
        :param pack_kwargs: 要填入复原方法的参数字典
        :param func: 钩子函数配置
        :return: None
        """
        if func: func()
        forget_control.pack_forget()
        pack_control.pack(*pack_args if pack_args else (),**pack_kwargs if pack_kwargs else {})
        self.logger.info('Return to previous page')



    def _built_setting(self) -> None:
        """
        搭建设置界面
        :return: None
        """
        self.pages['home'].forget()

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
        def save() -> None:
            """
            保存或更新设置数据
            :return: None
            """
            get_api = api_e.get()
            self.logger.debug(f'{get_api} | {old_api}')
            if get_api != old_api:
                self.logger.debug('Updating api')
                self.commands['set_api'](get_api)
                # get_mode = var.get()
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
                                command=lambda :self._back(setting,
                                                           self.pages['home'], pack_kwargs={'fill':'both'},
                                                           func=save)
                                )
        back_button.pack(anchor='w', pady=(20,0), padx=(20,0))

        setting_frame = tk.LabelFrame(setting,
                                      name='setting_frame_settings',
                                      text='  设置  ',
                                      font=('微软雅黑',12),
                                      bg=colors['bg'],
                                      highlightcolor=colors['highlightcolor'],
                                      highlightbackground=colors['highlightbackground'],
                                      highlightthickness=0.1)
        setting_frame.pack(fill='both', pady=(20,350), padx=20)

        api_frame = tk.Frame(setting_frame,
                             name='api_frame',
                             bg=colors['bg'])
        api_frame.pack(pady=(25,0), fill='x', side='top')

        api_l_color = colors['api_label']
        api_l = tk.Label(api_frame,
                         name='api_label',
                         text='API',
                         font=('微软雅黑',13),
                         bg=api_l_color['bg'],
                         highlightcolor=api_l_color['highlightcolor'],
                         highlightbackground=api_l_color['highlightbackground'],
                         highlightthickness=0.1,
                         fg=api_l_color['fg'],
                         bd=0.5)
        api_l.pack(side='left', anchor='n', padx=(20,0))

        api_e_color = colors['api_entry']
        api = self.commands['get_api']()
        api_e = tk.Entry(api_frame,
                         bg=api_e_color['bg'],
                         font=('微软雅黑',12),
                         highlightcolor=api_e_color['highlightcolor'],
                         highlightbackground=api_e_color['highlightbackground'],
                         relief='solid',
                         width=50)
        api_e.pack(side='left', padx=(20,0))
        api_e.insert(0, api)
        old_api = api_e.get()

        mode_frame = tk.Frame(setting_frame,
                              name='mode_frame',
                              bg=colors['bg'])
        mode_frame.pack(pady=(25,0), fill='x', side='top')

        mode_l_color = colors['mode_label']
        mode_label = tk.Label(mode_frame,
                              name='mode_label',
                              text='昼夜模式（暂定）',
                              font=('微软雅黑',13),
                              bg=mode_l_color['bg'],
                              highlightcolor=mode_l_color['highlightcolor'],
                              highlightbackground=mode_l_color['highlightbackground'],
                              highlightthickness=0.1,
                              fg=mode_l_color['fg'],
                              bd=0.5)
        mode_label.pack(side='left', anchor='n', padx=(20,0))

        mode_color = colors['mode_radiobutton']
        if 'mode-var' in self.cache:
            var = self.cache['mode-var']
        else:
            var = tk.StringVar(mode_frame, 'light')
            self.cache['mode-var'] = var
        self.ttk_style('TRadiobutton', background=mode_color['bg'], font=('微软雅黑',12))
        mode_light = ttk.Radiobutton(mode_frame,
                                    name='mode_light',
                                    #bg=mode_color['bg'],
                                    #activebackground=mode_color['activebackground'],
                                    #activeforeground=mode_color['activeforeground'],
                                    text='白昼',
                                    #font=('微软雅黑',12),
                                    variable=var,
                                    value='light')
        mode_light.pack(side='left', padx=(30,0))

        mode_dark = ttk.Radiobutton(mode_frame,
                                   name='mode_dark',
                                   #bg=mode_color['bg'],
                                   #activebackground=mode_color['activebackground'],
                                   #activeforeground=mode_color['activeforeground'],
                                   text='黑夜',
                                   #font=('微软雅黑',12),
                                   variable=var,
                                   value='dark')
        mode_dark.pack(side='left', padx=(20,0))
        old_mode = var.get()



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

        if 'image-about' in self.cache:
            image = self.cache['image-about']
            self.logger.debug('Get image cache "image-about"')
        else:
            image = tk.PhotoImage(file=r'img\PyAI-IMG(black)(normal).png')
            self.cache['image-about'] = image
        show_img = tk.Label(about,image=image, bg=colors['bg'])
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
        back_button.pack(side='left', anchor='n', pady=(20,0), padx=(18,0))


        about_text = """PyAI
一个基于 DeepSeek 大模型实现的 AI 伴侣
希望能给予你温暖和陪伴














作者：6comp, 6tft6
邮箱：3950264691@qq.com"""
        text_color = colors['text_label']
        text = tk.Label(about,
                        name='about_text',
                        text=about_text,
                        font=('微软雅黑',13),
                        bg=text_color['bg'],
                        highlightcolor=text_color['highlightcolor'],
                        highlightbackground=text_color['highlightbackground'],
                        highlightthickness=0.1,
                        width=60,
                        height=20,
                        relief='solid',
                        fg=text_color['fg'],
                        bd=0.5)
        text.pack(side='top', anchor='w', pady=(30,60), padx=(18,0))
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



    def _built_character_settings(self) -> None:
        """
        打开伴侣配置方法
        :return: None
        """
        self.pages['home'].forget()

        colors = self.colors['character_settings']
        character_settings = tk.Frame(self.main_tk,
                                      name='character_settings',
                                      bg=colors['bg'],
                                      highlightcolor=colors['highlightcolor'],
                                      highlightbackground=colors['highlightbackground'],
                                      highlightthickness=0.1)
        character_settings.pack(fill='both')
        self.pages['character_setting'] = character_settings

        back_color = colors['back_button']
        def save() -> None:
            """
            退出时保存的钩子函数
            :return: None
            """
            ai = ai_name, ai_gender, ai_voice = name_e.get(), gender_var.get(), voice_var.get()
        back_button = tk.Button(character_settings,
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
                                command=lambda :self._back(character_settings,
                                                           self.pages['home'], pack_kwargs={'fill':'both'},
                                                           func=save)
                                )
        back_button.pack(side='top', anchor='w', pady=(20,0), padx=(18,0))

        setting_frame = tk.Frame(character_settings,
                                 name='setting_frame_character',
                                 #text='  伴侣配置  ',
                                 #font=('微软雅黑',12),
                                 bg=colors['bg'],
                                 highlightcolor=colors['highlightcolor'],
                                 highlightbackground=colors['highlightbackground'],
                                 highlightthickness=0.1)
        setting_frame.pack(fill='both', pady=20, padx=30)

        name_frame = tk.Frame(setting_frame,
                              name='name_frame',
                              bg=colors['bg'])
        name_frame.pack(fill='x', side='top',pady=(10,0))

        name_l_color = colors['name_label']
        name_l = tk.Label(name_frame,
                          name='name_label',
                          text='名字',
                          font=('微软雅黑',13),
                          bg=name_l_color['bg'],
                          highlightcolor=name_l_color['highlightcolor'],
                          highlightbackground=name_l_color['highlightbackground'],
                          highlightthickness=0.1,
                          fg=name_l_color['fg'],
                          bd=0.5)
        name_l.pack(side='left', anchor='n', padx=(20,0))

        name_e_color = colors['name_entry']
        name = self.commands['get_setting'](area='ai', name='name')
        name_e = tk.Entry(name_frame,
                          bg=name_e_color['bg'],
                          font=('微软雅黑',12),
                          highlightcolor=name_e_color['highlightcolor'],
                          highlightbackground=name_e_color['highlightbackground'],
                          relief='solid',
                          width=45)
        name_e.pack(side='left', padx=(25,0))
        name_e.insert(0, name)

        gender_frame = tk.Frame(setting_frame,
                                name='gender_frame',
                                bg=colors['bg'])
        gender_frame.pack(pady=(30,0), fill='x', side='top')

        gender_l_color = colors['gender_label']
        gender_label = tk.Label(gender_frame,
                              name='gender_label',
                              text='性别',
                              font=('微软雅黑', 13),
                              bg=gender_l_color['bg'],
                              highlightcolor=gender_l_color['highlightcolor'],
                              highlightbackground=gender_l_color['highlightbackground'],
                              highlightthickness=0.1,
                              fg=gender_l_color['fg'],
                              bd=0.5)
        gender_label.pack(side='left', anchor='n', padx=(20,0))

        gender_color = colors['gender_radiobutton']
        if 'gender-var' in self.cache:
            gender_var = self.cache['gender-var']
        else:
            self.commands['get_setting'](area='ai', name='gender')
            gender_var = tk.StringVar(gender_frame, 'boy')
            self.cache['gender-var'] = gender_var
        self.ttk_style('TRadiobutton',background=gender_color['bg'],font=('微软雅黑',12))
        gender_boy = ttk.Radiobutton(gender_frame,
                                    name='gender_boy',
                                    # bg=gender_color['bg'],
                                    # activebackground=gender_color['activebackground'],
                                    # activeforeground=gender_color['activeforeground'],
                                    text='男孩',
                                    # font=('微软雅黑', 12),
                                    variable=gender_var,
                                    value='boy')
        gender_boy.pack(side='left', padx=(25, 0))

        gender_girl = ttk.Radiobutton(gender_frame,
                                     name='gender_girl',
                                     # bg=gender_color['bg'],
                                     # activebackground=gender_color['activebackground'],
                                     # activeforeground=gender_color['activeforeground'],
                                     text='女孩',
                                     # font=('微软雅黑', 12),
                                     variable=gender_var,
                                     value='girl')
        gender_girl.pack(side='left', padx=(15, 0))

        voice_frame = tk.Frame(setting_frame,
                               name='voice_frame',
                               bg=colors['bg'])
        voice_frame.pack(pady=(30,0), fill='x', side='top')

        voice_l_color = colors['voice_label']
        voice_label = tk.Label(voice_frame,
                               name='voice_label',
                               text='声音模型（EdgeTTS）',
                               font=('微软雅黑', 13),
                               bg=voice_l_color['bg'],
                               highlightcolor=voice_l_color['highlightcolor'],
                               highlightbackground=voice_l_color['highlightbackground'],
                               highlightthickness=0.1,
                               fg=voice_l_color['fg'],
                               bd=0.5)
        voice_label.pack(side='left', anchor='n', padx=(20,0))

        voice_c_color = colors['voice_combobox']
        if 'voice-var' in self.cache:
            voice_var = self.cache['voice-var']
        else:
            self.commands['get_setting'](area='ai', name='voice')
            voice_var = tk.StringVar(voice_frame, 'zh-CN-XiaoxiaoNeural')
            self.cache['voice-var'] = voice_var
        voices = (
            "zh-CN-XiaoxiaoNeural",
            "zh-CN-XiaoyiNeural",
            "zh-CN-YunjianNeural",
            "zh-CN-YunxiNeural",
            "zh-CN-YunxiaNeural",
            "zh-CN-XiaohanNeural",
            "zh-CN-XiaomengNeural",
            "zh-CN-XiaomoNeural",
            "zh-CN-XiaoranNeural",
            "zh-CN-XiaoruiNeural",
            "zh-CN-XiaoshuangNeural",
            "zh-CN-XiaoxuanNeural",
            "zh-CN-XiaoyouNeural",
            "zh-CN-YunyangNeural",
            "zh-CN-YunyeNeural",
            "zh-CN-YunzeNeural"
        )
        voice_combobox = ttk.Combobox(voice_frame,
                                      name='voice_combobox',
                                      textvariable=voice_var,
                                      font=('微软雅黑',12),
                                      values=voices,
                                      background=voice_c_color['bg'])
        voice_combobox.pack(side='left', anchor='n', padx=(15,0))

        introduction_frame = tk.Frame(setting_frame,
                                      name='introduction_frame',
                                      bg=colors['bg'])
        introduction_frame.pack(pady=(30,0), fill='x', side='top')

        introduction_l_color = colors['introduction_label']
        introduction_label = tk.Label(introduction_frame,
                                      name='voice_label',
                                      text='描述',
                                      font=('微软雅黑', 13),
                                      bg=introduction_l_color['bg'],
                                      highlightcolor=introduction_l_color['highlightcolor'],
                                      highlightbackground=introduction_l_color['highlightbackground'],
                                      highlightthickness=0.1,
                                      fg=introduction_l_color['fg'],
                                      bd=0.5)
        introduction_label.pack(side='left', anchor='n', padx=(20,0))

        insertor_color = colors['insertor_text']
        text_insertor = tk.Text(introduction_frame,
                                name='text_insertor',
                                wrap='word',
                                bg=insertor_color['bg'],
                                font=('微软雅黑',12),
                                relief='solid',
                                bd=0.5,
                                width=40,
                                height=10,
                                padx=2,
                                pady=2)
        text_insertor.pack(side='left', anchor='n', padx=(15,0))
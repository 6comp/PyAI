# coding=UTF-8

"""
@file: ui.py
"""

# 导入
# import gc
import re
import json
import os.path
import webbrowser
import typing as tp
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk


__all__ = ['Ui']


# gc.disable()

global ui_logger
def init(get_logger) -> None:
    """
    初始化模块
    :param get_logger: 获取记录器调用方法
    :return: None
    """
    global ui_logger
    ui_logger = get_logger('ui')



class Ui:
    """
    UI 功能的实现
    """

    def __init__(self) -> None:
        """
        Initiate UI
        """

        # 颜色和语言配置
        self.ui_logger = ui_logger
        self.ui_config = self.config['ui_config']
        self.language = self.ui_config['language']
        self.text_language = self.ui_config['text_language'][self.language]
        self.color_mode = self.ui_config['colors']['mode']
        self.colors = self.ui_config['colors'][self.color_mode]

        # 预定义
        self.main_tk = None
        self.title_block = None
        self.style = None
        self.cache = {}
        self.pages = {}

        # 线程处理器
        self.ui_thread = self.thread(1, '[PyAI]UI-TaskProcessor')

        # 之后要处理的对话（与 api 的对话内容相同）
        self.new_dialogs = []

        # 添加 API 必要参数
        if api:=self.get_api():
            self.add_api(api)
        else:
            self.show_warn('warning', '提示', '您还未配置 API，请先配置')
        if info:=self.get_info():
            self.add_info(json.loads(info))
        else:
            self.show_warn('warning', '提示', '您还未配置伴侣，请先配置')


        self.ui_logger.info('Initiate have down (ui)')



    def ttk_style(self, *args, **kwargs) -> None:
        """
        刷新 ttk 小组件风格配置
        :return: None
        """
        self.ui_logger.debug(args, kwargs)
        self.style.configure(*args, **kwargs)
        self.ui_logger.info('Update ttk style')



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
        self.ui_logger.info('show warn')
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
        搭建窗口
        :return: None
        """

        self.main_tk = tk.Tk('PyAI', 'PyAI-UI')
        self.main_tk.title('PyAI')
        self.main_tk.iconbitmap('img\\PyAIICO.ico')
        x = (self.main_tk.winfo_screenwidth()-800) // 2
        y = (self.main_tk.winfo_screenheight()-550) // 2
        self.main_tk.geometry(f'800x550+{x}+{y}')
        self.main_tk.resizable(False, False)

        self.style = ttk.Style()

        self._build_home()

        self.ui_logger.info('build windows')

        self.main_tk.mainloop()



    def _build_home(self) -> None:
        """
        搭建主页面
        :return: None
        """
        if 'home' in self.pages:self.pages['home'].pack(fill='both')

        else:
            colors = self.colors['home']                        # 获取颜色配置


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
            cmd = (self._build_about, self._build_help, self._build_setting, self._build_character_settings)
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
            def chat_to(txt:str, text_control:scrolledtext.ScrolledText,
                        entry_control:tk.Entry, button_control:tk.Button) -> None:
                if txt:
                    entry_control.delete(0,'end')
                    entry_control.insert('end', '等待回复...')
                    entry_control.config(state='disabled')
                    button_control.config(state='disabled')

                    text_control.config(state='normal')
                    text_control.insert('end', txt+'\n', 'user')
                    text_control.config(state='disabled')

                    result = self.chat(txt)
                    if result:
                        answer, date = result
                        # read_content = re.sub(r'\(.*+\)', '，', answer)
                        # self.ui_logger.debug(read_content)
                        # self.say(read_content)
                        text_control.config(state='normal')
                        text_control.insert('end', '\n', r'\n')
                        text_control.insert('end', answer+'\n', 'ai')
                        text_control.insert('end', '\n', r'\n')
                        text_control.config(state='disabled')
                        self.new_dialogs.append((answer, txt, date))
                    else:
                        text_control.config(state='normal')
                        text_control.insert('end', '\n', r'\n')
                        text_control.config(state='disabled')
                        self.show_warn('error', '错误', '请求时发生错误！\n请检查您的配置或查阅帮助文档')
                    button_control.config(state='normal')
                    entry_control.config(state='normal')
                    entry_control.delete(0, 'end')
                    text_control.see('end')
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
                                          command=lambda :self.add_task(self.ui_thread, chat_to,
                                                                        ('（摸摸头）', scr_text, insert_entry, button))
                                        )
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
                                      command=lambda :self.add_task(self.ui_thread, chat_to,
                                                                    ('（抱一抱）', scr_text, insert_entry, button))
                                   )
            hug_button.pack(side='left', anchor='n', pady=(20,0), padx=(20,0))

            hug_color = action_color['save_button']
            def save_dialog(event=None):
                if self.new_dialogs:
                    if not (get_info:=self.get_info()):
                        self.show_warn('warning', '提示', '你还没有配置过伴侣')
                        return
                    get_info = json.loads(get_info)
                    analysis, date = self.analysis_dialog(*self.new_dialogs, history=get_info)
                    self.save_info(analysis)
                    self.ui_logger.debug('Save info done')
                    self.save_dialogs(*self.new_dialogs)
                    self.ui_logger.debug('save dialogs done')
                    self.new_dialogs.clear()
                    self.show_warn('info', '提示', '保存完成')
                else:
                    self.ui_logger.debug('No dialogs')
                    self.show_warn('info', '提示', '还没有新的对话记录')
                self.ui_logger.info('Save ended')
            save_button = tk.Button(action_frame,
                                    name='save_button',
                                    text='保存对话',
                                    activebackground=hug_color['activebackground'],
                                    activeforeground=hug_color['activeforeground'],
                                    bg=hug_color['bg'],
                                    bd=0.5,
                                    relief='solid',
                                    font=('微软雅黑', 10),
                                    padx=15,
                                    pady=2,
                                    command=save_dialog)
            save_button.pack(side='right', anchor='n', pady=(20,0), padx=(0,26))
            save_button.bind('<Control-S>', save_dialog)

            text_color = colors_frame['chat_text']
            self.cache['dialogs-generator'] = self.get_dialogs()
            def flush(event) -> None:
                if event.delta < 0:
                    top = scr_text.yview()[0]
                    if top == 0.0:
                        scr_text.config(state='normal')
                        try:
                            for _ in range(20):
                                dialogs = next(self.cache['dialogs-generator'])
                                ai, user, date = dialogs
                                scr_text.insert(1.0, user+'\n', 'user')
                                scr_text.insert(2.0, '\n', r'\n')
                                scr_text.insert(3.0, ai+'\n', 'ai')
                                scr_text.insert(4.0, '\n', r'\n')
                        except StopIteration:
                            self.ui_logger.info('No dialogs can show')
                scr_text.config(state='disabled')

            scr_text = scrolledtext.ScrolledText(chat_frame,
                                             wrap='char',
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
            scr_text.pack(pady=(23,0), padx=10)
            scr_text.tag_config('ai', background=text_color['tag_ai'], relief='flat')
            scr_text.tag_config('user', background=text_color['tag_user'], relief='flat')
            scr_text.tag_config(r'\n', relief='flat')
            scr_text.bind('<MouseWheel>', flush)

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
                                    width=61)
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
                                      command=lambda :self.add_task(self.ui_thread, chat_to,
                                                                    (insert_entry.get(), scr_text, insert_entry, button))
                                    )
            send_button.pack(side='left', padx=(13,0))
            chat_frame.bind_all('<Return>', lambda e:self.add_task(self.ui_thread, chat_to,
                                                                   (insert_entry.get(), scr_text, insert_entry, button))
                                )
        self.ui_logger.info('Build the home page')



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
        self.ui_logger.info('Return to previous page')



    def _build_setting(self) -> None:
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
            a = self.show_warn('question', '询问', '是否保存？')
            if a:
                get_api = re.sub(r'\s?','',api_e.get())
                self.ui_logger.debug(get_api)
                self.set_api(get_api)                                           # 调用 DataManager 的 set_api 方法
                self.add_api(get_api)                                           # 更新请求头中的 API
            self.ui_logger.info('Updating api ended')
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
        api = self.get_api()
        api_e = tk.Entry(api_frame,
                         bg=api_e_color['bg'],
                         font=('微软雅黑',12),
                         highlightcolor=api_e_color['highlightcolor'],
                         highlightbackground=api_e_color['highlightbackground'],
                         relief='solid',
                         width=50)
        api_e.pack(side='left', padx=(20,0))
        api_e.insert(0, api if api else '')
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

        self.ui_logger.info('build the setting page')



    def _build_about(self) -> None:
        """
        搭建关于页面 GUI
        :return: None
        """
        self.pages['home'].forget()
        if 'about' in self.pages:self.pages['about'].pack(fill='both')

        else:
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
                self.ui_logger.debug('Get image cache "image-about"')
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


            about_text = f"""PyAI
            
一个基于 DeepSeek 大模型实现的 AI 伴侣
希望能给予你温暖和陪伴

An AI companion based
on the DeepSeek AI model.
Hoping to bring you warmth and company.



•作者Author: 6tft6(6comp)
•仓库Github: https://github.com/6comp/PyAI
•邮箱E-mail: 3950264691@qq.com


其实这玩意能翻
    """
            text_color = colors['text_label']
            text = tk.Text(about,
                            name='about_text',
                            #text=about_text,
                            font=('微软雅黑',13),
                            bg=text_color['bg'],
                            highlightcolor=text_color['highlightcolor'],
                            highlightbackground=text_color['highlightbackground'],
                            highlightthickness=0.1,
                            width=38,
                            # height=15,
                            relief='solid',
                            fg=text_color['fg'],
                            bd=0.5,
                           padx=10,
                           pady=10)
            text.pack(side='top', anchor='w', pady=(120,82), padx=(260,0))
            text.insert(0.0, about_text)
            text.config(state='disabled')

        self.ui_logger.info('Build the about page')



    def _build_help(self) -> None:
        """
        打开帮助方法
        :return: None
        """
        path = os.path.abspath(r'docs\HelpIndex.html')
        webbrowser.open_new_tab(f'file:///{path}')
        self.ui_logger.info('Open the "HelpIndex.html" helpfile to help user to get help')



    def _build_character_settings(self) -> None:
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

        def save() -> None:
            """
            退出时保存的钩子函数
            :return: None
            """
            a = self.show_warn('question', '询问', '是否保存？')
            if not a:return None

            ai = n, g, v, i = name_e.get().replace('\n',''), gender_var.get(), voice_var.get(), text_insertor.get(0.0, 'end').rstrip()
            if not all(ai):
                self.show_warn('warning', '提示', '还有空余选项未填')
                self.ui_logger.warning('Some question have not answered')
                return None
            if v not in voices:
                self.show_warn('warning', '提示', '你选择的声音模型不可使用')
                return None
            self.update_setting('voice', v)
            if all_info:
                abouts = all_info['对话者相关属性']['0']
                self.ui_logger.debug(abouts)
                abouts['姓名']=n
                abouts['性别']=g
                abouts['补充']=i
                self.ui_logger.debug(abouts)
                save_info = all_info
            else:
                save_info = {"对话者相关属性":{
                                 '0':{
                                     "姓名":n,
                                     "性别":g,
                                     "补充":i
                                     },
                                 '1':{
                                     "姓名":'暂时未知',
                                     "性别":'暂时未知',
                                     "补充":'暂无'
                                     }
                                            },
                                "相关记忆":[],
                                "正在进行的对话":{}
                            }
            self.ui_logger.debug(save_info)
            self.save_info(json.dumps(save_info, ensure_ascii=False))
            self.add_info(save_info)

            self.ui_logger.info('Save data about the character')
            return None

        back_color = colors['back_button']
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

        name,introduction,gender=('',)*3
        if all_info:=self.get_info():
            all_info = json.loads(all_info)
            self.ui_logger.debug(all_info)
            introduction = all_info['对话者相关属性']['0']
            name = introduction['姓名']
            gender = introduction['性别']
            del introduction['性别'], introduction['姓名']
            introduction = '\n\n'.join((i_value+'\n' for i_value in introduction.values()))

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
            gender_var = tk.StringVar(gender_frame, gender)
            self.cache['gender-var'] = gender_var
        self.ttk_style('TRadiobutton',background=gender_color['bg'],font=('微软雅黑',12))
        gender_boy = ttk.Radiobutton(gender_frame,
                                    name='gender_boy',
                                    # bg=gender_color['bg'],
                                    # activebackground=gender_color['activebackground'],
                                    # activeforeground=gender_color['activeforeground'],
                                    text='男生',
                                    # font=('微软雅黑', 12),
                                    variable=gender_var,
                                    value='男生')
        gender_boy.pack(side='left', padx=(25, 0))

        gender_girl = ttk.Radiobutton(gender_frame,
                                     name='gender_girl',
                                     # bg=gender_color['bg'],
                                     # activebackground=gender_color['activebackground'],
                                     # activeforeground=gender_color['activeforeground'],
                                     text='女生',
                                     # font=('微软雅黑', 12),
                                     variable=gender_var,
                                     value='女生')
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
            voice = voice if (voice:=self.get_setting('voice')) else ''
            voice_var = tk.StringVar(voice_frame, voice)
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
        introduction_frame.pack(pady=(30,60), fill='x', side='top')

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
        text_insertor.insert(0.0, introduction)

        self.ui_logger.info('build the character_setting page')
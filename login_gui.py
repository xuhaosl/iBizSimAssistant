"""
iBizSim 登录验证 GUI 工具
提供图形界面用于输入账号和密码，无需配置环境变量
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.config.settings import Settings
from src.browser.browser_manager import BrowserManager
from src.browser.page_handler import PageHandler
from src.auth.login_handler import LoginHandler
from src.data.game_extractor import GameExtractor
from src.utils.logger import get_logger


class LoginGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("iBizSim 助手")
        self.root.state('zoomed')
        self.root.resizable(True, True)
        
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.show_password = tk.BooleanVar(value=True)
        self.status = tk.StringVar(value="准备就绪")
        self.is_running = False
        
        self.games = []
        self.selected_game = None
        self.navigation_queue = []
        self.playwright_thread = None
        self.playwright_queue = []
        self.playwright_running = False
        
        self.setup_ui()
        self.logger = get_logger()
        
        self.browser_manager = None
        self.page_handler = None
        self.login_handler = None
        self.game_extractor = None
        self.settings = None
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(
            main_frame, 
            text="iBizSim 助手",
            font=("Microsoft YaHei UI", 16, "bold"),
            foreground="#2c3e50"
        )
        title_label.pack(pady=(0, 20))
        
        info_label = ttk.Label(
            main_frame,
            text="请输入您的 iBizSim 账号和密码",
            font=("Microsoft YaHei UI", 10)
        )
        info_label.pack(pady=(0, 10))
        
        input_frame = ttk.LabelFrame(main_frame, text="登录信息", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(input_frame, text="用户名:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        username_entry = ttk.Entry(
            input_frame, 
            textvariable=self.username,
            width=40,
            font=("Microsoft YaHei UI", 10)
        )
        username_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(input_frame, text="密码:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        password_entry = ttk.Entry(
            input_frame,
            textvariable=self.password,
            width=40,
            font=("Microsoft YaHei UI", 10),
            show=""
        )
        password_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        self.password_entry = password_entry
        
        show_password_check = ttk.Checkbutton(
            input_frame,
            text="显示密码",
            variable=self.show_password,
            command=self.toggle_password_visibility
        )
        show_password_check.grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=(20, 0))
        
        login_button = ttk.Button(
            button_frame,
            text="登录",
            command=self.start_verification,
            width=20,
            state=tk.NORMAL
        )
        login_button.pack(side=tk.LEFT, padx=5)
        
        stop_button = ttk.Button(
            button_frame,
            text="停止",
            command=self.stop_verification,
            width=20,
            state=tk.DISABLED
        )
        stop_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = ttk.Button(
            button_frame,
            text="清空",
            command=self.clear_inputs,
            width=20
        )
        clear_button.pack(side=tk.LEFT, padx=5)
        
        status_frame = ttk.LabelFrame(main_frame, text="状态", padding="10")
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        status_label = ttk.Label(
            status_frame,
            textvariable=self.status,
            font=("Microsoft YaHei UI", 10),
            wraplength=500
        )
        status_label.pack(fill=tk.X)
        
        games_frame = ttk.LabelFrame(main_frame, text="我参加的赛事", padding="10")
        games_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.games_listbox = tk.Listbox(
            games_frame,
            height=15,
            font=("Microsoft YaHei UI", 10),
            selectmode=tk.SINGLE
        )
        self.games_listbox.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.games_listbox, orient=tk.VERTICAL, command=self.games_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.games_listbox.config(yscrollcommand=scrollbar.set)
        
        enter_game_button = ttk.Button(
            games_frame,
            text="进入比赛",
            command=self.enter_game,
            state=tk.DISABLED
        )
        enter_game_button.pack(fill=tk.X, pady=(5, 0))
        
        log_button_frame = ttk.Frame(main_frame)
        log_button_frame.pack(fill=tk.X, pady=(10, 0))
        
        log_button = ttk.Button(
            log_button_frame,
            text="查看日志",
            command=self.show_log_dialog,
            width=20
        )
        log_button.pack(side=tk.RIGHT)
        
        self.login_button = login_button
        self.stop_button = stop_button
        self.enter_game_button = enter_game_button
        
        self.log_text = scrolledtext.ScrolledText(
            None,
            width=80,
            height=20,
            font=("Consolas", 9),
            wrap=tk.WORD
        )
    
    def log(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.logger.info(message)
    
    def update_status(self, status, color="black"):
        self.status.set(status)
        self.log(f"[状态] {status}")
    
    def clear_inputs(self):
        self.username.set("")
        self.password.set("")
        self.update_status("已清空输入框")
        self.log("[操作] 清空了输入框")
    
    def toggle_password_visibility(self):
        show = self.show_password.get()
        self.password_entry.config(show="" if show else "*")
        self.log(f"[密码] 密码显示模式: {'可见' if show else '隐藏'}")
    
    def bring_to_front(self):
        try:
            self.root.lift()
            self.root.focus_force()
            self.root.attributes('-topmost', True)
            self.root.after(100, lambda: self.root.attributes('-topmost', False))
        except Exception as e:
            self.log(f"[错误] 无法提升界面: {e}")
    
    def show_log_dialog(self):
        log_window = tk.Toplevel(self.root)
        log_window.title("日志")
        log_window.geometry("800x600")
        
        log_frame = ttk.Frame(log_window, padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        log_text = scrolledtext.ScrolledText(
            log_frame,
            width=80,
            height=25,
            font=("Consolas", 9),
            wrap=tk.WORD
        )
        log_text.pack(fill=tk.BOTH, expand=True)
        
        log_text.insert(tk.END, self.log_text.get("1.0", tk.END))
        log_text.config(state=tk.DISABLED)
        
        button_frame = ttk.Frame(log_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        close_button = ttk.Button(
            button_frame,
            text="关闭",
            command=log_window.destroy,
            width=15
        )
        close_button.pack(side=tk.RIGHT)
        
        clear_log_button = ttk.Button(
            button_frame,
            text="清空日志",
            command=lambda: self.clear_log(log_text),
            width=15
        )
        clear_log_button.pack(side=tk.RIGHT, padx=(0, 10))
    
    def clear_log(self, log_text_widget=None):
        self.log_text.delete("1.0", tk.END)
        if log_text_widget:
            log_text_widget.config(state=tk.NORMAL)
            log_text_widget.delete("1.0", tk.END)
            log_text_widget.config(state=tk.DISABLED)
    
    def load_games(self):
        try:
            self.log("[赛事] 正在加载赛事列表...")
            
            if not self.page_handler:
                self.log("[错误] 页面处理器未初始化")
                return
            
            self.game_extractor = GameExtractor(self.page_handler)
            
            games = self.game_extractor.extract_games_from_table()
            
            if not games:
                self.log("[赛事] 尝试提取链接...")
                games = self.game_extractor.extract_games_with_links()
            
            self.games = games
            
            self.games_listbox.delete(0, tk.END)
            
            for i, game in enumerate(games):
                game_id = game.get('比赛ID', '')
                game_name = game.get('比赛名称', f'赛事 {i+1}')
                create_date = game.get('创建日期', '')
                game_status = game.get('比赛状态', '')
                game_desc = game.get('比赛描述', '')
                
                display_text = f"{game_id}：{game_name}，{create_date}，{game_status}，{game_desc}"
                
                self.games_listbox.insert(tk.END, display_text)
                self.log(f"[赛事] 添加: {game_name} - {game_status}")
            
            self.update_status(f"找到 {len(games)} 个赛事", color="green")
            self.log(f"[赛事] 总共加载了 {len(games)} 个赛事")
            
            if games:
                self.enter_game_button.config(state=tk.NORMAL)
            else:
                self.enter_game_button.config(state=tk.DISABLED)
                
        except Exception as e:
            self.log(f"[错误] 加载赛事列表失败: {e}")
            self.update_status("加载赛事列表失败", color="red")
    
    def enter_game(self):
        try:
            if not self.page_handler:
                messagebox.showerror("错误", "浏览器未启动，请先登录")
                self.update_status("浏览器未启动", color="red")
                self.log("[错误] page_handler为None")
                return
                
            selection = self.games_listbox.curselection()
            if not selection:
                messagebox.showwarning("提示", "请先选择一个赛事")
                return
            
            index = selection[0]
            if index >= len(self.games):
                messagebox.showerror("错误", "选择的赛事无效")
                return
            
            game = self.games[index]
            game_url = game.get('url')
            
            if not game_url:
                messagebox.showerror("错误", "该赛事没有有效的链接")
                return
            
            game_name = game.get('比赛名称', 'Unknown')
            self.log(f"[赛事] 正在进入赛事: {game_name}")
            self.log(f"[赛事] 原始URL: {game_url}")
            
            if game_url.startswith('/'):
                game_url = f"https://www.ibizsim.cn{game_url}"
            
            self.log(f"[赛事] 转换后URL: {game_url}")
            self.update_status(f"正在进入赛事: {game_name}", color="blue")
            
            self.playwright_queue.append(('navigate', game_url, game_name))
            self.log(f"[队列] 已添加导航请求到Playwright队列")
            
            if not self.playwright_thread or not self.playwright_thread.is_alive():
                self.log(f"[Playwright] 启动Playwright操作线程")
                self.playwright_running = True
                self.playwright_thread = threading.Thread(target=self.playwright_operation_loop)
                self.playwright_thread.daemon = True
                self.playwright_thread.start()
                
        except Exception as e:
            self.log(f"[错误] 进入赛事失败: {e}")
            self.update_status("进入赛事失败", color="red")
            messagebox.showerror("错误", f"进入赛事失败：\n\n{e}")
    
    def playwright_operation_loop(self):
        self.log("[Playwright] Playwright操作线程已启动")
        self.root.after(0, self.bring_to_front)
        while self.playwright_running:
            if self.playwright_queue:
                operation = self.playwright_queue.pop(0)
                op_type = operation[0]
                
                try:
                    if op_type == 'login':
                        _, username, password = operation
                        self.run_login_verification(username, password)
                    elif op_type == 'navigate':
                        _, game_url, game_name = operation
                        self.log(f"[Playwright] 执行导航: {game_name}")
                        
                        if self.page_handler.navigate(game_url):
                            self.root.after(0, lambda: self.update_status(f"已进入赛事: {game_name}", color="green"))
                            self.root.after(0, self.bring_to_front)
                            self.log(f"[成功] 成功跳转到赛事页面")
                        else:
                            error_msg = "无法跳转到赛事页面"
                            if not self.page_handler:
                                error_msg = "浏览器未启动，请先登录"
                            self.root.after(0, lambda: self.update_status("跳转失败", color="red"))
                            self.log("[错误] 无法跳转到赛事页面")
                            self.root.after(0, lambda: messagebox.showerror("错误", error_msg))
                    else:
                        self.log(f"[警告] 未知的操作类型: {op_type}")
                        
                except Exception as e:
                    self.root.after(0, lambda: self.log(f"[错误] Playwright操作失败: {e}"))
                    self.root.after(0, lambda: self.update_status("操作失败", color="red"))
                    self.root.after(0, lambda: messagebox.showerror("错误", f"Playwright操作失败：\n\n{e}"))
            else:
                import time
                time.sleep(0.1)
        
        self.log("[Playwright] Playwright操作线程已退出")
    
    def start_verification(self):
        if self.is_running:
            messagebox.showwarning("警告", "验证正在进行中，请先停止当前任务")
            return
        
        username = self.username.get().strip()
        password = self.password.get().strip()
        
        if not username or not password:
            messagebox.showerror("错误", "用户名和密码不能为空")
            return
        
        self.is_running = True
        self.login_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        self.update_status("正在启动验证...", color="blue")
        self.log(f"[开始] 使用用户名: {username}")
        self.log(f"[开始] 使用密码: {password}")
        
        if not self.playwright_thread or not self.playwright_thread.is_alive():
            self.playwright_running = True
            self.playwright_thread = threading.Thread(target=self.playwright_operation_loop)
            self.playwright_thread.daemon = True
            self.playwright_thread.start()
        
        self.playwright_queue.append(('login', username, password))
        self.log(f"[队列] 已添加登录请求到Playwright队列")
    
    def stop_verification(self):
        if not self.is_running:
            return
        
        self.is_running = False
        self.playwright_running = False
        self.login_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        
        self.update_status("正在停止...", color="orange")
        self.log("[操作] 用户请求停止验证")
        
        if self.browser_manager:
            threading.Thread(target=self.cleanup_browser).start()
    
    def run_login_verification(self, username, password):
        try:
            self.log("[配置] 加载配置文件...")
            self.settings = Settings()
            self.log(f"[配置] 网站: {self.settings.website.get('base_url')}")
            self.log(f"[配置] 登录页面: {self.settings.website.get('login_url')}")
            
            self.settings.username = username
            self.settings.password = password
            
            self.log("[浏览器] 启动浏览器...")
            browser_config = self.settings.browser
            headless = browser_config.get('headless', False)
            timeout = browser_config.get('timeout', 30000)
            screenshot_on_error = browser_config.get('screenshot_on_error', True)
            
            self.browser_manager = BrowserManager(
                headless=headless,
                timeout=timeout,
                screenshot_on_error=screenshot_on_error
            )
            
            if not self.browser_manager.start():
                self.update_status("浏览器启动失败", color="red")
                self.log("[错误] 无法启动浏览器")
                self.is_running = False
                self.root.after(0, lambda: self.login_button.config(state=tk.NORMAL))
                self.root.after(0, lambda: self.stop_button.config(state=tk.DISABLED))
                return
            
            self.log("[浏览器] 浏览器启动成功")
            self.root.after(0, self.bring_to_front)
            
            page = self.browser_manager.get_page()
            if not page:
                self.update_status("无法获取页面对象", color="red")
                self.log("[错误] 无法获取页面对象")
                self.cleanup_browser()
                self.is_running = False
                self.root.after(0, lambda: self.login_button.config(state=tk.NORMAL))
                self.root.after(0, lambda: self.stop_button.config(state=tk.DISABLED))
                return
            
            self.page_handler = PageHandler(page, on_navigate=self.bring_to_front)
            self.settings.username = username
            self.settings.password = password
            
            self.login_handler = LoginHandler(self.page_handler, self.settings, on_navigate=self.bring_to_front)
            self.log("[登录] 初始化登录处理器")
            
            self.update_status("正在登录...", color="blue")
            self.log("[登录] 导航到登录页面")
            self.log("[登录] 填写用户名和密码")
            
            login_success = self.login_handler.login()
            
            if login_success:
                self.update_status("登录成功！", color="green")
                self.log("[成功] 登录验证成功！")
                self.log(f"[状态] 已登录: {self.login_handler.is_authenticated()}")
                self.log(f"[页面] 当前页面: {page.url}")
                
                self.root.after(0, self.bring_to_front)
                
                self.update_status("正在导航到赛事列表页面...", color="blue")
                self.log("[赛事] 导航到mygames页面...")
                
                mygames_url = "https://www.ibizsim.cn/games/mygames"
                if self.page_handler.navigate(mygames_url):
                    self.log("[赛事] 成功导航到赛事列表页面")
                    self.root.after(0, self.bring_to_front)
                    self.update_status("正在加载赛事列表...", color="blue")
                    self.log("[赛事] 开始加载赛事列表...")
                    
                    self.load_games()
                    self.root.after(0, self.bring_to_front)
                else:
                    self.log("[错误] 无法导航到赛事列表页面")
                    self.update_status("导航到赛事列表失败", color="red")
            else:
                self.update_status("登录失败", color="red")
                self.log("[失败] 登录验证失败")
                self.log("[原因] 可能是用户名或密码错误")
                
                messagebox.showerror(
                    "验证失败",
                    "登录验证失败！\n\n可能的原因：\n1. 用户名或密码错误\n2. 网站选择器配置错误\n3. 网络连接问题\n\n请查看日志了解详细信息。"
                )
                
        except Exception as e:
            self.update_status(f"发生错误: {str(e)}", color="red")
            self.log(f"[异常] 测试过程中发生异常: {e}")
            messagebox.showerror("错误", f"发生错误：\n\n{e}")
        finally:
            if not self.is_running:
                self.cleanup_browser()
            self.root.after(0, lambda: self.login_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.stop_button.config(state=tk.DISABLED))
    
    def cleanup_browser(self):
        self.playwright_running = False
        if self.browser_manager:
            self.log("[清理] 关闭浏览器...")
            self.browser_manager.stop()
            self.browser_manager = None
            if not self.page_handler or not self.is_running:
                self.page_handler = None
            self.login_handler = None
    
    def on_closing(self):
        if self.is_running:
            if messagebox.askyesno("确认", "验证正在进行中，确定要退出吗？"):
                self.stop_verification()
        self.cleanup_browser()
        self.root.destroy()
    
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()


def main():
    app = LoginGUI()
    app.run()


if __name__ == '__main__':
    main()

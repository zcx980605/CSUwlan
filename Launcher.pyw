# Launcher for "Autologin.py" (Build for Windows only)
# First Build In Version 0.10.0 @ 2019/08/25 $ 核心功能
# In Version 0.11.0 @ 2019/08/26 $ 调用主程序时利用命令行传参
# In Version 0.11.3 @ 2019/09/02 $ 可指定python解释器路径、检测无线网络连接状态
# In Version 0.12.0 @ 2019/09/04 $ 独立的配置信息文件
# In Version 0.12.1 @ 2019/09/14 $ 阻止系统自动从无网络访问的WLAN断开(issue of Win10 1903)
# In Version 0.12.3 @ 2019/09/22 $ 无网络连接时在限定时间内重试
# In Version 0.12.4 @ 2019/09/28 $ 错误码修改，线程同步(issue 20190926)
# In Version 0.12.5 @ 2019/10/20 $ 转义处理网址中的特殊含义字符以安全地回显消息(issue 20191011)

import os
import subprocess
import sys
import threading
from time import sleep
from urllib import request

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.curdir)
try:
    from launcher_config import *
except ImportError:
    print("\nMissing configuration file 'launcher_config.py'. Please reinstall to fix.")
    sys.exit(2)
except SyntaxError as err:
    print("\nBad configuration file detected. Please correct.")
    print('\t'+str(err.args))
    sys.exit(255)


class MyRedirectHandler(request.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, hdrs):
        """重写父类http_error_302方法，阻止其自动跟踪重定向"""
        return fp


class MyThread(threading.Thread):
    def __init__(self, target, args, daemon):
        """初始化父类属性和新增的report属性"""
        super().__init__(target=target, args=args, daemon=daemon)
        self.report = None

    def run(self):
        """重写父类run方法，使之可更新report属性"""
        self.report = self._target(*self._args)


def try_req(req_obj):
    global con_timeout

    try:
        resp = request.urlopen(req_obj, timeout=con_timeout)
    except Exception as err:
        print(err)
    else:
        return resp


def no_window_sub_proc(cmd, redirect_stdout):
    mystartupinfo = subprocess.STARTUPINFO()
    mystartupinfo.wShowWindow = subprocess.SW_HIDE
    if redirect_stdout:
        return subprocess.Popen(args=cmd, shell=True, stdout=subprocess.PIPE, startupinfo=mystartupinfo)
    else:
        return subprocess.Popen(args=cmd, shell=True, startupinfo=mystartupinfo)


def get_wlan_sys_info():
    global connected

    connected = False
    sub_proc = no_window_sub_proc('NETSH wlan show interfaces', True)
    sub_proc.wait(3)
    wlan_sys_info = sub_proc.stdout.read().decode('gbk')
    wlan_sys_info = wlan_sys_info.replace(' ', '').split('\r\n')
    if '状态:已连接' in wlan_sys_info:
        connected = True
        return [item[item.find(':')+1:] for item in wlan_sys_info if item[:4] == 'SSID'][0]
    else:
        return ''


def connect_to_ap(name):
    sub_proc = no_window_sub_proc('NETSH wlan connect name="'+name+'"', False)
    sub_proc.wait(3)


def start_login(argument=''):
    global path_of_python, monitor_wlan_if_timeout, event_thread_start

    event_thread_start.set()
    path_of_main_script = os.path.abspath(r'.\AutoLogin.py')
    ret_code = os.system(path_of_python+' '+path_of_main_script+' '+argument)
    if ret_code == 200:
        ret_code = 0
        sleep(monitor_wlan_if_timeout)
    return ret_code


def timing(seconds):
    global event_thread_start

    event_thread_start.set()
    sleep(seconds)


myhandler = MyRedirectHandler()
myopener = request.build_opener(myhandler)
request.install_opener(myopener)

req_1 = request.Request(test_url)
req_1.add_header('User-Agent', ua)

event_thread_start = threading.Event()
thread_timing = MyThread(timing, (wait_for_wlan_con_timout,), True)
thread_timing.start()
event_thread_start.wait()
event_thread_start.clear()
while thread_timing.isAlive():
    thread_check_internet = MyThread(try_req, (req_1,), True)
    thread_check_internet.start()
    ssid_0 = get_wlan_sys_info()
    thread_check_internet.join(hard_timeout-2)
    resp_1 = thread_check_internet.report
    if resp_1 == None:
        if connected:
            thread_check_internet = MyThread(try_req, (req_1,), True)
            thread_check_internet.start()
            thread_check_internet.join(hard_timeout)
            resp_1 = thread_check_internet.report
            break
    else:
        break
    sleep(0.5)

if resp_1 == None:
    if connected:
        thread_login = MyThread(start_login, ('/return 200',), True)
    else:
        sys.exit(0)
else:
    if resp_1.getcode() == 302:
        location = resp_1.getheader('location')
    else:
        os.system(
            'ECHO.&ECHO Exception occured in step 1:&ECHO \tNot the expected status code.&ECHO.&PAUSE')
        sys.exit(0)
    if url_pattern in location:
        thread_login = MyThread(
            start_login, ('/return 200 /location "'+location+'"',), False)
    elif location == test_succeed_redirection:
        sys.exit(0)
    else:
        chars_to_escape = ['&', '>', '<']
        for char in chars_to_escape:
            location = location.replace(char, '^'+char)
        os.system('ECHO.&ECHO Exception occured in step 1:&ECHO \tUnsupported authentication page -' +
                  location+'.&ECHO.&PAUSE')
        sys.exit(0)

thread_login.start()
event_thread_start.wait()
event_thread_start.clear()

while thread_login.isAlive():
    ssid = get_wlan_sys_info()
    if connected:
        if not ssid == ssid_0:
            connect_to_ap(ssid_0)
            sleep(1)
    else:
        connect_to_ap(ssid_0)
        sleep(1)
    sleep(0.3)

if not thread_login.report == 0:
    sys.exit(thread_login.report)

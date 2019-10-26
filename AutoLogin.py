# First Version 0.9.0 @ 2019/05/01 $ 核心功能
# Version 0.9.1 @ 2019/05/04 $ 输出、错误处理
# Version 0.9.2 @ 2019/05/11 $ 历史记录，超时硬限制
# Version 0.10.0 @ 2019/08/25 $ 无需操作时不弹出窗口(Launcher.pyw)
# Version 0.11.0 @ 2019/08/26 $ step3超时重试，命令行参数，模块化重构
# Version 0.11.1 @ 2019/08/27 $ 登出功能
# Version 0.11.2 @ 2019/09/01 $ 显示系统无线接口信息，重构主函数
# Version 0.11.3 @ 2019/09/02 $ “账号已在线”错误时尝试注销并重试，启动器更新
# Version 0.12.0 @ 2019/09/04 $ 独立的配置信息文件
# Version 0.12.1 @ 2019/09/14 $ 启动器更新
# Version 0.12.2 @ 2019/09/20 $ 配置文件支持直接运行以修改账号密码
# Version 0.12.3 @ 2019/09/22 $ 启动器更新
# Version 0.12.4 @ 2019/09/28 $ 错误码修改，启动器更新
# Version 0.12.5 @ 2019/10/20 $ 启动器更新
#TODO issue 20191026 存在多个候选连接时Windows可能在step3、4未完成时切换网络

import json
import os
import sqlite3
import sys
import threading
import time
from urllib import error, parse, request

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from config import *
except ImportError:
    print("\nMissing configuration file 'config.py'. Please reinstall to fix.")
    time.sleep(2)
    sys.exit(2)
except SyntaxError as err:
    print("\nBad configuration file detected. Please correct.")
    print('\t'+str(err.args))
    time.sleep(2)
    sys.exit(255)

cur_time = time.time()
IsWindows = sys.platform == 'win32'
if IsWindows:
    os.system('TITLE 登录数字中南')
    if save_to_install_dir:
        os.chdir(os.path.dirname(__file__))
    else:
        os.chdir(history_db_dir)

    def pause():
        if enable_pause:
            print('')
            os.system("PAUSE")

    def show_wlan_info(repeat, interval):
        import subprocess

        i = 0 if repeat == 0 else 1
        interval = 0.0 if repeat == 1 else interval
        while i <= repeat:
            sub_proc = subprocess.Popen(
                'NETSH wlan show interfaces', shell=True, stdout=subprocess.PIPE)
            sub_proc.wait()
            wlan_sys_info = sub_proc.stdout.read().decode('gbk')
            os.system('CLS')
            print(wlan_sys_info)

            time.sleep(interval)
            if not repeat == 0:
                i = i+1

else:
    os.chdir(os.getenv('HOME')+'/notebooks')

    def pause():
        if enable_pause:
            input('\nPress Enter to continue...')

    def show_wlan_info(repeat, interval):
        import subprocess

        i = 0 if repeat == 0 else 1
        interval = 0.0 if repeat == 1 else interval
        while i <= repeat:
            colums = os.get_terminal_size()[0]
            sub_proc = subprocess.Popen(
                'ifconfig wlan0', shell=True, stdout=subprocess.PIPE)
            sub_proc.wait()
            wlan_sys_info = sub_proc.stdout.read().decode('gbk')
            wlan_sys_info = wlan_sys_info.split('\n')
            flush_str = ''
            new_line = 0
            for item in wlan_sys_info:
                if len(item) <= colums:
                    flush_str = flush_str+item+' '*(colums-len(item))
                else:
                    flush_str = flush_str+item+' '*(len(item)-colums)
                    new_line = new_line+1
            sys.stdout.write(
                '\r\b'*(len(wlan_sys_info)+new_line)+flush_str+'\r')
            sys.stdout.flush()

            time.sleep(interval)
            if not repeat == 0:
                i = i+1


def handle_args():
    global enable_pause, location, skip_main, logout_mode, ret_code

    i = 1
    skip_main = False
    logout_mode = False
    ret_code = 0
    arg_count = len(sys.argv)-1
    while i <= arg_count:
        argument = sys.argv[i]
        if argument == '/location':
            if i+1 <= arg_count:
                i = i+1
                location = sys.argv[i]
        elif argument == '/logout':
            skip_main = True
            logout_mode = True
        elif argument == '/sysinfo':
            skip_main = True
            repeat = 1
            interval = 1.0
            if (i+1 <= arg_count) and (sys.argv[i+1] == '/r'):
                i = i+1
                repeat = 0
                if (i+1 <= arg_count) and (sys.argv[i+1][0] != '/'):
                    i = i+1
                    repeat = int(sys.argv[i])
                if (i+1 <= arg_count) and (sys.argv[i+1][0] != '/'):
                    i = i+1
                    interval = float(sys.argv[i])
            show_wlan_info(repeat, interval)
        elif argument == '/nopause':
            enable_pause = False
        elif argument == '/return':
            if (i+1 <= arg_count) and (sys.argv[i+1][0] != '/'):
                i = i+1
                ret_code = int(sys.argv[i])
        else:
            apperror(0, "Invalid argument - '"+argument+"'")
            sys.exit(22)
        i = i+1


def try_req(req_obj, con_timeout_local=0.0, returnerr=False):
    global con_timeout
    if con_timeout_local == 0.0:
        con_timeout_local = con_timeout

    try:
        resp = request.urlopen(req_obj, timeout=con_timeout_local)
    except Exception as err:
        print(err)
        if returnerr:
            return err
    else:
        return resp


def apperror(step, reason, needpause=True):
    print('\nException occured in step '+str(step)+':')
    print('\t'+reason+'\n')
    if needpause:
        pause()
    else:
        print('Exit in 3s...')
        time.sleep(3)
    sys.exit()


def write_history(start_time, data_dict):
    global cookie

    con = sqlite3.connect('csuwlan.db')
    cursor = con.cursor()
    rst = cursor.execute(
        "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='History'")
    if not rst.fetchall()[0][0] == 1:
        cursor.execute(
            '''CREATE TABLE History(
            Time DATETIME PRIMARY KEY NOT NULL,
            User VARCHAR(50) NOT NULL,
            IP VARCHAR(15) NOT NULL,
            IP_specified BOOLEAN NOT NULL,
            Total_flow NUMERIC(7,2) NOT NULL,
            Used_flow NUMERIC(7,2) NOT NULL,
            Surplus_flow NUMERIC(7,2) NOT NULL,
            Balance NUMERIC(5,2) NOT NULL,
            Update_time DATETIME NOT NULL,
            Cookie VARCHAR(255) NOT NULL);'''
        )

    part1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(cur_time))
    part2 = (cur_time - int(cur_time)) * 1000
    C1 = '%s.%03d' % (part1, part2)
    C2 = data_dict['accountID']
    C3 = data_dict['userIntranetAddress']
    C4 = False
    C5 = data_dict['totalflow']
    C6 = data_dict['usedflow']
    C7 = data_dict['surplusflow']
    C8 = data_dict['surplusmoney']
    C9 = data_dict['lastupdate']
    C10 = cookie
    values = [C1, C2, C3, C4, C5, C6, C7, C8, C9, C10]
    values = str(values)[1:-1]
    values = values.replace('True', '1')
    values = values.replace('False', '0')
    cursor.execute(
        "INSERT INTO History(Time, User, IP, IP_specified, Total_flow, Used_flow, Surplus_flow, Balance, Update_time, Cookie) " +
        "VALUES("+values+")"
    )
    con.commit()
    con.close()


def logout(post_header):
    con = sqlite3.connect('csuwlan.db')
    cursor = con.cursor()
    rst = cursor.execute(
        "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='History'")
    if rst.fetchall()[0][0] == 1:
        rst = cursor.execute("SELECT COUNT(*) FROM History")
        if rst.fetchall()[0][0] >= 1:
            rst = cursor.execute(
                "SELECT Time, User, IP, Cookie FROM History ORDER BY Time DESC LIMIT 0,1")
            records = rst.fetchall()[0]
            last_login_time = records[0]
            last_account = records[1]
            last_ip = records[2]
            last_cookie = records[3]
        else:
            apperror(1, 'No history record found.')
    else:
        apperror(1, 'Missing history record table.')

    post_header['Referer'] = 'http://61.137.86.87:8080/portalNat444/main2.jsp'
    post_header['Cookie'] = last_cookie
    post_data = 'brasAddress=59df7586&userIntranetAddress='+last_ip
    post_data = post_data.encode('utf-8')

    req = request.Request(url=logout_url, headers=post_header, data=post_data)
    resp = try_req(req, 10)

    if resp == None:
        apperror(2, 'Logout request posted, but failed to get response.')

    data_resp = json.loads(resp.read().decode('utf-8'))
    if data_resp['resultCode'] == '0':
        print('Successfully logged out.\n')
        print('Connection info:')
        print('%-18s%s' % ('   Account:', last_account))
        print('%-18s%s' % ('   Local IP:', data_resp['userIntranetAddress']))
        print('%-18s%s' % ('   IP:', data_resp['userAddress']))
        print('%-18s%s' % ('   Login time:', last_login_time))
        print('%-18s%s' % ('   Duration:', data_resp['time']))
        print('-'*43)
        print('')
    else:
        apperror(3, 'Unknown Error.\n'+str(data_resp))


def internet_test():
    global test_url, hard_timeout
    global location

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

    myhandler = MyRedirectHandler()
    myopener = request.build_opener(myhandler)
    request.install_opener(myopener)

    req_1 = request.Request(test_url)
    req_1.add_header('User-Agent', ua)
    while True:
        sub_thread = MyThread(try_req, (req_1,), True)
        sub_thread.start()
        sub_thread.join(hard_timeout)
        resp_1 = sub_thread.report
        if resp_1 == None:
            print(
                'Seems no connections established or network is unstable. System will retry in 3s.\n')
            time.sleep(3)
        else:
            break
    if resp_1.getcode() == 302:
        location = resp_1.getheader('location')
    else:
        apperror(1, 'Not the expected status code.')


def analyze_location():
    global url_pattern, test_succeed_redirection
    global location, ip

    if url_pattern in location:
        ip = location[location.find('wlanuserip=')+11:location.find('&')]
    elif location == test_succeed_redirection:
        apperror(1, 'Already have Internet access.', False)
    else:
        apperror(2, "Unsupported authentication page -'"+location+"'")


def get_cookie():
    global step3_max_retry, location
    global cookie

    req_2 = request.Request(location)
    req_2.add_header('User-Agent', ua)
    for ii in range(0, step3_max_retry):
        resp_2 = try_req(req_2)
        if resp_2 == None:
            if ii < step3_max_retry-1:
                print('Network is unstable. System will retry in 3s.\n')
                time.sleep(3)
            else:
                apperror(3, 'Reached maximum retry times. Exiting...')
        else:
            break
    if 'JSESSIONID=' in resp_2.getheader('Set-Cookie'):
        cookie = resp_2.getheader('Set-Cookie').split(';')[0]
    else:
        apperror(3, 'Failed to get cookie.')


def login(post_header, retry_when_unknown_err=False):
    global login_url, account, password, ip, cookie
    global data_resp_3

    post_header['Cookie'] = cookie
    post_str = 'accountID='+account+'&password='+password + \
        '&brasAddress=59df7586&userIntranetAddress='+ip
    post_data = parse.quote(post_str, safe='=&').encode('utf-8')
    req_3 = request.Request(url=login_url, headers=post_header, data=post_data)

    resp_3 = try_req(req_3, 10, True)
    if isinstance(resp_3, BaseException):

        apperror(4, 'Login request posted, but failed to get response.')

    raw_resp_3 = resp_3.read().decode('utf-8')
    data_resp_3 = json.loads(raw_resp_3)
    if data_resp_3['resultCode'] == '0':
        print('Successfully logged in.\n')
        print('Account info:')
        print('%-18s%s' % ('   Name:', data_resp_3['accountID']))
        print('%-18s%s' % ('   IP:', data_resp_3['userIntranetAddress']))
        print('%-18s%s' % ('   Total flow:', data_resp_3['totalflow']+'MB'))
        print('%-18s%s' % ('   Used flow:', data_resp_3['usedflow']+'MB'))
        print('%-18s%s' % ('   Surplus flow:',
                           data_resp_3['surplusflow']+'MB'))
        print('%-18s%s' % ('   Balance:', '￥'+data_resp_3['surplusmoney']))
        print('-'*43)
        print('Information updated at: ' + data_resp_3['lastupdate'])
        print('')
    elif data_resp_3['resultDescribe'] == '该账号已在线':
        print('\nException occured in step 4:')
        print(
            "\tServer returned error code ["+data_resp_3['resultCode'] + "]: '"+data_resp_3['resultDescribe']+"'\n")
        print('Attempting to logout last recorded session....')
        logout(base_post_header)
        print('Waiting for server refreshing account state.... 3s')
        time.sleep(3)
        print('Retrying login....')
        login(base_post_header, True)
    elif data_resp_3['resultDescribe'] == None and retry_when_unknown_err:
        print('Failed. Waiting for server refreshing account state.... 5s')
        time.sleep(5)
        print('\nRetrying login....')
        login(base_post_header, False)
    else:
        apperror(4, 'Unknown Error.\n\n'+str(data_resp_3))


def main():
    handle_args()
    if skip_main:
        sub()
        return
    if not 'location' in globals().keys():
        internet_test()
    analyze_location()
    get_cookie()
    login(base_post_header)
    if save_history:
        write_history(cur_time, data_resp_3)


def sub():
    if logout_mode:
        logout(base_post_header)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        ret_code = 130
    except Exception as err:
        print(err)
        ret_code = 255
    pause()
    sys.exit(ret_code)

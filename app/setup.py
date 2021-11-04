import ctypes
import os
import sys
import time

title = '数字中南自动登录脚本安装配置'
os.system('TITLE %s' % title)

uid = '%s\\%s' % (os.getenv('USERDOMAIN'), os.getenv('USERNAME'))
path_dir_of_script = os.path.dirname(os.path.abspath(__file__))
path_internal_python = path_dir_of_script+'\\lib_python\\python.exe'
cmd_add_schtask = 'schtasks /CREATE /TN "1_登录数字中南" /RU "%USERDOMAIN%\\%USERNAME%" /XML "schtask.xml"'
cmd_del_schtask = 'schtasks /DELETE /TN "1_登录数字中南" /F'
cmd_query_schtask = 'schtasks /QUERY /TN "1_登录数字中南" /FO TABLE 2>NUL'
cmd_create_shortcut_login = 'cscript WinLinkHelper.vbs /linkname:"登录数字中南" /target:"%s" /args:"%s"' % (
    path_internal_python, path_dir_of_script+'\\AutoLogin.py')
cmd_create_shortcut_logout = 'cscript WinLinkHelper.vbs /linkname:"登出数字中南" /target:"%s" /args:"%s,%s"' % (
    path_internal_python, path_dir_of_script+'\\AutoLogin.py', '/logout')
msg_overwrite = '你希望：覆盖(Y) / 保留已有版本(N) / 中断安装(A)'
msg_retry = '你希望：重试(Y) / 忽略然后继续(N) / 中断安装(A)'
text_schtask_xml = '''<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Date>2019-05-04T18:02:41.9924126</Date>
    <Author>%s</Author>
    <URI>\\FakeURI</URI>
  </RegistrationInfo>
  <Principals>
    <Principal id="Author">
      <UserId>FakeSID</UserId>
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>true</StopIfGoingOnBatteries>
    <ExecutionTimeLimit>PT1H</ExecutionTimeLimit>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <RestartOnFailure>
      <Count>3</Count>
      <Interval>PT1M</Interval>
    </RestartOnFailure>
    <IdleSettings>
      <StopOnIdleEnd>true</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <UseUnifiedSchedulingEngine>true</UseUnifiedSchedulingEngine>
  </Settings>
  <Triggers>
    <LogonTrigger>
      <UserId>%s</UserId>
    </LogonTrigger>
    <SessionStateChangeTrigger>
      <StateChange>SessionUnlock</StateChange>
      <UserId>%s</UserId>
    </SessionStateChangeTrigger>
    <EventTrigger>
      <Subscription>&lt;QueryList&gt;&lt;Query Id="0" Path="Microsoft-Windows-WLAN-AutoConfig/Operational"&gt;&lt;Select Path="Microsoft-Windows-WLAN-AutoConfig/Operational"&gt;*[System[Provider[@Name='Microsoft-Windows-WLAN-AutoConfig'] and EventID=8001]]&lt;/Select&gt;&lt;/Query&gt;&lt;/QueryList&gt;</Subscription>
    </EventTrigger>
  </Triggers>
  <Actions Context="Author">
    <Exec>
      <Command>pythonw</Command>
      <Arguments>%s\\Launcher.pyw</Arguments>
      <WorkingDirectory>%s</WorkingDirectory>
    </Exec>
  </Actions>
</Task>
''' % (uid, uid, uid, path_dir_of_script, path_dir_of_script)

text_launcher_config_py = '''# Configuration file for "Launcher.pyw"

################################################################################
#### Note: This is an executable script. Any illegal modification may cause ####
#### application crash or function unexpectedly. BE CAREFUL WHEN EDITING!!! ####
################################################################################

# Timeout setting for network connection test (Step 1)
con_timeout = 5.0
hard_timeout = 5.0

# URL settings for network connection test (Step 1)
test_url = 'http://www.baidu.com/'
test_succeed_redirection = 'https://www.baidu.com/'

# URL pattern for "CSU ChinaNet" Network (Step 2)
url_pattern = 'http://61.137.86.87:8080/portalNat444/AccessServices/bas.59df7586?wlanuserip='

# Settings for request header
ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'

# Path of python interpreter
path_of_python = r'%s'

# Time of monitoring WLAN interface after a succeed login
## Note: Win10 Version 1903 will automatically disconnect form 
##   the wireless access point that can not reach internet if 
##   user does not interact with the system notification related  
##   to it. This program will call Windows Net Shell (NETSH) and
##   reconnect to "CSU ChinaNet" access point if system close 
##   the connection in the following setted time.
wait_for_wlan_con_timeout = 20.0
monitor_wlan_if_timeout = 15.0
''' % (path_internal_python)

text_config_py = '''# Configuration file for "AutoLogin.py"

################################################################################
#### Note: This is an executable script. Any illegal modification may cause ####
#### application crash or function unexpectedly. BE CAREFUL WHEN EDITING!!! ####
################################################################################

# Timeout setting for network connection test (Step 1)
con_timeout = 5.0
hard_timeout = 5.0

# URL settings for network connection test (Step 1)
test_url = 'http://www.baidu.com/'
test_succeed_redirection = 'https://www.baidu.com/'

# URL pattern for "CSU ChinaNet" Network (Step 2)
url_pattern = 'http://61.137.86.87:8080/portalNat444/AccessServices/bas.59df7586?wlanuserip='

# Maximum retry times setting for getting cookie (Step 3)
step3_max_retry = 3

# Setting for whether pausing when application terminate
# Note: Use '/nopause' command argument to temporary disable pause
enable_pause = True

# Settings for history recording
# Note: Logout will not work if history recording is disabled
save_history = True
save_to_install_dir = True
# Be sure to uncomment the following line and assign a
# valid path if 'save_to_install_dir' is setted to 'False'
#history_db_dir = r'E:\\Database'

# Login and Logout URL for "CSU ChinaNet" Network
login_url = 'http://61.137.86.87:8080/portalNat444/AccessServices/login'
logout_url = 'http://61.137.86.87:8080/portalNat444/AccessServices/logout?'

# Account settings for "CSU ChinaNet" Network
account = 'sample'
password = 'rsa'

# Settings for request header
ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
base_post_header = {
    'Host': '61.137.86.87:8080',
    'User-Agent': ua,
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'http://61.137.86.87:8080',
    'Referer': 'http://61.137.86.87:8080/portalNat444/index.jsp',
    'Connection': 'keep-alive'
}

if __name__ == '__main__':
    import os
    import sys
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(os.path.abspath(os.curdir))
    import myrsa

    print('\\nAttention: Running this script may only modify account and password.')
    print('If you want to change other settings, please edit this file directly.')
    print('-'*30)
    new_account = input('account > ')
    new_account = new_account.strip()+'@zndx.inter'
    new_password = input('password> ')
    new_password = myrsa.encrypt('10001', 'a8a02b821d52d3d0ca90620c78474b78435423be99da83cc190ab5cb5b9b922a4c8ba6b251e78429757cf11cde119e1eacff46fa3bf3b43ef68ceb29897b7aa6b5b1359fef6f35f32b748dc109fd3d09f3443a2cc3b73e99579f3d0fe6a96ccf6a48bc40056a6cac327d309b93b1d61d6f6e8f4a42fc9540f34f1c4a2e053445', new_password)

    data = ''
    cur_file = os.path.abspath(__file__)
    bak_file = cur_file+'_bak.txt'
    with open(cur_file, 'r') as old:
        for line in old.readlines():
            if line[0:7] == 'account':
                line = "account = '"+new_account+"'\\n"
            elif line[0:8] == 'password':
                line = "password = '"+new_password+"'\\n"
            data += line
    if os.path.exists(bak_file):
        os.remove(bak_file)
    os.rename(cur_file, bak_file)
    with open(cur_file, mode='w+', encoding='utf-8') as new:
        new.writelines(data)
    print('Account information updated successfully.')
    print("Old settings backed up in file '%s'" % bak_file)
    input('\\nPress Enter to continue...')
'''


def get_str_time():
    cur_time = time.time()
    part1 = time.strftime('%H:%M:%S', time.localtime(cur_time))
    part2 = (cur_time - int(cur_time)) * 1000
    return('%s.%03d' % (part1, part2))


def rich_print(prompt, style='none'):
    if style == 'inf':
        print('[%s] %s: %s' % (get_str_time(), 'INF', prompt))
    elif style == 'war':
        print('[%s] %s: %s' % (get_str_time(), 'WAR', prompt))
    elif style == 'err':
        print('[%s] %s: %s' % (get_str_time(), 'ERR', prompt))
    else:
        print('   '+prompt.replace('\n', '\n   '))


def draw_center_msg(msg, mode):
    rows = os.get_terminal_size()[0]
    if mode == 0:
        msg = ' '+msg+' '
        left = (rows-len(msg))/2
        if isinstance(left, int):
            right = left
        else:
            left = int(left+0.5)
            right = left-1
        print('%s%s%s' % ('='*left, msg, '='*right))
    elif mode == 1:
        border_top = '#'*rows
        border_left = '#'*4
        spaces_left = (rows-len(border_left)*2-len(msg)*2)/2
        if isinstance(spaces_left, int):
            spaces_right = spaces_left
        else:
            spaces_left = int(spaces_left+0.5)
            spaces_right = spaces_left-1
        print(border_top)
        print('%s%s%s' % (border_left, ' '*(rows-len(border_left)*2), border_left))
        print('%s%s%s%s%s' % (border_left, ' '*spaces_left,
                              msg, ' '*spaces_right, border_left))
        print('%s%s%s' % (border_left, ' '*(rows-len(border_left)*2), border_left))
        print(border_top)
        print()
    elif mode == 2:
        print('-'*rows)


def run_external_cmd(cmd, read_stdout=False, auto_retry=0, succeed_code=0):
    retry_count = 0
    msg_begin = 'Begin of external command'
    msg_end = 'End of external command'
    print()
    draw_center_msg(msg_begin, 0)
    while True:
        if read_stdout:
            try:
                result = os.popen(cmd)
                draw_center_msg(msg_end, 0)
                print()
                return result.read()
            except Exception as err:
                draw_center_msg('', 2)
                rich_print("外部命令'%s'执行时出现致命错误，安装失败！\n详细信息：" % cmd, 'err')
                rich_print(err)
                terminate(False, 1)
        else:
            try:
                result = os.system(cmd)
                if result != succeed_code and retry_count < auto_retry:
                    retry_count += 1
                    draw_center_msg('', 2)
                    rich_print("外部命令'%s'执行时出现错误!" % cmd, 'err')
                    rich_print("开始第 %d of %d 次重试..." %
                               (retry_count, auto_retry), 'war')
                    draw_center_msg('', 2)
                    continue
                draw_center_msg(msg_end, 0)
                print()
                return result
            except Exception as err:
                draw_center_msg('', 2)
                rich_print("外部命令'%s'执行时出现致命错误，安装失败！\n详细信息：" % cmd, 'err')
                rich_print(err)
                terminate(False, 1)


def interact(prompt):
    while True:
        print()
        answer = input('===>%s\n===>' % prompt).strip().lower()
        if answer == 'y':
            break
        elif answer == 'n':
            break
        elif answer == 'a':
            break
        else:
            print('请输入有效的此选项！')
    print()
    return answer


def terminate(succeed=True, exitcode=0):
    if succeed:
        if exitcode == 130:
            rich_print('操作被用户中断。', 'inf')
        elif exitcode == 0:
            rich_print('操作成功完成！', 'inf')
    else:
        rich_print('由于不可修正的错误，操作提前终止！', 'inf')
    if IsWindows:
        print()
        os.system('PAUSE')
    else:
        input('\n按下回车键以继续...')
    sys.exit(exitcode)


def write_file(file, text, encoding):
    with open(file, 'w', encoding=encoding) as f:
        f.write(text)
        f.close()


def generate_config(name, content):
    if os.path.exists(name):
        rich_print("配置文件'%s'已经存在" % name, 'war')
        answer = interact(msg_overwrite)
        if answer == 'y':
            os.remove(name)
            rich_print("已删除文件'%s'" % os.path.abspath(name), 'inf')
        elif answer == 'n':
            rich_print("已保留原有配置文件'%s'" % name, 'inf')
            return
        elif answer == 'a':
            terminate(True, 130)
    write_file(name, content, 'UTF-8')
    rich_print("成功生成配置文件'%s'" % name, 'inf')


############################################################
############################################################
draw_center_msg(title, 1)
rich_print('数字中南自动登录脚本安装配置', 'inf')
rich_print("当前运行平台是'%s'" % sys.platform, 'inf')
IsWindows = sys.platform == 'win32'
if IsWindows:
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as err:
        rich_print("外部过程调用时出现致命错误，安装失败！\n详细信息：", 'err')
        rich_print(err)
        sys.exit(1)
    if is_admin == 0:
        rich_print('安装程序需要更高的权限，将于3秒后请求提权...', 'war')
        time.sleep(3)
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, os.path.abspath(__file__), None, 1)
        sys.exit(1)
    else:
        skip_schtask_add = False
else:
    rich_print('安装程序将跳过任务计划配置，原因：非Windows操作系统。', 'inf')
    skip_schtask_add = True


os.chdir(path_dir_of_script)
rich_print('准备生成配置文件...', 'inf')
generate_config('launcher_config.py', text_launcher_config_py)
generate_config('config.py', text_config_py)

if not skip_schtask_add:
    rich_print('查找已存在的任务计划...', 'inf')
    result = run_external_cmd(cmd_query_schtask, read_stdout=True)
    if result == '':
        pass
    else:
        rich_print("任务'1_登录数字中南'已经存在！", 'war')
        rich_print('任务信息如下：'+result)
        answer = interact(msg_overwrite)
        if answer == 'y':
            run_external_cmd(cmd_del_schtask, auto_retry=3)
        elif answer == 'n':
            skip_schtask_add = True
            rich_print('保留原有的任务计划.', 'inf')
        elif answer == 'a':
            terminate(True, 130)

if not skip_schtask_add:
    rich_print('尝试创建任务计划...', 'inf')
    write_file('schtask.xml', text_schtask_xml, 'UTF-16')
while not skip_schtask_add:
    if run_external_cmd(cmd_add_schtask) == 0:
        rich_print('任务计划创建成功！', 'inf')
        break
    else:
        rich_print('创建任务计划失败', 'err')
        answer = interact(msg_retry)
        if answer == 'y':
            continue
        elif answer == 'n':
            skip_schtask_add = True
            rich_print('跳过任务计划创建.', 'inf')
            continue
        elif answer == 'a':
            terminate(True, 130)

############################################################
############################################################
rich_print("运行'%s'以配置登录信息..." % os.path.abspath('config.py'), 'inf')
run_external_cmd('""%s" "%s""' % (path_internal_python,
                                  os.path.abspath('config.py')), auto_retry=3)

rich_print('准备创建快捷方式', 'inf')
run_external_cmd(cmd_create_shortcut_login, auto_retry=3, succeed_code=200)
run_external_cmd(cmd_create_shortcut_logout, auto_retry=3, succeed_code=200)

rich_print('已完成所有请求的操作！', 'inf')
terminate()
# Configuration file for "AutoLogin.py"

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
#history_db_dir = r'E:\Database'

# Login and Logout URL for "CSU ChinaNet" Network
login_url = 'http://61.137.86.87:8080/portalNat444/AccessServices/login'
logout_url = 'http://61.137.86.87:8080/portalNat444/AccessServices/logout?'

# Account settings for "CSU ChinaNet" Network
account = 'sample'
password = 'rsa'

# Settings for request header
ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
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
    import myrsa

    print('\nAttention: Running this script can only...')
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
                line = "account = '"+new_account+"'\n"
            elif line[0:8] == 'password':
                line = "password = '"+new_password+"'\n"
            data += line
    if os.path.exists(bak_file):
        os.remove(bak_file)
    os.rename(cur_file, bak_file)
    with open(cur_file, mode='w+', encoding='utf-8') as new:
        new.writelines(data)

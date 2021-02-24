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
account = 'n@zndx.inter'
password = '95714d7243b98e150ec015c53ecc1e0c6af6edc862eb698e616b9b9e878d22fae89594c5c5a9fd0dd7c4446c021ed0e35159fe0e44c5a586c2f4ca0c7f0c990d61e0fbee5275676a5403710b554fbc5eee9d72fcce6397e7683f0b8d7be79c8ba67eec00cc03f18210cc94373cd0f40fbaa020310e793c7b23d3a40e4a213347'

# Settings for request header
ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
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

    print('\nAttention: Running this script may only modify account and password.')
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
                line = "account = '"+new_account+"'\n"
            elif line[0:8] == 'password':
                line = "password = '"+new_password+"'\n"
            data += line
    if os.path.exists(bak_file):
        os.remove(bak_file)
    os.rename(cur_file, bak_file)
    with open(cur_file, mode='w+', encoding='utf-8') as new:
        new.writelines(data)
    print('Account information updated successfully.')
    print("Old settings backed up in file '%s'" % bak_file)
    input('\nPress Enter to continue...')

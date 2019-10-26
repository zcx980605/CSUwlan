# Configuration file for "Launcher.pyw"

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
ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'

# Path of python interpreter
path_of_python = r'.\lib_python\python.exe'

# Time of monitoring WLAN interface after a succeed login
## Note: Win10 Version 1903 will automatically disconnect form 
##   the wireless access point that can not reach internet if 
##   user does not interact with the system notification related  
##   to it. This program will call Windows Net Shell (NETSH) and
##   reconnect to "CSU ChinaNet" access point if system close 
##   the connection in the following setted time.
wait_for_wlan_con_timout = 20.0
monitor_wlan_if_timeout = 15.0
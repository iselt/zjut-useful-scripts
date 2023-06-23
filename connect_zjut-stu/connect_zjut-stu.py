import pywifi,time
from pywifi import const
 
def wifi_connect_status():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0] #acquire the first Wlan card,maybe not
 
    if iface.status() in [const.IFACE_CONNECTED,const.IFACE_INACTIVE]:
        print("WIFI 已连接")
        return 1
    else:
        print("WIFI 未连接")
    
    return 0
 
def scan_wifi():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
 
    iface.scan()
    time.sleep(1)
    basewifi = iface.scan_results()
 
    for i in basewifi:
        print("wifi scan result:{}".format(i.ssid))
        print("wifi device MAC address:{}".format(i.bssid))
        
    return basewifi
 
def connect_wifi(ssid, password):
    wifi = pywifi.PyWiFi()
    ifaces = wifi.interfaces()[0]
    print("使用网卡："+ifaces.name())               #输出无线网卡名称
 
    profile = pywifi.Profile()                          #配置文件
    profile.ssid = ssid                        #wifi名称
    
    if password != None:
        # 需要密码
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = password
    else:
        #不需要密码
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_NONE)
        profile.cipher = const.CIPHER_TYPE_NONE
 
    # ifaces.remove_all_network_profiles()                #删除其它配置文件
    tmp_profile = ifaces.add_network_profile(profile)   #加载配置文件
    ifaces.connect(tmp_profile)
    # 监测连接状态
    isok = False
    for i in range(6):
        if ifaces.status() == const.IFACE_CONNECTED:
            isok = True
            print('连接成功')
            break
        else:
            time.sleep(1)
 
    return isok
 
if wifi_connect_status() == 1:
    print("已经连接Zjut-stu")
else:
    print("正在连接Zjut-stu")
    connect_wifi("Zjut-stu",None)
    


import requests

# 获取本机ip（wlan）
import socket
my_ip_addr = socket.gethostbyname(socket.getfqdn(socket.gethostname()))

# 读取当前目录的account.txt，第一行为user_account，第二行为user_password，加入报错处理（文件不存在）
try:
    with open('account.txt', 'r') as f:
        user_account = f.readline().strip()
        user_password = f.readline().strip()
except FileNotFoundError:
    print('account.txt文件不存在，无法登录')
    time.sleep(2)
    exit()
    
    
    
print(f"登录账号：{user_account}")
# 发送以上请求
url=f'http://192.168.8.1:801/eportal/?c=Portal&a=login&callback=dr1003&login_method=1&user_account=%2C0%2C{user_account}&user_password={user_password}&wlan_user_ip='+my_ip_addr+'&wlan_user_ipv6=&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name=&jsVersion=3.3.3&v=791'
headers = {
    'Host': '192.168.8.1:801',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36',
    'Referer': 'http://192.168.8.1/',
    'cookie': 'PHPSESSID=tc1fb27hktn4dohl55nqh3clqk',
    'Connection': 'close'
}

r = requests.get(url, headers=headers)

if '\"result\":\"1\"' in r.text:
    print('登录成功')
elif '\"ret_code\":2' in r.text:
    print('已经登录')
else :
    print('登录失败')

time.sleep(2)

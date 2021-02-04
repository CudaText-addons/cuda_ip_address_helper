import os
import json
from urllib.request import urlopen
from cudatext import *

# 176.59.8.61 Russia
# 132.14.55.68 USA
# 132.14.55.68.32 Error
# wer::32d:43:21:ff::sa
# z8::0000:0000:0370
# 2001:4860:4860:0000:0000:0000:0000:8888
# 2001:0DB8:85A3:0000:0000:8A2E:0370:7334
# B8::0000:0000:0370z

ABOUT = '[IP Address Helper] '

def work(ip):
    # https://stackoverflow.com/questions/24678308/how-to-find-location-with-ip-address-in-python
    msg_status(ABOUT + 'Looking for IPv4...', True)
    url = 'https://ipinfo.io/' + ip + '/json'
    res = urlopen(url)
    msg_status('')
    if not res: return
    data = json.load(res)
    code = data.get('country', '?')
    return 'IP '+ip+': '+code

def detect_ip4(s,x):
    ipsymbols='1234567890.'
    symbols=', /;()[]{}\t'
    start=x
    end=x

    while start>=0:
        if s[start] in ipsymbols:
            start -= 1
        else:
            break
    while end<len(s):
        if s[end] in ipsymbols:
            end += 1
        else:
            break
    if start>-1:
        if not s[start] in symbols:
            return
    if len(s)>end:
        if not s[end] in symbols:
            return
    start+=1
    ip=s[start:end]
    parts=ip.split('.')
    if len(parts)!=4:
        return
    for i in parts:
        if len(i)>3:
            return
    res=work(ip)
    if res:
        msg_status(res)

'''
def detect_ip6(s,x):
    ipsymbols='1234567890abcdefABCDEF:'
    symbols=', /;()[]{}\t'
    start=x
    end=x
    while start>=0:
        if s[start] in ipsymbols:
            start -= 1
        else:
            break
    while end<len(s):
        if s[end] in ipsymbols:
            end += 1
        else:
            break
    lin=s[start+1:end]
    parts=lin.split(':')
    if 2<=len(parts)<=8:
        if start>=0:
            if not s[start] in symbols:
                return
        if end<len(s):
            if not s[end] in symbols:
                return
    if 2<=len(parts)<=8:
        res=work(lin)
        if res:
            msg_status(res)
'''

class Command:
    active = False

    def on_mouse_stop(self, ed_self, x, y):
        if not self.active:
            return
        res = ed.convert(CONVERT_PIXELS_TO_CARET,x,y)
        if res is None:
            return
        x,y = res
        if not (0<=y<ed_self.get_line_count()):
            return
        s=ed_self.get_text_line(y)
        if not (0<=x<len(s)):
            return
        detect_ip4(s,x)

    def toggle(self):
        self.active = not self.active
        ev = 'on_mouse_stop' if self.active else ''
        app_proc(PROC_SET_EVENTS, 'cuda_ip_address_helper;'+ev+';')
        msg_status(ABOUT+('Active' if self.active else 'Inactive'))

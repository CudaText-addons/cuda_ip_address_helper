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

def ip_country(ip):
    # https://stackoverflow.com/questions/24678308/how-to-find-location-with-ip-address-in-python
    url = 'https://ipinfo.io/' + ip + '/json'
    res = urlopen(url)
    if not res: return
    data = json.load(res)
    code = data.get('country', '?')
    return 'IP '+ip+': '+code

def ip4_country(overline,x):
    ipsymbols='1234567890.'
    symbols=', /;()[]{}\t'
    start=x
    end=x

    while start>=0:
        if overline[start] in ipsymbols:
            start -= 1
        else:
            break
    while end<len(overline):
        if overline[end] in ipsymbols:
            end += 1
        else:
            break
    if start>-1:
        if not overline[start] in symbols:
            return
    if len(overline)>end:
        if not overline[end] in symbols:
            return
    start+=1
    ip=overline[start:end]
    for i in ip.split('.'):
           if len(i)>3:
               return ''
    res=str(ip_country(overline[start:end]))
    if res:
        msg_status(res)

def ip6_country(overline,x):
    ipsymbols='1234567890abcdefABCDEF:'
    symbols=', /;()[]{}\t'
    start=x
    end=x
    while start>=0:
        if overline[start] in ipsymbols:
            start -= 1
        else:
            break
    while end<len(overline):
        if overline[end] in ipsymbols:
            end += 1
        else:
            break
    lin=overline[start+1:end]
    if 2<=len(lin.split(':'))<=8:
        if start>=0:
            if not overline[start] in symbols:
                return
        if end<len(overline):
            if not overline[end] in symbols:
                return
    if 2<=len(lin.split(':'))<=8:
        res=ip_country(lin)
        if res:
            msg_status(res)
        else:
            msg_status('IP: ?')
        return

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
        overline=ed_self.get_text_line(y)
        if not (0<=x<len(overline)):
            return
        #ipv6
        msg_status(ABOUT+'Looking for IPv6...', True)
        if not ip6_country(overline,x):
            #ipv4
            msg_status(ABOUT+'Looking for IPv4...', True)
            ip4_country(overline,x)

    def toggle(self):
        self.active = not self.active
        msg_status(ABOUT+('Active' if self.active else 'Inactive'))

import os
from cudatext import *

import urllib
from urllib import request

# 176.59.8.61 Russia
# 132.14.55.68 USA
# 132.14.55.68.32 Error
# wer::32d:43:21:ff::sa  
# ::1
def ip_country(ip):
    if not len(ip.split('.'))==4:
        return ''
    for i in ip.split('.'):
        if len(i)>3:
            return ''
    try:
        req = urllib.request.Request('http://smart-ip.net/geoip/'+ip+'/auto', headers={'User-Agent' : "Magic Browser"})
        con=urllib.request.urlopen(req)
        return 'IP: '+str(con.read()).split('Geo-Location for')[1].split('Country')[1].split('</td>')[1].split('>')[2].strip()
    except:
        return 'IP: ?'

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_ip_address_helper.ini')


class Command:

    def config(self):
        file_open(fn_config)
        
    def on_mouse_stop(self, ed_self, x, y):
        x,y = ed.convert(CONVERT_PIXELS_TO_CARET,x,y)
        if not (0<=y<ed_self.get_line_count()):
            return
        overline=ed_self.get_text_line(y)
        if not (0<=x<len(overline)):
            return
        symbols=', /;()[]{}'
        #ipv6
        ipsymbols='1234567890abcdef:'
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
        print(lin)
        if 2<=len(lin.split(':'))<=8:
            print('exit')
            res=ip_country(lin)
            if res:
              msg_status(ip_country(lin))
            else:
              msg_status('IP:?')
            return
        #ipv4
        print('trying to find ipv4')
        ipsymbols='1234567890.'
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
        res=str(ip_country(overline[start:end]))
        if res:
            msg_status(res)

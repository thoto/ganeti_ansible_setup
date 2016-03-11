def digit_to_char(digit):
    if digit < 10:
        return str(digit)
    return chr(ord('a') + digit - 10)

def str_base(number,base):
    if number < 0:
        return '-' + str_base(-number, base)
    (d, m) = divmod(number, base)
    if d > 0:
        return str_base(d, base) + digit_to_char(m)
    return digit_to_char(m)

def band(val_one,val_two,base=10):
    return str_base(int(val_one,base=base) & int(val_two,base=base),base)

def bor(val_one,val_two,base=10):
    return str_base(int(val_one,base=base) | int(val_two,base=base),base)

def revzone(value):
    ''' returns reverse zone file for given IP(v6/v4) network '''
    try:
        addr,prefix=value.split('/')
    except:
        addr,prefix=value,128

    v4split=addr.split('.')
    v6split=addr.split(':')

    res=''
    y=int(prefix)
    if len(v4split) > 1:
        for i in v4split:
            if y<=8 and y>0:
                i=str(int(i,10) & ~(2**(8-y)-1))
            elif y<=0 :
                return res+"in-addr.arpa"
            y-=8
            res=i+'.'+res
        return res+"in-addr.arpa"
    elif len(v6split) > 1:
        try:
            loidx=v6split.index('')
            v6split=v6split[:loidx]+['0']*(9-len(v6split))+v6split[loidx+1:]
        except:
            pass

        for i in v6split:
            for j in i.rjust(4,'0'):
                if y<=4 and y>0:
                    j=hex(int(j,16) & ~(2**(4-y)-1))[2:]
                elif y<=0:
                    return res+"ip6.arpa"
                y-=4
                res=j+'.'+res
        return res+"ip6.arpa"
    else:
        return False

class FilterModule(object):
    '''reverse zone and binary operations'''
    def filters(self):
        return {
            'band': band,
            'bor': bor,
            'revzone': revzone,
        }
# vim:ff=unix ts=4 sw=4 ai expandtab

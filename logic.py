import itertools, re


all_vars = ['cheetah','gazelle','savanna']
know = ['eats,cheetah,gazelle',
        'eats,cheetah,gazelle',
        'eats,cheetah,gazelle',
        'livesin,gazelle,savanna',
        'livesin,cheetah,savanna']    
rules = ['predator(X)=eats,any.X,any.Y and lives,any.X,savanna',
             'eatsall,X=eats,any.X,any.y,any.Z']
    
    #qs = gen(all_vars,know,rules[0])

"""def gen(all_vars,know,rule):
    fv,r = rule.split('=')
    sp = r.split(',')
    #print(sp)
    k = sp[0]
    combos = itertools.combinations_with_replacement(all_vars, len(sp)-1)
    c = list(combos)
    #print(c)

    x = [','.join([k]+list(y)) for y in c]
    y = [z in know for z in x]

    fv,r = rule.split('=')
    f,v = fv.split(',')

    for k in know:
        exec('def {}({}):\n\treturn ')"""


# istrue(['any.X','any.Y'],0,2,'eats')
def convrule(rule):
    fv, rest = rule.split('=')
    rest = rest.split(',')
    func = rest.pop(0)
    ll = len(rest)
    print(rest,0,ll,func)
    x = istrue(rest,0,ll,func)
    print(x)
    print(any(x))


# vtype: ['any.X','any.Y']
# vvalue: ['cheetah','gazelle']
# index: 1
# maxv: 2
# cq = 'eats,'

def compound(rule):
    r = re.split(' and | or ', rule)
    print(r)
    for rp in r:
        rparts = convrule(rp)
        print(rparts)
    
    return

def istrue(vtype, index, maxv, cq):
    if index < maxv:
        if vtype[index].startswith('any.'):
            res = []
            for v in all_vars:
                ret = istrue(vtype,index+1,maxv,cq+','+v)
                for r in ret:
                    if not r in res:
                        res.append(r)
                #res.append(istrue(vtype,index+1,maxv,cq+','+v))
            if any(res):
                return res
            else:
                return []
        elif vtype[index].startswith('all.'):
            res = []
            for v in all_vars:
                ret = istrue(vtype,index+1,maxv,cq+','+v)
                for r in ret:
                    if not r in res:
                        res.append(r)
                #res.append(istrue(vtype,index+1,maxv,cq+','+v))
            if all(res):
                return res
            else:
                return []
        else:
            res = []
            #res = [istrue(vtype,index+1,maxv,cq+','+vtype[index])]
            ret = istrue(vtype,index+1,maxv,cq+','+vtype[index])
            for r in ret:
                if not r in res:
                    res.append(ret)
            return res
    elif index == maxv:
        if cq in know:
            return cq
        else:
            return []

if __name__ == '__main__':
    #print(istrue(['any.X','any.Y'],0,2,'eats'))
    compound(rules[0])
    #convrule(rules[1])

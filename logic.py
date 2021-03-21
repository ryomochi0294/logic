import itertools, re


all_vars = ['cheetah','gazelle','savanna']
know = ['eats,cheetah,gazelle',
        'eats,cheetah,gazelle',
        'eats,cheetah,gazelle',
        'livesin,gazelle,savanna',
        'livesin,cheetah,savanna']    
rules = ['predator(X)=eats,any.X,any.Y and lives,any.X,savanna',
             'eatsall,X=eats,any.X,any.y,any.Z']


# istrue(['any.X','any.Y'],0,2,'eats')
# Convert a string containing a rule into the format used by istrue()
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
        # If any of the child functions returns true, then return that solution.
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
        # Every child function must return a solution or it is false.
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
        # Fixed variable like eats,X.any,gazelle
        else:
            res = []
            #res = [istrue(vtype,index+1,maxv,cq+','+vtype[index])]
            ret = istrue(vtype,index+1,maxv,cq+','+vtype[index])
            for r in ret:
                if not r in res:
                    res.append(ret)
            return res
    # Evaluate when you reach the max depth
    elif index == maxv:
        if cq in know:
            return cq
        else:
            return []

if __name__ == '__main__':
    #print(istrue(['any.X','any.Y'],0,2,'eats'))
    compound(rules[0])
    #convrule(rules[1])

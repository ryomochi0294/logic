import itertools, re


all_vars = ['cheetah','gazelle','savanna','alligator']
know = ['eats,cheetah,gazelle',
        'eats,alligator,alligator',
        'eats,alligator,gazelle',
        'eats,alligator,savanna',
        'eats,alligator,cheetah',
        'eats,alligator,cheetah,gazelle',
        
        'livesin,gazelle,savanna',
        'livesin,cheetah,savanna']    
rules = [
    'predator,X=eats,any.X,any.Y',
    'eatsall,X=eats,any.X,all.y',
    'thirdtier,X=eats,any.X,any.Y,any.Z'
]


# istrue(['any.X','any.Y'],0,2,'eats')
# Convert a string containing a rule into the format used by istrue()
def evaluate_rule(rule):
    fv, rest = rule.split('=')
    rest = rest.split(',')

    # func = eats
    func = rest.pop(0)

    new_knowledge = []
    results = evaluate_phrase(func, rest, 0, len(rest))

    for result in results:
        if result == []:
            continue
        func, var_being_updated = fv.split(',')
        location_in_query = rest.index('any.'+var_being_updated)
        new = '{},{}'.format(func,result.split(',')[location_in_query+1])
        if not new in new_knowledge:
            new_knowledge.append(new)
    return new_knowledge

# eats,any.X,any.Y
# current_query = 'eats' -> 'eats,cheetah'
# vtype: ['any.X','any.Y']
# vvalue: ['cheetah','gazelle']
# index: 0
# maxv: 2
def evaluate_phrase(current_query, vtype, index, maxv):
    if index < maxv:
        res = []
        for v in all_vars:
            ret = evaluate_phrase(current_query + ',' + v, vtype, index+1, maxv)
            for r in ret:
                if not r in res:
                    res.append(r)
        if vtype[index].startswith('all.') and not all(res):
            return []
        return res

    # Evaluate when you reach the max depth
    elif index == maxv:
        if current_query in know:
            #print(cq)
            return [current_query]
        else:
            return [[]]

def compound(rule):
    r = re.split(' and | or ', rule)
    print(r)
    for rp in r:
        rparts = convrule(rp)
        print(rparts)
    
    return

if __name__ == '__main__':
    #print(istrue(['any.X','any.Y'],0,2,'eats'))
    print(evaluate_rule(rules[0]))
    print(evaluate_rule(rules[1]))
    print(evaluate_rule(rules[2]))
    #convrule(rules[1])

import itertools, re

all_vars = ['grass','cheetah','gazelle','savanna','baboon','crocodile']

know = [
    'plant,grass',
    'animal,gazelle',
    'animal,cheetah',
    'animal,crocodile',
    'animal,baboon',

    'eats,gazelle,grass',
    'eats,baboon,grass',
    'eats,baboon,gazelle',
    'eats,cheetah,gazelle',
    'eats,cheetah,zebra',
    'eats,crocodile,gazelle',
    'eats,crocodile,baboon',
    'eats,crocodile,cheetah',
    'eats,crocodile,crocodile',
        
    'livesin,gazelle,savanna',
    'livesin,zebra,savanna',
    'livesin,cheetah,savanna',
    'livesin,crocodile,savanna'
]

rules = [
    'herbivore,X=eats,X,Y and plant,Y', # works
    'carnivore,X=eats,X,Y and animal,Y', # works
    'thirdtier,X=eats,X,Y and eats,Y,Z', # works
    'omnivore,X=eats,X,Y and animal,Y and eats,X,Z and plant,Z', # works
    'doesnoteat,X=~eats,X,Y',
    'notpicky,X=eats,X,all.Y and animal,Y',
    'naturalpredator,X=eats,X,Y and livesin,X,Z and livesin,X,Z',
    'topofthefoodchain,X=~eats,all.Y,X'
]

def evaluate_compound_and(compound):
    fv, rest = compound.split('=')
    phrases = rest.split(' and ')
    vars_ = []
    for p in phrases:
        parts = p.split(',')
        del parts[0]
        for part in parts:
            if not part in vars_:
                vars_.append(part)
    print(vars_)

    combos = itertools.permutations(all_vars, len(vars_))
    for x in combos:
        p = rest
        for y in range(len(x)):
            p = p.replace(vars_[y], x[y])
        #print(p)

        p = '\'' + p.replace(' and', '\' in know and') + '\' in know'
        p = p.replace('and ',' and \'')
        if eval(p) == True:
            print(p)

            soln = fv
            for y in range(len(x)):
                soln = soln.replace(vars_[y], x[y])
                if not soln in know:
                    print('adding {}'.format(soln))
                    know.append(soln)
    

# predator,X=eats,X,Y and plant,Y
def evaluate_rule(rule):
    fv, rest = rule.split('=') # fv=predator,X
    rest = rest.split(',')
    new_knowledge = []
    # evaluate_phrase('eats', ['any.X','any.Y'], 0, 2)
    results = evaluate_phrase(rest.pop(0), rest, 0, len(rest))

    for result in results:
        if result == []:
            continue
        func, var_being_updated = fv.split(',')
        location_in_query = rest.index(var_being_updated)
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
        if index > 0:
            return res
        else:
            result = []
            for r in res:
                if r != []:
                    result.append(r)
            return result

    # Evaluate when you reach the max depth
    elif index == maxv:
        if current_query in know:
            #print(cq)
            return [current_query]
        else:
            return [[]]

if __name__ == '__main__':
    evaluate_compound_and(rules[3])
    #print(evaluate_phrase('eats', ['X','all.Y'],0,2))
    #print(evaluate_rule(rules[0]))
    #print(evaluate_rule(rules[1]))
    #print(evaluate_rule(rules[2]))
    #convrule(rules[1])

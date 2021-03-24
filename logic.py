import re

all_vars = ['grass','cheetah','gazelle','savanna','crocodile']

know = [
    'plant,grass',
    'animal,gazelle',
    'animal,cheetah',
    'animal,crocodile',

    'eats,gazelle,grass',
    'eats,cheetah,gazelle',
    'eats,crocodile,gazelle',
    'eats,crocodile,cheetah',
        
    'livesin,gazelle,savanna',
    'livesin,cheetah,savanna',
    'livesin,crocodile,savanna'
]

rules = [
    'herbivore,X=eats,X,Y and plant,Y',
    'carnivore,X=eats,X,Y and animal,Y',
    'notpicky,X=eats,X,all.Y and animal,Y',
    'omnivore,X=eats,X,Y and animal,Y and eats,X,Z and plant,Z',
    'naturalpredator,X=eats,X,Y and livesin,X,Z and livesin,X,Z',
    'topofthefoodchain,X=~eats,all.Y,X'
]

def evaluate_compound(compound):
    func, rest = compound.split('=')
    phrases = re.split(' and | or ', rest)
    solns = []

    # herbivore,x=eats,X,Y and plant,Y
    # phrase 1: eats,X,Y, phrase 2: plant,Y
    for phrase in phrases:
        # func = eats or plant
        # variables = X,Y or Y
        func, variables = phrase.split(',', 1)
        variables = variables.split(',')
        # evaluate the phrase
        nk = evaluate_phrase(func, variables, 0, len(variables))

        solns_phrase = []
        for n in nk:
            n = n.split(',', 1)[1]
            n = n.split(',')

            # if eats,X,Y returns eats,cheetah,gazelle
            # put it into format:
            # {
            #   'X': cheetah,
            #   'Y': gazelle
            # }
            new_soln = {}
            for x in range(len(n)):
                new_soln[variables[x]] = n[x]
            # Append to a list of all solutions for the phrase.
            solns_phrase.append(new_soln)
        # Then, append to a list of all solutions.
        solns.append(solns_phrase)

    # Now, the task is to find solution(s) to the phrase for which
    # all variables have the same value.

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

def compound(rule):
    r = re.split(' and | or ', rule)
    print(r)
    for rp in r:
        rparts = convrule(rp)
        print(rparts)
    
    return

if __name__ == '__main__':
    evaluate_compound(rules[0])
    #print(evaluate_phrase('eats', ['X','Y'],0,2))
    #print(evaluate_rule(rules[0]))
    #print(evaluate_rule(rules[1]))
    #print(evaluate_rule(rules[2]))
    #convrule(rules[1])

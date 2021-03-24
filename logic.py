import itertools, re

all_vars = ['grass','cheetah','gazelle','savanna','zebra','crocodile']

know = [
    'plant,grass',
    'animal,gazelle',
    'animal,cheetah',
    'animal,crocodile',

    'eats,gazelle,grass',
    'eats,zebra,grass',
    'eats,cheetah,gazelle',
    'eats,cheetah,zebra',
    'eats,crocodile,gazelle',
    'eats,crocodile,zebra',
    'eats,crocodile,cheetah',
        
    'livesin,gazelle,savanna',
    'livesin,zebra,savanna',
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
    all_vars_here = []

    # herbivore,x=eats,X,Y and plant,Y
    # phrase 1: eats,X,Y, phrase 2: plant,Y
    for phrase in phrases:
        # func = eats or plant
        # variables = X,Y or Y
        func, variables = phrase.split(',', 1)
        variables = variables.split(',')
        for var in variables:
            if not var in all_vars_here:
                all_vars_here.append(var)
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
            #   'Y': gazelle,
            #   'phrase': 0
            # }
            new_soln = {}
            for x in range(len(n)):
                new_soln[variables[x]] = n[x]
            new_soln['phrase'] = phrase
            # Append to a list of all solutions for the phrase.
            solns_phrase.append(new_soln)
        # Then, append to a list of all solutions.
        for p in solns_phrase:
            solns.append(p)
        #solns.append(solns_phrase)

    #print(solns)    
    # Now, the task is to find solution(s) to each phrase for which
    # all variables have the same value.
    #first = solns[0]
    #del solns[0]

    fin = resolve_and(all_vars_here, solns, len(phrases))
    print(fin)

# Find all combinations of dicts such that there are no variable conflicts and
# all variables are included.
def resolve_and(all_vars, solns, total_phrases):
    # Create a list of all combinations of given solutions.
    all_combos = []
    for n in range(1, len(solns)+1):
        for v in itertools.combinations(solns, n):
            all_combos.append(v)
    print(len(all_combos))

    valid = []
    for possible in all_combos:
        var_values = {}
        phrases = []
        for v in all_vars:
            var_values[v] = []
            #print(v)
        for soln in possible:
            for v in soln:
                if v != 'phrase':
                    if soln[v] not in var_values[v]:
                        var_values[v].append(soln[v])
            if soln['phrase'] not in phrases:
                phrases.append(soln['phrase'])

        max_len_var_vals = max(len(var_values[vt]) for vt in var_values)
        if max_len_var_vals == 1 and len(phrases) == total_phrases:
            print('valid solution', possible)

            soln = {}
            for x in possible:
                soln.update(x)
            del soln['phrase']
            valid.append(soln)
            #valid.append(possible)
            #print(var_values)
            #print(len(phrases))
        #return
    
    return valid

    """a
    valid = []
    for i in range(len(solns) - 1):
        phrases_had = []
        possible = solns[i]
        for j in range(i + 1, len(solns)):
            compatible = True
            for key in solns[i]:
                print(key)
                if key != 'phrase' and key in solns[j] and solns[i][key] != solns[j][key]:
                    compatible = False
            if compatible:
                possible.update(solns[j])
        


        continue
        for j in range(i + 1, len(solns)):
            compatible = True
            copy1 = possible.copy()
            for key in solns[j]:
                if copy1[key] != solns[j][key] and key != 'phrase':
                    compatible = False

            if compatible:
                if not solns[j]['phrase'] in phrases_had:
                    phrases_had.append(solns[j]['phrase'])
                possible.update(solns[j])

        does_have_all_vars = True
        for v in all_vars_here:
            if not v in possible:
                does_have_all_vars = False
        if does_have_all_vars:
            #print('all_vars={}'.format(possible))
            #print(len(phrases_had))
            valid.append(possible)

        #if len(phrases_had) == len(phrases) and does_have_all_vars:
            #valid.append(possible)"""
    

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

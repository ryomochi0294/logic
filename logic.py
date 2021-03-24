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
    fv, rest = compound.split('=')
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
    print('func=', fv)
    for solution in fin:
        new_knowledge = fv
        for var in solution:
            new_knowledge = new_knowledge.replace(var, solution[var])
        print(new_knowledge)
        if not new_knowledge in know:
            know.append(new_knowledge)

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
        # Create a dict containing all the values of the variables in a given
        # combination:
        # {X: [], Y: []}
        var_values = {}
        phrases = []
        for v in all_vars:
            var_values[v] = []

        # Add the value for each variable to its list, so:
        # {X: ['zebra'], Y:['grass']}
        for soln in possible:
            for v in soln:
                if v != 'phrase':
                    if soln[v] not in var_values[v]:
                        var_values[v].append(soln[v])
            if soln['phrase'] not in phrases:
                phrases.append(soln['phrase'])

        # Each variable should have exactly one value, meaning they are all
        # the same. Also, the number of unique phrases should equal the total
        # number of phrases in our equation. So for
        # herbivore,X=eats,X,Y and plant,Y
        # We have 2 phrases.
        # A valid solution must 1 have value for each variable and include
        # both phrases.
        max_len_var_vals = max(len(var_values[vt]) for vt in var_values)
        min_len_var_vals = min(len(var_values[vt]) for vt in var_values)
        if max_len_var_vals == 1 and min_len_var_vals == 1 and len(phrases) == total_phrases:
            #print('valid solution', possible)

            soln = {}
            for x in possible:
                soln.update(x)
            del soln['phrase']
            valid.append(soln)
        # In this case the solutions are gazelle,grass and zebra,grass.
    
    return valid
    

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

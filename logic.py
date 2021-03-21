import itertools

def main2():
    all_vars = ['cheetah','gazelle','savanna']
    know = ['eats,cheetah,gazelle','livesin,gazelle,savanna',
                 'livesin,cheetah,savanna']
    rules = ['predator,X=eats,X,any.Y','eatsall,X=eats,X,all.y']
    
    #query = 'predator,cheetah'
    #query2 = 'predator,gazelle'
    #print('Cheetah is predator: {}'.format(check2(all_vars,know,rules,query)))
    #print('Gazelle is predator: {}'.format(check2(all_vars,know,rules,query2))
    #print(eval2(know, 'eats,cheetah,gazelle'))
    #print(eval2(know, 'eats,gazelle,cheetah'))
    #print(query_gen(all_vars, know, rules[0]))
    print(generate(all_vars, know, rules[0]))


#def check2(know, rules, query):
    # define functions


def generate(all_vars, know, rule):
    prov, cond = rule.split('=')
    func, var = prov.split(',', 1)

    conditional_function, rest = cond.split(',', 1)
    first_var, rest = rest.split(',', 1)
    rest = rest.split(',')

    all_queries = []
    # Checking X
    for var in all_vars:
        query = conditional_function + ',' + var
        combinations = itertools.combinations(all_vars, len(rest))
        for combination in combinations:
            query_test = ','.join([query]+list(combination))
            all_queries.append(query_test)
    return all_queries

def construct(know, rules):
    while True:
        did_change = False

        for rule in rules:
            results = generate(know, rule)
            if results != []:
                did_change = True

        if not did_change:
            return False

def eval2(know, stmt):
    return stmt in know

if __name__ == '__main__':
    main2()

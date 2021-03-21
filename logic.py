def main2():
    all_vars = set(['cheetah','turtle','swamp'])
    rules = set(['eats(cheetah,gazelle)','livesin(gazelle,savanna)',
                 'livesin(cheetah','savanna'),
                'predator(X,Y,Z)=eats(X,Y) and livesin(X,Z) and livesin(Y,Z)])
    evals = set(['predator(X,Y)=eats(X,Y)'])

def check_rule(all_vars, knowledge_base, rule):
    for var in all_vars:
        exec('%s = %s' % (var, var in knowledge_base))
    cond, prov = rule.split('->')
    return eval(cond)

def main():
    all_vars = set(['T','B','cat','F'])
    know = set('T')
    rules = set(['T or B->cat','cat->F'])
    checked = set()

    while True:
        did_change = False
        for rule in rules:
            result = check_rule(all_vars, know, rule)
            if result == True:
                cond, prov = rule.split('->')
                if prov == 'F':
                    return True
                know.add(prov)
                checked.add(rule)
                did_change = True

        if not did_change:
            return False

        for rule in checked:
            if rule in rules:
                rules.remove(rule)

if __name__ == '__main__':
    print(main())

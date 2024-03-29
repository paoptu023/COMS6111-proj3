import sys
import csv
import operator
from itertools import combinations, permutations

def init():
    # extract all large itemsets with size of 1 and calculate the support metric
    cache = {}
    l1 = []
    for t in database:
        for item in t:
            if len(item) == 0:
                continue
            if item not in cache:
                cache[item] = 0
            cache[item] += 1
    for item in sorted(cache.keys()):
        cur_supp = float(cache[item])/N
        if cur_supp >= min_supp:
            item_sets[(item,)] = cur_supp
            l1.append((item,))
        else:
            cache.pop(item)
    return l1


def apriori_gen(l, k):
    # take all large (k-1)-itemsets and return a superset of all large k-itemsets
    c_k = []
    helper_set = set(l)
    for s in l:
        helper_set.add(s)
    # join-step
    for p, q in combinations(l, 2):
        if p[:k-3] == q[:k-3]:
            new_tuple = list(p)
            new_tuple.append(q[k-2])
            c_k.append(tuple(sorted(new_tuple))) 
    # prune-step
    for c in c_k:
        for sub in combinations(c, k-1):
            if sub not in helper_set:
                c_k.remove(c)
                break
    return c_k


def get_l(c_k, k):
    cache = {}
    # count the frequency
    helper_set = set()
    for c in c_k:
        helper_set.add(c)

    for t in database:
        c_t = set()
        for i in combinations(t, k):
            c_t.add(tuple(sorted(i)))

        for c in c_t.intersection(helper_set):
            if c not in cache:
                cache[c] = 1.0
            else:
                cache[c] += 1
    # calculate support and generate l_k
    l = []
    for c in sorted(cache.keys()):
        cur_supp = cache[c]/N
        if cur_supp >= min_supp:
            item_sets[c] = cur_supp
            l.append(c)
    return l


def apriori():
    # generate all large itemsets
    # l -- list type, is a table, each row is a tuple
    l = init()
    k = 2
    while len(l) != 0:
        c_k = apriori_gen(l, k)
        l = get_l(c_k, k)
        k += 1


def generate():
    # generate high-confidence rules
    rules = {}
    for itemset in item_sets.keys():
        if len(itemset) == 1:
            continue
        for item in itemset:
            LHS = list(itemset)
            LHS.remove(item)
            LHS_supp = item_sets[tuple(LHS)]
            RHS_and_LHS_supp = item_sets[itemset]
            if LHS_supp > 0:
                cur_conf = RHS_and_LHS_supp/LHS_supp
                RHS = []
                RHS.append(item)
                if cur_conf >= min_conf:
                    temp = {}
                    temp['conf'] = cur_conf
                    temp['supp'] = item_sets[itemset]
                    key = '[' + ', '.join(LHS) + '] => '
                    key += '[' + str(RHS[0]) + ']'
                    rules[key] = temp
    return rules

if __name__ == "__main__":
    csvin = sys.argv[1]
    min_supp = float(sys.argv[2])
    min_conf = float(sys.argv[3])

    f = open(csvin, 'r')
    data = [tuple(line) for line in csv.reader(f)]
    
    # database -- contains all transactions, a table, each row is a transaction (in tuple format)
    database = set()
    for t in data:
        database.add(t)

    # the number of transactions
    N = len(database)

    # item_sets -- contains all large itemsets with their support
    item_sets = {}

    # calculate all large itemsets
    apriori()
    output = open('output.txt', 'w')

    print '====== Frequent itemsets (min_sup =', min_supp*100, '%) ======'
    output.write('====== Frequent itemsets (min_sup =' + str(min_supp*100) + '%) ======' + '\n')
    for item_set in sorted(item_sets.items(), key=operator.itemgetter(1), reverse=True):
        print '       [' + ', '.join(item_set[0]) + '] -- ', item_set[1]*100, '%'
        output.write('       [' + ', '.join(item_set[0]) + '] -- ' + str(item_set[1]*100) + '%' + '\n')


    # extract rules
    rules = generate()
    sorted_rules = sorted(rules.items(), key=lambda x:operator.getitem(x[1], 'conf'), reverse=True)

    print ''
    print '====== High-confidence association rules (min_conf =', min_conf*100, '%) ======'
    output.write('\n')
    output.write('====== High-confidence association rules (min_conf =' + str(min_conf*100) + '%) ======' + '\n')
    for rule in sorted_rules:
        print '       ' + rule[0] + ' -- ' + '(Conf:', rule[1]['conf']*100,'%  Supp:', rule[1]['supp']*100,'%)'
        output.write('       ' + rule[0] + ' -- ' + '(Conf:' + str(rule[1]['conf']*100) + '%  Supp:' + str(rule[1]['supp']*100) + '%)' + '\n')

    output.close()

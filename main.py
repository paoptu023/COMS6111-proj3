import sys
import csv
from itertools import combinations, permutations

def init():
    # extract all large itemsets with size of 1 and calculate support metric
    cache = {}
    l1 = []
    for t in database:
        for item in t:
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
            c_k.append(tuple(sorted(new_tuple))) # sort is important
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
                    key = '[' + ','.join(LHS) + '] => '
                    key += '[' + str(RHS[0]) + ']'
                    rules[key] = temp
    return rules

if __name__ == "__main__":
    #csvin = sys.argv[0]
    #min_supp = float(sys.argv[1])
    #min_conf = float(sys.argv[2])

    csvin = 'test.csv'
    min_supp = 0.7
    min_conf = 0.8

    f = open(csvin, 'r')
    data = [tuple(line) for line in csv.reader(f)]
    print data

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
    print '====== Frequent itemsets (min_sup =', min_supp*100, '%) ======'
    for item_set in item_sets:
        print '       [' + ','.join(item_set) + '] -- ', item_sets[item_set]*100, '%'

    # extract rules
    rules = generate()
    print ''
    print '====== High-confidence association rules (min_conf =', min_conf*100, '%) ======'
    for rule in rules.keys():
        print '       ' + rule + ' -- ', '(Conf:', rules[rule]['conf']*100,'%  Supp:', rules[rule]['supp']*100,'%)'
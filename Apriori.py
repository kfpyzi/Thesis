import argparse
from itertools import chain, combinations


#OPENING THE DATA
def open_data(filename):
    f = open(filename, 'rU')
    for l in f:
        l = l.strip().rstrip(',')
        row = frozenset(l.split(','))
        yield row

def itemset_from_data(data):
    itemset = set()
    transaction_list = list()
    for row in data:
        transaction_list.append(frozenset(row))
        for item in row:
            if item:
                itemset.add(frozenset([item]))
    return itemset, transaction_list


def itemset_support(transaction_list, itemset, min_support=0):
    len_transaction_list = len(transaction_list)
    l = [
        (item, float(sum(1 for row in transaction_list if item.issubset(row))) / len_transaction_list)
        for item in itemset
    ]
    return dict([(item, support) for item, support in l if support >= min_support])


def freq_itemset(transaction_list, c_itemset, min_support):
    f_itemset = dict()

    k = 1
    while True:
        if k > 1:
            c_itemset = joinset(l_itemset, k)
        l_itemset = itemset_support(transaction_list, c_itemset, min_support)
        if not l_itemset:
            break
        f_itemset.update(l_itemset)
        k += 1

    return f_itemset

def getRules(f_itemset, min_confidence):
    rules = list()
    for item, support in f_itemset.items():
        if len(item) > 1:
            for A in subsets(item):
                B = item.difference(A)
                if B:
                    A = frozenset(A)
                    AB = A | B
                    confidence = float(f_itemset[AB]) / f_itemset[A]
                    lift = float(f_itemset[AB]) / (f_itemset[A] * f_itemset[B])
                    if confidence >= min_confidence:
                        rules.append((A, B, confidence,lift))
    return rules, f_itemset

def joinset(itemset, k):
    return set([i.union(j) for i in itemset for j in itemset if len(i.union(j)) == k])


def subsets(itemset):
    return chain(*[combinations(itemset, i + 1) for i, a in enumerate(itemset)])

# APRIORI ALGORITHM

def apriori_algorithm(data, min_support, min_confidence):
    # Get first itemset and transactions
    itemset, transaction_list = itemset_from_data(data)

    # Get the frequent itemset
    f_itemset = freq_itemset(transaction_list, itemset, min_support)

    # Association rules
    return getRules(f_itemset, min_confidence)

# PRINT THE FREQUENT ITEMSET AND ASSOCIATION RULES
def print_result(rules: object, f_itemset: object) -> object:
    rulesnew = []

    ant = []
    cons = []
    conf = []
    liftt = []
    #print('--Frequent Itemset--')
    #for item, support in sorted(f_itemset.items(), key=lambda item_support: item_support[0]):
       # print('ITEMS: {} : '.format(tuple(item)), end='')
       # print('{}'.format(round(support, 4)))

   # print('')
    #print('--Rules--')
    for A, B, confidence,lift in sorted(rules, key=lambda A_B_confidence: A_B_confidence[0]):
        #print('RULES: {} => {} : {}'.format(tuple(A), tuple(B), round(confidence, 4)))
        #rulesnew.append('RULES: {} => {} : {}'.format(tuple(A), tuple(B), round(confidence, 5),round(lift,3)))
        ant.append(tuple(A))
        cons.append(tuple(B))
        conf.append(round(confidence,4))
        liftt.append(round(lift,3))
    return ant,cons,conf,liftt
# MAIN METHOD
def mine(csv):
    # options = parse_options()

    # MUST BE COMPUTED
    default_support = 0.014



    default_confidence = 0.9

    ''' The CSV file 
        
        data2.csv is just a sample file, can be changed
    '''
    data = open_data(csv)
    
    '''' APRIORI ALGORITHM AND PRINT'''
    rules, itemset = apriori_algorithm(data, default_support, default_confidence)
    return print_result(rules, itemset)




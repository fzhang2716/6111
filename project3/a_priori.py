import csv
import sys
from itertools import chain, combinations
import pandas as pd

def get_L1(filename, min_sup, all_supports):
    
    C1, L1, transactions, item_dict = set(), set(), [], {}
	
    with open(filename, mode='r', encoding='utf-8-sig') as f:
        data = csv.reader(f)

        for line in data:
            line = list(filter(None, line))
            transactions.append(set(line))
            for item in line:
                if len(item) != 0:
                    C1.add(frozenset([item]))
    
    for item in C1:
        for trans in transactions:
            if item.issubset(trans):
                if item not in item_dict:
                    item_dict[item] = 0
                if item not in all_supports:
                    all_supports[item] = 0
                item_dict[item] += 1
                all_supports[item] += 1

    for item in item_dict.items():
        key, value = item
        item_support = float(value / len(transactions))
        if item_support >= min_sup:
            L1.add(key)

    return L1, transactions, all_supports

def apriori_generation(Lk, k):

    Ck = set()
    # join
    for p in Lk:
        for q in Lk:
            if len(p.union(q)) == k:
                joint_item = p.union(q)
                Ck.add(joint_item)
    
    # prune
    removed_Ck = Ck.copy()
    for c in Ck:
        subsets = combinations(c, k-1)
        for subset in subsets:
            if frozenset(subset) not in Lk:
                removed_Ck.remove(c)
                break

    return removed_Ck

def compute_supports(transactions, Ck, all_supports):

    Ck_supports = {}

    for c in Ck:
        for trans in transactions:
            if c.issubset(trans):
                if c not in Ck_supports:
                    Ck_supports[c] = 0
                if c not in all_supports:
                    all_supports[c] = 0
                Ck_supports[c] += 1
                all_supports[c] += 1

    return Ck_supports


def apriori(filename, min_sup, min_conf):

    L, k, all_supports = {}, 1, {}
    L[k], transactions, all_supports = get_L1(filename, min_sup, all_supports)
    while True:

        k += 1
        Ck = apriori_generation(L[k-1], k)
        Ck_supports = compute_supports(transactions, Ck, all_supports)

        L[k] = set()
        for item in Ck_supports.items():
            key, value = item
            item_support = float(value / len(transactions))
            if  item_support >= min_sup:
                L[k].add(key)
        if len(L[k]) == 0:
            break
        print("k:{}\t Lk length:{}".format(k, len(L[k])))

    return L, all_supports, transactions

def extract_association_rules(L, supports, min_conf, transactions):

    extracted_rules = []
    for item in L.items():
        k, L_k = item
        for Lk_item in L_k:
            all_subsets, subsets = [], []
            for length in range(1, len(Lk_item)):
                subsets = combinations(Lk_item, length)
            all_subsets += subsets

            for subset in all_subsets:
                conf = float(supports[Lk_item] / supports[frozenset(subset)])
                if conf >= min_conf:
                    extracted_rules.append({
                        "lhs": set(subset), 
                        "rhs": set(Lk_item.difference(subset)),
                        "conf": conf,
                        "support": float(supports[frozenset(subset)]/len(transactions))}
                    )

    extracted_rules_sorted = sorted(extracted_rules, key=lambda x:x["conf"], reverse=True)
    return extracted_rules_sorted

def process_input():
    sys.argv.pop(0)
    filename, min_sup, min_conf = sys.argv[0], float(sys.argv[1]), float(sys.argv[2])
    return filename, min_sup, min_conf

def main():

    filename, min_sup, min_conf = process_input()
    L, supports, transactions = apriori(filename, min_sup, min_conf)
    rules = extract_association_rules(L, supports, min_conf, transactions)

    sorted_supports = sorted(supports.items(), key=lambda x: x[1], reverse=True)

    output_filename = "output.txt"
    with open(output_filename, "w") as output_file:
        output_file.write("==Frequent itemsets (min_sup={}%)\n".format(min_sup*100))
        for support_pair in sorted_supports:
            item, support_value = support_pair
            item = ["".join(list(sub_item)) for sub_item in item]
            output_file.write("[{}], {}%\n".format(item, support_value/len(transactions)*100)) 
        output_file.write("==High-confidence association rules (min_conf={}%)\n".format(min_conf*100))  
        for rule in rules:
            lhs, rhs, conf, support = rule["lhs"], rule["rhs"], rule["conf"], rule["support"]
            lhs, rhs = ["".join(list(item)) for item in lhs], ["".join(list(item)) for item in rhs]
            output_file.write("[{}]=>[{}] (Conf: {}%, Supp: {}%)\n".format(lhs, rhs, conf*100, support*100))

if __name__ == "__main__":
    main()
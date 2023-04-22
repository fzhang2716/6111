import csv

def get_itemset(filename):

	itemset, transactions = set(), []
	
	with open(filename, mode='r', encoding='utf-8-sig') as f:
		data = csv.reader(f)
		for line in data:
            transactions.append(set(line))
			for item in line:
				itemset.add(set(item))

	return itemset, transactions

def apriori_generation(Lk):

    Ck = set()
    # join
    for p in Lk:
        for q in Lk:
            if len(p.difference(q)) == 1:
                joint_item = p.union(q)
                Ck.add(joint_item)
    
    # prune
    for c in Ck:
        if any(item not in Lk for item in [c.difference(set[item_c]) for item_c in c]):
            Ck.remove(c)

    return Ck

def compute_supports(Ck, transactions):

    Ck_supports = {}

    for trans in transactions:
        Ct = trans.difference(Ck)
        for c in Ct:
            if c not in Ck_supports:
                Ck_supports[c] = 0
            Ck_supports[c] += 1

    return Ck_supports

def apriori(filename, min_sup, min_conf):

    L, k, all_L, all_supports = {}, 1, set(), {}
    L[k], transactions = get_itemset(filename)

    while True:

        k += 1
        Ck = apriori_generation(L[k-1])
        Ck_supports = compute_supports(transactions, Ck)

        L[k] = [c for c in list(Ck_supports.keys()) if Ck_supports[c] >= min_sup]
        L[k] = set(L[k])
    
        all_supports.update(Ck_supports)
        if len(L[k]) == 0:
            break
    
    for item in L.items():
        k, Lk = item
        all_L.union(Lk)

    return all_L, all_supports

def extract_association_rules(L, supports, min_conf):

    extracted_rules = []
    for item in L:
        all_subsets_per_item = [(item.difference([elem]), set([elem])) for elem in item]
        for pair in all_subsets_per_item:
            lhs, rhs = pair
            conf = float(supports[item] / supports[lhs])
            if conf >= min_conf:
                extracted_rules.append({
                    "lhs": lhs, 
                    "rhs": rhs,
                    "conf": conf,
                    "support": supports[item]}
                )

    return extracted_rules

def process_input():
    sys.argv.pop(0)
    filename, min_sup, min_conf = sys.argv[0], int(sys.argv[1]), int(sys.argv[2])
   
    return filename, min_sup, min_conf

def main():

    filename, min_sup, min_conf = process_input()
    L, supports = apriori(filename, min_sup)
    rules = extract_association_rules(L, supports, min_conf)

    output_filename = "output.txt"
    with (output_filename, "w") as output_file:
        output_file.write("==Frequent itemsets (min_sup={}%)\n".format(min_sup*100))
        for item in L:
            output_file.write("[{}], {}%\n".format(item, supports[item]*100)) 
        output_file.write("==High-confidence association rules (min_conf={}%)\n".format(min_conf*100))  
        for rule in rules:
            lhs, rhs, conf, support = rule["lhs"], rule["rhs"], rule["conf"], rule["support"]
            output_file.write("[{}]=>[{}] (Conf: {}%, Supp: {}%)\n".format(lhs, rhs, conf*100, support*100))

if __name__ == "__main__":
    main()
import itertools
import csv
#from memory_profiler import profile
from memory_profiler import memory_usage

class FPNode(object):

    def __init__(self, value, count, parent):

        self.value = value
        self.count = count
        self.parent = parent
        self.link = None
        self.children = []

    def has_child(self, value):

        for node in self.children:
            if node.value == value:
                return True

        return False

    def get_child(self, value):

        for node in self.children:
            if node.value == value:
                return node

        return None

    def add_child(self, value):

        child = FPNode(value, 1, self)
        self.children.append(child)
        return child


class FPTree(object):
    """
    A frequent pattern tree.
    """

    def __init__(self, transactions, threshold, root_value, root_count):

        self.frequent = self.find_frequent_items(transactions, threshold)
        self.headers = self.build_header_table(self.frequent)
        self.root = self.build_fptree(
            transactions, root_value,
            root_count, self.frequent, self.headers)

    @staticmethod
    def find_frequent_items(transactions, threshold):

        items = {}

        for transaction in transactions:
            for item in transaction:
                if item in items:
                    items[item] += 1
                else:
                    items[item] = 1

        for key in list(items.keys()):
            if items[key] < threshold:
                del items[key]

        return items

    @staticmethod
    def build_header_table(frequent):

        headers = {}
        for key in frequent.keys():
            headers[key] = None

        return headers

    def build_fptree(self, transactions, root_value,
                     root_count, frequent, headers):

        root = FPNode(root_value, root_count, None)

        for transaction in transactions:
            sorted_items = [x for x in transaction if x in frequent]
            sorted_items.sort(key=lambda x: frequent[x], reverse=True)
            if len(sorted_items) > 0:
                self.insert_tree(sorted_items, root, headers)

        return root

    def insert_tree(self, items, node, headers):

        first = items[0]
        child = node.get_child(first)
        if child is not None:
            child.count += 1
        else:
            # Add new child.
            child = node.add_child(first)

            # Link it to header structure.
            if headers[first] is None:
                headers[first] = child
            else:
                current = headers[first]
                while current.link is not None:
                    current = current.link
                current.link = child

        # Call function recursively.
        remaining_items = items[1:]
        if len(remaining_items) > 0:
            self.insert_tree(remaining_items, child, headers)

    def tree_has_single_path(self, node):

        num_children = len(node.children)
        if num_children > 1:
            return False
        elif num_children == 0:
            return True
        else:
            return True and self.tree_has_single_path(node.children[0])

    def mine_patterns(self, threshold):

        if self.tree_has_single_path(self.root):
            return self.generate_pattern_list()
        else:
            return self.zip_patterns(self.mine_sub_trees(threshold))

    def zip_patterns(self, patterns):

        suffix = self.root.value

        if suffix is not None:
            # We are in a conditional tree.
            new_patterns = {}
            for key in patterns.keys():
                new_patterns[tuple(sorted(list(key) + [suffix]))] = patterns[key]

            return new_patterns

        return patterns

    def generate_pattern_list(self):

        patterns = {}
        items = self.frequent.keys()

        # If we are in a conditional tree,
        # the suffix is a pattern on its own.
        if self.root.value is None:
            suffix_value = []
        else:
            suffix_value = [self.root.value]
            patterns[tuple(suffix_value)] = self.root.count

        for i in range(1, len(items) + 1):
            for subset in itertools.combinations(items, i):
                pattern = tuple(sorted(list(subset) + suffix_value))
                patterns[pattern] = \
                    min([self.frequent[x] for x in subset])

        return patterns

    def mine_sub_trees(self, threshold):

        patterns = {}
        mining_order = sorted(self.frequent.keys(),
                              key=lambda x: self.frequent[x])

        # Get items in tree in reverse order of occurrences.
        for item in mining_order:
            suffixes = []
            conditional_tree_input = []
            node = self.headers[item]

            # Follow node links to get a list of
            # all occurrences of a certain item.
            while node is not None:
                suffixes.append(node)
                node = node.link

            # For each occurrence of the item, 
            # trace the path back to the root node.
            for suffix in suffixes:
                frequency = suffix.count
                path = []
                parent = suffix.parent

                while parent.parent is not None:
                    path.append(parent.value)
                    parent = parent.parent

                for i in range(frequency):
                    conditional_tree_input.append(path)

            # Now we have the input for a subtree,
            # so construct it and grab the patterns.
            subtree = FPTree(conditional_tree_input, threshold,
                             item, self.frequent[item])
            subtree_patterns = subtree.mine_patterns(threshold)

            # Insert subtree patterns into main patterns dictionary.
            for pattern in subtree_patterns.keys():
                if pattern in patterns:
                    patterns[pattern] += subtree_patterns[pattern]
                else:
                    patterns[pattern] = subtree_patterns[pattern]

        return patterns


def find_frequent_patterns(transactions, support_threshold):
   # Find the frequent paterns
    tree = FPTree(transactions, support_threshold, None, None)
    return tree.mine_patterns(support_threshold)


def generate_association_rules(patterns, confidence_threshold):
   # Assocation Rules with the given threshhold/confidence

    rules = {}
    for itemset in patterns.keys():
        upper_support = patterns[itemset]

        for i in range(1, len(itemset)):
            for antecedent in itertools.combinations(itemset, i):
                antecedent = tuple(sorted(antecedent))
                consequent = tuple(sorted(set(itemset) - set(antecedent)))

                if antecedent in patterns:
                    lower_support = patterns[antecedent]
                    confidence = float(upper_support) / lower_support

                    if confidence >= confidence_threshold:
                        rules[antecedent] = (consequent, confidence)

    return rules

#OPENING THE DATA
def open_data(filename):
    f = open(filename, 'rU')
    for l in f:
        l = l.strip().rstrip(',')
        row = frozenset(l.split(','))
        yield row


def mine(file):
    minsup = 9
    mincon = 0.9
    transactions = []

    with open(file, 'r') as database:
        for row in csv.reader(database):
            # row = row.strip().rstrip(',')
            # result = frozenset(row.split(','))
            # if options.numeric:
            #     transaction = []
            #     for item in row:
            #         transaction.append(item)
            #     transactions.append(transaction)
            # else:
            transactions.append(row)

    '''' FP-GROWTH ALGORITHM AND PRINT'''
    pattern = find_frequent_patterns(transactions,minsup)

    rules = generate_association_rules(pattern, mincon)

    #print('--Frequent Itemset--')
    #for item, support in sorted(pattern.items(), key=lambda item_support: item_support[0]):
        #print('ITEMS: {} : '.format(tuple(item)), end='')
        #print('{}'.format(support))
    newrules = []
    nrules = []
    confi = []
    #print('')
    #print('--Rules--')
    for rule, confidence in sorted(rules.items(), key=lambda rule_confidence: rule_confidence[0]):
            #print('RULES: {}: {}'.format(tuple(rule), confidence))
            newrules.append('RULES: {}: {}'.format(tuple(rule), confidence))
            nrules.append(tuple(rule))
            confi.append(confidence)
    return nrules,confi
'''
    p = OptionParser(usage='%prog data_file')
    p.add_option('-s', '--minimum-support', dest='minsup', type='int',
                 help='Minimum itemset support (default: 2)')
    p.add_option('-n', '--numeric', dest='numeric', action='store_true',
                 help='Convert the values in datasets to numerals (default: false)')
    p.add_option('-c', '--minimum-confidence', dest='mincon', type='float',
                 help='Minimum Confidence (default: 0.7)')
    p.set_defaults(minsup=2)
    p.set_defaults(numeric=False)



    options, args = p.parse_args()
    if len(args) < 1:
        p.error('must provide the path to a CSV file to read')
'''
'''
if __name__ == '__main__':

    main()
'''
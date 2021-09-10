#!/usr/local/bin/python3
import re
import sys
import math
import pandas as pd
from itertools import product
import numpy as np

# define constants
DEBUG = False

operators = {
    '!': lambda p: not p,
    '<=>': lambda p,q: not (p ^ q),
    '->': lambda p,q: (not p) and q,
    '|': lambda p,q: p or q,
    '&': lambda p,q: p and q,
    '^': lambda p,q: p ^ q
}

def parse_logic(statement, atomic_values):
    s = statement.replace(' ','')

    # stack overflow
    _tokenizer = re.compile(r'\s*([()])\s*').split
    def tokenize(s):
        return filter(None, _tokenizer(s))

    def parse_conditions(expr):
        def _helper(tokens):
            items = []
            for item in tokens:
                if item == '(':
                    result, closeparen = _helper(tokens)
                    if not closeparen:
                        raise ValueError("Unbalanced parentheses")
                    items.append(result)
                elif item == ')':
                    return items, True
                else:
                    items.append(item)
            return items, False
        return _helper(tokenize(expr))[0] 

    def eval_exprs(items):
        for i in range(len(items)):
            if isinstance(items[i], list):
                eval_exprs(items[i])
            else:
                if re.search(r'.*[A-Z].*', items[i]):
                    # case for !
                    if len(items[i]) == 2:
                        items[i] = str(operators[items[i][1]](atomic_values[items[i][1]]))
                    else:
                        print(items[i])
                        # print(items[i][1], atomic_values[items[i][0]], atomic_values[items[i][2]])
                        # items[i] = str(operators[items[i][1]](atomic_values[items[i][0]],atomic_values[items[i][2]]))
            # if re.search(r'[A-Z]', items[i]):
            #     print(re.findall(r'[A-Z]',items[i]))
        return items

    print(eval_exprs(parse_conditions(s)))

    # exprs = []
    # ops = []

    # if '(' in s:
    #     group_level = 0
    #     while i < len(s):
    #         if s[i] == '(':
    #             startP = i + s[i:].find('(')
    #             endP = i + s[i:].find(')')
    #             expr = s[startP+1:endP]
    #             exprs.append(re.sub(r'[()]','',expr))
    #             i = endP
    #             group_level = group_level + 1
    #         else:
    #             ops.append(s[i])
    #         i = i + 1
    # else:
    #     exprs = [s]
    
    # ops = list(filter(lambda x: x != ')', ops))

    # if DEBUG:
    #     print('Higher level ops: %s' % ops)

    # for exp in exprs:
    #     # convert to RPN type form
    #     op_list = []
    #     for opr in list(dict.keys(operators)):
    #         if opr in exp:
    #             op_list.append(opr)

    #     atom_list = list(re.sub(r'[^A-Z]', '', exp))

    #     if DEBUG:
    #         print('Subops: %s' % op_list)
    #         print('Atom sent: %s' % atom_list)

    #     op_stack = atom_list + op_list


def main(x):
    atomic_sentences = [x.upper().strip() for x in sys.argv[1].split(r',')]
    premises = [x.upper().strip() for x in sys.argv[2].split(r',')]
    conclusion = sys.argv[3].upper()

    # make a set of columns without redundancies
    set_cols = list(dict.fromkeys(atomic_sentences + premises + [conclusion]).keys())
    num_cases = 2**len(atomic_sentences)

    # get truth value possible combinations
    list_perm = [list(x) for x in list(product(['T','F'], repeat=int(math.sqrt(num_cases))))]
    # transpose matrix for input to dataframe
    truth_vals = np.array(list_perm).T

    print(truth_vals)

    # # generate the data dict
    # data = {}
    # # populate truth values for atomic sentences
    # for i in range(len(atomic_sentences)):
    #     data[set_cols[i]] = truth_vals[i]
    # for i in range(len(atomic_sentences),len(set_cols)-1):
    #     curr_prem = set_cols[i]
    #     # find the logical operator
    #     # operator, sring = parse_logic(curr_prem)
    #     # data[set_cols[i]] = t_val

if __name__ == '__main__':
    # parse_logic('((!A)->(B^C))^(A<=>C)', {'A':True, 'B':False, 'C':True})
    main()
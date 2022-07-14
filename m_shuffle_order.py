#! python

import argparse
import random
import json
import copy
import itertools

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-np', help='number of pattern for each data', type=int, default=4)
    parser.add_argument('-nv', help='number of random variation', type=int, default=10)
    parser.add_argument('-seed', help='random seed', type=int, default=1234)
    parser.add_argument('-i', help='input training data', default='out/e2e_test.json')
    parser.add_argument('-d_out', help='output directory', default='out_shuffle')
    args = parser.parse_args()

    print('** generate test data extension by shuffling order **')
    print(' input json file                 : '+str(args.i))
    print(' output directory                : '+str(args.d_out))
    print(' number of pattern for each data : '+str(args.np))
    print(' number of random variation      : '+str(args.nv))
    print(' random seed                     : '+str(args.seed))

    # generate all 'order' patterns
    a_order_pattern = {}
    for n in range(1, 9):
        a_order_pattern[n] = {'num': 0, 'order': []}
        a_num = []
        for i in range(n):
            a_num.append(i+1)

        a_pattern = itertools.permutations(a_num)
        for pattern in a_pattern:
            a_tmp = []
            for m in range(n):
                a_tmp.append(pattern[m])
            a_order_pattern[n]['order'].append(a_tmp)
        a_order_pattern[n]['num'] = len(a_order_pattern[n]['order'])

    # generate extend data (w/ random order)
    with open(args.i, 'r', encoding='utf-8') as f:
        a_data_org = json.load(f)

    a_n_attr = []
    a_pattern_idx = []
    for data in a_data_org:
        order = []
        n_attr = 0
        for attr in data['order']:
            if data['order'][attr] > 0:
                order.append(data['order'][attr])
                n_attr += 1
        a_n_attr.append(n_attr)

        idx = 0
        for n in range(a_order_pattern[n_attr]['num']):
            if order == a_order_pattern[n_attr]['order'][n]:
                idx = n
                break
        a_pattern_idx.append(idx)

    for n in range(args.nv):
        # set random seed
        random.seed(args.seed + n)
        a_data_new = []
        for i, data in enumerate(a_data_org):
            n_attr = a_n_attr[i]
            pattern_idx = a_pattern_idx[i]
            if a_order_pattern[n_attr]['num'] < args.np+1:
                a_idx = random.sample(range(a_order_pattern[n_attr]['num']), k=a_order_pattern[n_attr]['num'])
            else:
                a_idx = random.sample(range(a_order_pattern[n_attr]['num']), k=args.np+1)
            flag = False
            for j in range(len(a_idx)-1):
                if flag is False:
                    idx = a_idx[j]
                    if a_idx[j] == pattern_idx:
                        idx = a_idx[j+1]
                        flag = True
                else:
                    idx = a_idx[j+1]
                data_new = copy.deepcopy(data)
                k = 0
                for attr in data['order']:
                    if data['order'][attr] != 0:
                        data_new['order'][attr] = a_order_pattern[n_attr]['order'][idx][k]
                        k += 1
                data_new['id_ext'] = j+1
                a_data_new.append(data_new)

        with open(args.d_out.rstrip('\n')+'/e2e_test_ex_'+str(n)+'.json', 'w', encoding='utf-8') as f:
            json.dump(a_data_new, f, ensure_ascii=False, indent=4, sort_keys=False)

    print('** done **')

#! python

import argparse
import json

def make_value_list(value_list, a_obj, mix_flag):
    for obj in a_obj:
        for attr in value_list:
            if (obj['mr'][attr] != '') and ((obj['mr'][attr] in value_list[attr]) is False):
                value_list[attr].append(obj['mr'][attr])
    if mix_flag is True:
        value_list['name'] = list(set(value_list['name'] + value_list['near']))
        value_list['near'] = list(set(value_list['name'] + value_list['near']))
    for attr in value_list:
        value_list[attr] = sorted(value_list[attr])

    return value_list


## main function
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-itrain', help='input training data (json)')
    parser.add_argument('-ivalid', help='input validation data (json)')
    parser.add_argument('-itest',  help='input test data (json)')
    parser.add_argument('-o',  help='output value list (json)')
    parser.add_argument('-mix', help='mix name and near', action='store_true')
    args = parser.parse_args()

    print('** make_valuelist: E2E MR_value list **')
    print(' input (train) : '+str(args.itrain))
    print(' input (valid) : '+str(args.ivalid))
    print(' input (test)  : '+str(args.itest))
    print(' output        : '+str(args.o))
    print(' mix           : '+str(args.mix))

    value_list = {
        'name': [],
        'eatType': [],
        'food': [],
        'priceRange': [],
        'customer rating': [],
        'area': [],
        'familyFriendly': [],
        'near': []
    }

    with open(args.itrain, 'r', encoding='utf-8') as fi:
        a_obj_train = json.load(fi)
    with open(args.ivalid, 'r', encoding='utf-8') as fi:
        a_obj_valid = json.load(fi)
    with open(args.itest, 'r', encoding='utf-8') as fi:
        a_obj_test = json.load(fi)

    value_list = make_value_list(value_list, a_obj_train, args.mix)
    value_list = make_value_list(value_list, a_obj_valid, args.mix)
    value_list = make_value_list(value_list, a_obj_test, args.mix)

    with open(args.o, 'w', encoding='utf-8') as fo:
        json.dump(value_list, fo, ensure_ascii=False, indent=4, sort_keys=False)

    print('** done **')

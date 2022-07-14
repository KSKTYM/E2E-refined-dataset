#! python

import json
import copy
import argparse
import numpy

## (1) remove LF code
def remove_lf(a_lines_in):
    ## trainset.csv
    # L.15765-15766
    # L.32411-32412
    a_lines_out = []
    for line in a_lines_in:
        if '[' in line:
            a_lines_out.append(line.rstrip('\n'))
        else:
            a_lines_out[len(a_lines_out)-1] += line.rstrip('\n')
    return a_lines_out

## (2) convert csv to object
def conv_csv2obj(a_csv):
    obj_template = {
        'mr': {
            'name': '',
            'eatType': '',
            'food': '',
            'priceRange': '',
            'customer rating': '',
            'area': '',
            'familyFriendly': '',
            'near': ''
        },
        'txt': '',
        'id': 0
    }

    a_obj = []
    for i, csv in enumerate(a_csv):
        obj = copy.deepcopy(obj_template)
        obj['id'] = i

        if ('\",') in csv:
            mr = csv.split('\",')[0]
            obj['txt'] = csv.split('\",')[1]
        else:
            print('line '+str(i)+': '+csv)
            continue

        # obtain MR data
        for attr in obj['mr']:
            if (attr+'[') in mr:
                obj['mr'][attr] = mr[mr.find(attr+'[')+len(attr+'['):].split(']')[0]

        a_obj.append(obj)

    return a_obj

## main function
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='input data (csv)')
    parser.add_argument('-o', help='output data (json)')
    args = parser.parse_args()

    print('** convert csv to object(json) **')
    print(' input  (csv)  : '+str(args.i))
    print(' output (json) : '+str(args.o))

    # (0) obtain original lines
    with open(args.i, 'r', encoding='utf-8') as fi:
        a_csv = fi.readlines()

    # (1) remove the 1st line
    a_csv = a_csv[1:]

    # (2) remove LF code
    a_csv = remove_lf(a_csv)

    # (3) convert csv to object
    a_obj = conv_csv2obj(a_csv)

    # (4) dump file
    with open(args.o, 'w', encoding='utf-8') as fo:
        json.dump(a_obj, fo, ensure_ascii=False, indent=4, sort_keys=False)

    print('** done **')

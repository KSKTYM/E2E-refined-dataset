#! python

import argparse
import json

## main function
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='input json file')
    parser.add_argument('-o', help='output csv file')
    parser.add_argument('-nr', help='no reference', action='store_true')
    args = parser.parse_args()

    print('** conv_tsv2csv: convert tsv to csv **')
    print(' input  : '+str(args.i))
    print(' output : '+str(args.o))

    with open(args.i, 'r', encoding='utf-8')as fi:
        a_obj_in = json.load(fi)

    fo = open(args.o, 'w', encoding='utf-8')
    fo.write('mr')
    if args.nr is False:
        fo.write(',ref')
    fo.write('\n')
    for obj in a_obj_in:
        fo.write('\"')
        flag = False
        if obj['mr']['name'] != '':
            fo.write('name['+obj['mr']['name']+']')
            flag = True
        if obj['mr']['eatType'] != '':
            if flag is True:
                fo.write(', ')
            fo.write('eatType['+obj['mr']['eatType']+']')
        if obj['mr']['food'] != '':
            if flag is True:
                fo.write(', ')
            fo.write('food['+obj['mr']['food']+']')
        if obj['mr']['priceRange'] != '':
            if flag is True:
                fo.write(', ')
            fo.write('priceRange['+obj['mr']['priceRange']+']')
        if obj['mr']['customer rating'] != '':
            if flag is True:
                fo.write(', ')
            fo.write('customer rating['+obj['mr']['customer rating']+']')
        if obj['mr']['area'] != '':
            if flag is True:
                fo.write(', ')
            fo.write('area['+obj['mr']['area']+']')
        if obj['mr']['familyFriendly'] != '':
            if flag is True:
                fo.write(', ')
            fo.write('familyFriendly['+obj['mr']['familyFriendly']+']')
        if obj['mr']['near'] != '':
            if flag is True:
                fo.write(', ')
            fo.write('near['+obj['mr']['near']+']')
        fo.write('\"')
        if args.nr is False:
            fo.write(',\"')
            fo.write(obj['txt'])
            fo.write('\"')
        fo.write('\n')
    fo.close()
    print('** done **')

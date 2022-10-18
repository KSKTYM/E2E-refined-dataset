#! python

import argparse
import json

def print_msg(msg, verbose_flag):
    if verbose_flag is True:
        print(msg)

# main
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-org', help='org json file')
    parser.add_argument('-new', help='new json file')
    parser.add_argument('-o', help='output txt file')
    parser.add_argument('-v', help='verbose flag', action='store_true')
    args = parser.parse_args()

    print('** error analysis **')
    print(' org data: '+str(args.org))
    print(' new data: '+str(args.org))
    print(' output  : '+str(args.o))
    print(' verbose : '+str(args.v))

    with open(args.org, 'r', encoding='utf-8') as f:
        a_org = json.load(f)
    with open(args.new, 'r', encoding='utf-8') as f:
        a_new = json.load(f)

    num_weird = 0
    num_duplicate = 0
    num_mr_ins = 0
    num_mr_del = 0
    num_mr_sub = 0
    for obj_org in a_org:
        obj_id = obj_org['id']

        obj = None
        for obj_new in a_new:
            if obj_new['id'] == obj_id:
                obj = obj_new
                break
        if obj is None:
            if obj_org['remarks'].startswith('duplicate'):
                num_duplicate += 1
            elif obj_org['remarks'].startswith('weird'):
                num_weird += 1
            print_msg('[id:'+str(obj_id)+'] '+obj_org['remarks'], args.v)
            print_msg('txt: '+str(obj_org['txt']), args.v)
        else:
            error_flag = False
            error_ins = False
            error_del = False
            error_sub = False
            for attr in obj_org['mr']:
                if (obj_org['org']['mr'][attr].lower() == '') and (obj['mr']['value'][attr].lower() != ''):
                    error_flag = True
                    error_ins = True
                elif (obj_org['org']['mr'][attr].lower() != '') and (obj['mr']['value'][attr].lower() == ''):
                    error_flag = True
                    error_del = True
                elif (obj_org['org']['mr'][attr].lower() != obj['mr']['value'][attr].lower()):
                    if (attr != 'priceRange') or (obj_org['mr'][attr] != 'high') or (obj['mr']['value'][attr] != 'expensive'):
                        error_flag = True
                        error_sub = True

            if error_flag is True:
                error_msg = ''
                if error_ins is True:
                    error_msg += '(INS)'
                    num_mr_ins += 1
                if error_del is True:
                    error_msg += '(DEL)'
                    num_mr_del += 1
                if error_sub is True:
                    error_msg += '(SUB)'
                    num_mr_sub += 1
                if (error_ins is True) and (error_del is True) and (error_sub is True):
                    error_msg = 'ALL'
                print_msg('[id:'+str(obj_id)+'] MR error '+error_msg, args.v)
                print_msg('org: '+str(obj_org['org']['mr']), args.v)
                print_msg('new: '+str(obj['mr']['value']), args.v)
                if (error_ins is True) and (error_del is True) and (error_sub is True):
                    print_msg('txt: '+str(obj_org['txt']), args.v)

        if obj_org['org']['mr']['name'] == '':
            print_msg('id: '+str(obj_org['id'])+' name is empty', args.v)

    with open(args.o, 'w', encoding='utf-8') as f:
        f.write('num of data\t'+str(len(a_org))+'\n')
        f.write('num of errors'+'\n')
        f.write('[text]'+'\n')
        f.write(' weird\t'+str(num_weird)+'\n')
        f.write(' duplicate\t'+str(num_duplicate)+'\n')
        f.write('[mr]'+'\n')
        f.write(' insertion\t'+str(num_mr_ins)+'\n')
        f.write(' deletion\t'+str(num_mr_del)+'\n')
        f.write(' substitution\t'+str(num_mr_sub)+'\n')
    print('** done **')

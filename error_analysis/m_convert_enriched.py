#! python

import copy
import xmltodict
import json
import argparse

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
    'mr_lex': {
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
    'txt_lex': '',
    'order': {
        'name': 0,
        'eatType': 0,
        'food': 0,
        'priceRange': 0,
        'customer rating': 0,
        'area': 0,
        'familyFriendly': 0,
        'near': 0
    },
    'num_sen': 0,
    'id': ''
}

def convert(f_input, all_flag=False):
    with open(f_input, 'r', encoding='utf-8') as f:
        a_input = f.readlines()
    script = ''
    for line in a_input:
        script += line.rstrip('\n')
    script = script.replace('</sentence>        <sentence>', '')
    obj_org = xmltodict.parse(script, force_list=('entry', 'target', 'sentence', 'input'))

    a_obj_new = []
    for entry in obj_org['entries']['entry']:
        for target in entry['target']:
            if target['text'] is None:
                continue

            obj = copy.deepcopy(obj_template)
            obj['id'] = entry['@eid']+'-'+target['@lid']
            obj['txt'] = target['text']
            obj['txt_lex'] = target['text']

            output_flag = True
            a_loc = {}
            for sentence in target['structuring']['sentence']:
                if sentence is None:
                    continue

                if (all_flag is False) and \
                   (len(sentence['input']) != int(entry['@size'])):
                    output_flag = False
                    break

                for attribute in sentence['input']:
                    obj['mr'][attribute['@attribute']] = attribute['@value']
                    obj['mr_lex'][attribute['@attribute']] = attribute['@value']
                    a_loc[attribute['@attribute']] = target['template'].find(attribute['@tag'])
                if obj['mr']['name'] != '':
                    obj['mr_lex']['name'] = 'NAME'
                    obj['txt_lex'] = obj['txt_lex'].replace(obj['mr']['name'], obj['mr_lex']['name'])
                if obj['mr']['near'] != '':
                    obj['mr_lex']['near'] = 'NEAR'
                    obj['txt_lex'] = obj['txt_lex'].replace(obj['mr']['near'], obj['mr_lex']['near'])

            if output_flag is False:
                continue

            a_loc_tmp = sorted(a_loc.items(), key=lambda x:x[1])
            n = 1
            for i in range(len(a_loc_tmp)):
                if obj['mr'][a_loc_tmp[i][0]] != '':
                    obj['order'][a_loc_tmp[i][0]] = n
                    n += 1
            obj['num_sen'] = obj['txt'].count('.') + obj['txt'].count('?')
            a_obj_new.append(obj)
    return a_obj_new

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d_i', help='input directory')
    parser.add_argument('-o', help='output json file')
    parser.add_argument('-all', help='all data', action='store_true')
    args = parser.parse_args()

    print('** convert xml file (enriched E2E dataset) to json file **')
    print(' input directory  : '+str(args.d_i))
    print(' output json file : '+str(args.o))
    print(' all data flag    : '+str(args.all))

    a_obj_new = []
    a_obj_new += convert(args.d_i.rstrip('/')+'/3attributes.xml', args.all)
    a_obj_new += convert(args.d_i.rstrip('/')+'/4attributes.xml', args.all)
    a_obj_new += convert(args.d_i.rstrip('/')+'/5attributes.xml', args.all)
    a_obj_new += convert(args.d_i.rstrip('/')+'/6attributes.xml', args.all)
    a_obj_new += convert(args.d_i.rstrip('/')+'/7attributes.xml', args.all)
    a_obj_new += convert(args.d_i.rstrip('/')+'/8attributes.xml', args.all)

    with open(args.o, 'w', encoding='utf-8') as f:
        json.dump(a_obj_new, f, ensure_ascii=False, indent=4, sort_keys=False)

    print('** done **')

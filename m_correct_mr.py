#! python

import argparse
import json
import copy
import numpy as np

# (1)(2) name and near (subs)
def extract_near_A(obj_new, a_word_cand, a_article):
    a_near = [
        'across from',
        'across the street from',
        'adjacent to',
        'along from',
        'along the river from',
        'along the riverbank from',
        'area of',
        'around',
        'around the corner from',
        'around where',
        'beside',
        'beside the river and',
        'by the mid-range chinese restaurant',
        'by the not family friend',
        'by the riverside and',
        'close',
        'close by',
        'close by to',
        'close competitor,',
        'close proximity to fast food outlet',
        'close to',
        'close to a competitor',
        'close to the city centre, the river and also',
        'close to the city\'s center as well as',
        'close to the city\'s centre as well as',
        'close to the coffee shop called',
        'close to the english pub that is called',
        'close to the fast food',
        'close to the river and',
        'close to the riverside and',
        'close-by landmark is',
        'close-by to',
        'closed to',
        'closer to',
        'convenient to',
        'east of',
        'easy to find from',
        'family friendly in',
        'few steps of',
        'find it by',
        'hither to',
        'in front of',
        'in riverside by',
        'in the area include',
        'in the centre of',
        'in the city centre of',
        'in the city core',
        'in the side',
        'in the vicinity of',
        'is minutes from',
        'it is above',
        'it is by',
        'it is in the city centre of',
        'it is located',
        'it\'s by',
        'it\'s right by',
        'located a short distance away from',
        'located across the street from the famous restaurant',
        'located at',
        'located by',
        'located by the river and',
        'located by the riverside',
        'located by the riverside at',
        'located in',
        'located in city centre that is family friendly and offers',
        'located in city centre that offers',
        'located in the city centre by',
        'located in the city centre that is family friendly and offers',
        'located in the city centre that offers',
        'located in the city centre there',
        'located in the city centre, there',
        'located in the riverside by',
        'located just up the street from',
        'located near the low rated, children friendly coffee shop called',
        'located near the low rated, children friendly restaurant called,',
        'located near the moderate',
        'located near the river, there',
        'located next to door to',
        'located next to the riverside and',
        'located on',
        'located riverside by',
        'location by',
        'location city centre area has a coffee shop named',
        'location city centre, and',
        'near',
        'near a children friendly french coffee shop in riverside called',
        'near a city centre and',
        'near a city centre and the local',
        'near a coffee shop called',
        'near a river and',
        'near a river and the local',
        'near a riverside and',
        'near a riverside and the local',
        'near a sushi restaurant called',
        'near a town centre and',
        'near a town centre and the local',
        'near city centre',
        'near city centre and',
        'near french food',
        'near from',
        'near from the famous',
        'near in',
        'near it called',
        'near japanese',
        'near of',
        'near river',
        'near river and',
        'near riverside',
        'near riverside and',
        'near riverside in',
        'near the centre of the city and',
        'near the centre of the city and the fast food',
        'near the city centre',
        'near the city centre and',
        'near the city centre\'s',
        'near the city centre,',
        'near the coffee shop',
        'near the coffee shop called',
        'near the coffee shop,',
        'near the famous',
        'near the fast food',
        'near the fast food restaurant',
        'near the fast food restaurant,',
        'near the indian restaurant,',
        'near the infamous',
        'near the popular',
        'near the pub',
        'near the restaurant',
        'near the river',
        'near the river and',
        'near the river, and',
        'near the river, there',
        'near the rivers side and',
        'near the riverside',
        'near the riverside and',
        'near the riverside area and',
        'near the riverside area in',
        'near the town centre',
        'near the town centre and',
        'near to',
        'near to city centre and',
        'near to coffee shop',
        'near to river and',
        'near to riverside and',
        'near to the city centre and',
        'near to the coffee shop',
        'near to the coffee shop called',
        'near to the japanese restaurant,',
        'near to the river and',
        'near to the riverside and',
        'near to the town centre and',
        'near to town centre and',
        'near town centre',
        'near town centre and',
        'near,',
        'near:',
        'nearby',
        'nearby called',
        'nearby eatery is',
        'nearby the city centre and',
        'nearby the city centre and the restaurant',
        'nearby there is',
        'nearby to',
        'nearby with an average customer rating called',
        'nearby with cheap prices and an average customer rating, which is called',
        'neighbor to a new, kid-friendly fast-food joint called',
        'neighbour to a new, kid-friendly fast-food joint called',
        'neighboring',
        'neighbouring',
        'neighbour',
        'next door is a high priced italian eater named',
        'next to',
        'next to the river and',
        'north of',
        'not far away is',
        'not far from',
        'not too far from',
        'off the river in',
        'on side',
        'on the river at',
        'on the riverside at',
        'on the riverside where',
        'on the side',
        'one block from',
        'opposite',
        'opposite to',
        'past',
        'place by',
        'proximity of',
        'proximity to',
        'rating by',
        'right be',
        'shop in',
        'short distance along the riverside from',
        'short distance from',
        'short distance from the city centre and',
        'short walk from',
        'sits near an averagely rated indian pub known as',
        'situated by',
        'situated in',
        'south of',
        'staying at',
        'the road from',
        'this place is known as',
        'vicinity of',
        'visiting',
        'west of',
        'within a short walk of',
        'within walking distance of',
        'you can see'
    ]

    remove_val = ''
    for keyword in a_near:
        for article in a_article:
            for name in a_word_cand:
                flag = False
                if keyword + article + name in obj_new['txt']:
                    obj_new['mr']['near'] = name
                    remove_val = name
                    flag = True
                if '%%%' in obj_new['txt']:
                    if keyword + article + '%%%' + name in obj_new['txt']:
                        obj_new['mr']['near'] = name
                        remove_val = name
                        flag = True
                if flag is True:
                    if keyword == 'near,':
                        obj_new['txt'] = obj_new['txt'].replace('near,', 'near')
                    elif keyword == 'located in':
                        obj_new['txt'] = obj_new['txt'].replace('located in', 'located at')
                    elif keyword == 'located':
                        obj_new['txt'] = obj_new['txt'].replace('located', 'located at')

    a_near_back = [
        'are near it',
        'close by',
        'close to it as well',
        'is connected to the restaurant',
        'is just near by',
        'is just on the road',
        'is located nearby',
        'is near by',
        'is nearby',
        'located nearby',
        'near by',
        'near the city centre area has a coffee shop named',
        'nearby',
        'neighborhood',
        'next door',
        'which also sits on the river',
        'which sits nearby'
    ]

    if remove_val == '':
        for name in a_word_cand:
            for near_back in a_near_back:
                if name + ' ' + near_back in obj_new['txt']:
                    obj_new['mr']['near'] = name
                    remove_val = name

    if remove_val != '':
        a_word_cand.remove(remove_val)

    if obj_new['mr']['near'] == '':
        for name in a_word_cand:
            for article in a_article:
                if (obj_new['txt'].startswith('by' + article + name)) or \
                   (obj_new['txt'].startswith('over by' + article + name)):
                    obj_new['mr']['near'] = name
                    a_word_cand.remove(name)
                    break
                elif obj_new['txt'].endswith('by' + article + name + '.'):
                    obj_new['mr']['near'] = name
                    a_word_cand.remove(name)
                    break

    if obj_new['mr']['near'] == '':
        for name in a_word_cand:
            if name + '. opposite that' in obj_new['txt']:
                obj_new['mr']['near'] = name
                a_word_cand.remove(name)
                break

    return obj_new, a_word_cand

def extract_near_B(obj_new, a_word_cand, a_article):
    a_near_B = [
        'in',
        'by',
    ]
    remove_val = ''
    for keyword in a_near_B:
        for near in a_word_cand:
            for article in a_article:
                if keyword + article + near in obj_new['txt']:
                    obj_new['mr']['near'] = near
                    remove_val = near

    if remove_val != '':
        a_word_cand.remove(remove_val)

    return obj_new, a_word_cand

# (2) name
def extract_name_A(obj_new, a_word_cand):
    remove_val = ''
    for article in ['', 'a ', 'an ', 'the ']:
        for name in a_word_cand:
            if obj_new['txt'].startswith(article+name):
                obj_new['mr']['name'] = name
                remove_val = name
    if remove_val != '':
        a_word_cand.remove(remove_val)

    return obj_new, a_word_cand

# (1)(2) name and near (main)
def extract_name_near(obj_new, value_list, verbose_flag, mr_old):
    a_article = [' ', ' a ', ' an ', ' the ']

    # (0) return if invalid object
    if obj_new['remarks'] != '':
        return obj_new

    # (1-0) search word candidates
    a_word_cand = []
    for value in value_list['name']:
        count = obj_new['txt'].count(value)
        for i in range(count):
            a_word_cand.append(value)
    a_name_list = list(set(a_word_cand))

    # (1-1) near and name
    # remove invalid data: number of NAME candidates
    if (len(a_name_list) == 0) or (len(a_name_list) > 2):
        if len(a_name_list) == 0:
            obj_new['remarks'] = 'no NAME/NEAR candidates in txt'
        else:
            obj_new['remarks'] = 'too many number of NAME/NEAR candidate values in txt'
        if verbose_flag is True:
            print('[name/near:A]('+str(obj_new['id'])+') '+obj_new['remarks'])
        return obj_new

    elif len(a_name_list) == 1:
        # remove invalid data
        if len(a_word_cand) == 2:
            for articleA in a_article:
                for articleB in a_article:
                    if ((articleA + a_word_cand[0] + '' + articleB + a_word_cand[0]) in obj_new['txt']) or \
                       ((articleA + a_word_cand[0] + ' near' + articleB + a_word_cand[0]) in obj_new['txt']) or \
                       ((articleA + a_word_cand[0] + ' is' + articleB + a_word_cand[0]) in obj_new['txt']):
                        obj_new['remarks'] = 'weird NAME/NEARs are appeared in txt'
                        if verbose_flag is True:
                            print('[name/near:B]('+str(obj_new['id'])+') '+obj_new['remarks'])
                        return obj_new

        # near
        obj_new, a_word_cand = extract_near_A(obj_new, a_word_cand, a_article)
        if obj_new['mr']['near'] != '':
            if (obj_new['txt'].count(obj_new['mr']['near']) == 1) and \
               (('near ' + obj_new['mr']['near'] in obj_new['txt']) is False):
                if verbose_flag is True:
                    print('C0: '+str(obj_new['id']))
                obj_new['mr']['name'] = obj_new['mr']['near']
                obj_new['mr']['near'] = ''
            else:
                # remove invalid data
                if obj_new['txt'].count(obj_new['mr']['near']) == 1:
                    obj_new['remarks'] = 'no NAME candidates but one NEAR candidate value appeared in txt'
                else:
                    obj_new['remarks'] = 'NAME and NEAR have the same candidate value'
                if verbose_flag is True:
                    print('[name/near:C]('+str(obj_new['id'])+') '+obj_new['remarks'])
                return obj_new
        else:
            # name
            obj_new['mr']['name'] = a_name_list[0]
            a_word_cand.remove(obj_new['mr']['name'])

    else:
        # len(a_name_list) == 2

        # near and name
        remove_val_A = ''
        remove_val_B = ''
        for nameA in list(set(a_name_list)):
            for nameB in list(set(a_name_list)):
                for articleA in a_article:
                    for articleB in a_article:
                        for word in ['near', 'close to', 'by', 'next to', 'near to', 'around', 'north of', 'near the city centre and']:
                            if ((word + articleA + nameA + ' called' + articleB + nameB) in obj_new['txt']) or \
                               ((word + articleA + nameA + ' named' + articleB + nameB) in obj_new['txt']):
                                obj_new['mr']['near'] = nameA
                                obj_new['mr']['name'] = nameB
                                remove_val_A = nameA
                                remove_val_B = nameB
        if (remove_val_A != '') and (remove_val_B != ''):
            a_word_cand.remove(remove_val_A)
            a_word_cand.remove(remove_val_B)

        # remove invalid data E (OK)
        for nameA in list(set(a_word_cand)):
            for nameB in list(set(a_word_cand)):
                for articleA in a_article:
                    for articleB in a_article:
                        if (('by' + articleA + nameA + ' by' + articleB + nameB) in obj_new['txt']) or \
                           (('near' + articleA + nameA + ' near' + articleB + nameB) in obj_new['txt']):
                            obj_new['remarks'] = 'NEAR have two candidate values'
                            if verbose_flag is True:
                                print('[name/near:E1]('+str(obj_new['id'])+') '+obj_new['remarks'])
                            return obj_new

                        if ((articleA + nameA + ' called' + articleB + nameB) in obj_new['txt']) or \
                           ((articleA + nameA + ' named' + articleB + nameB) in obj_new['txt']):
                            obj_new['remarks'] = 'NAME or NEAR have two candidate values'
                            if verbose_flag is True:
                                print('[name/near:E2]('+str(obj_new['id'])+') '+obj_new['remarks'])
                            return obj_new

        # near
        if len(list(set(a_word_cand))) > 0:
            obj_new, a_word_cand = extract_near_A(obj_new, a_word_cand, a_article)

        # remove invalid data F (OK)
        if len(list(set(a_word_cand))) == 1:
            a_connect = ['']
        else:
            a_connect = ['', ' is']
        for nameA in a_word_cand:
            for nameB in a_word_cand:
                for articleA in ['', 'a ', 'an ', 'the ']:
                    for articleB in a_article:
                        for connect in a_connect:
                            if articleA + nameA + connect + articleB + nameB in obj_new['txt']:
                                if nameA != obj_new['mr']['near']:
                                    obj_new['remarks'] = 'weird NAME/NEARs are appeared in txt'
                                    if verbose_flag is True:
                                        print('[name/near:F]('+str(obj_new['id'])+') '+obj_new['remarks'])
                                    return obj_new

    # (1-2) name
    obj_new, a_word_cand = extract_name_A(obj_new, a_word_cand)

    # (1-3) near
    if (obj_new['mr']['name'] != '') and (obj_new['mr']['near'] == ''):
        obj_new, a_word_cand = extract_near_B(obj_new, a_word_cand, a_article)

    # (1-4) near and name
    remove_val_A = ''
    remove_val_B = ''
    for nameA in a_word_cand:
        for nameB in a_word_cand:
            if nameA == nameB:
                continue
            for article in a_article:
                if ((nameA + ' in' + article + nameB) in obj_new['txt']) or \
                   ((nameA + ' at' + article + nameB) in obj_new['txt']) or \
                   ((nameA + ' and' + article + nameB) in obj_new['txt']) or \
                   ((nameA + ' by' + article + nameB) in obj_new['txt']):
                    obj_new['mr']['name'] = nameA
                    obj_new['mr']['near'] = nameB
                    remove_val_A = nameA
                    remove_val_B = nameB
    if (remove_val_A != '') and (remove_val_B != ''):
        a_word_cand.remove(remove_val_A)
        a_word_cand.remove(remove_val_B)
 
    # (1-5) near
    if (obj_new['mr']['name'] != '') and (obj_new['mr']['near'] == ''):
        remove_val = ''
        for name in a_word_cand:
            for article in a_article:
                if ((obj_new['mr']['name'] + ' in' + article + name) in obj_new['txt']) or \
                   ((obj_new['mr']['name'] + ' at' + article + name) in obj_new['txt']) or \
                   ((obj_new['mr']['name'] + ' and' + article + name) in obj_new['txt']):
                    obj_new['mr']['near'] = name
                    remove_val = name
        if remove_val != '':
            a_word_cand.remove(remove_val)

    # (1-6) name
    if obj_new['mr']['name'] == '':
        flag_name = False
        remove_val = ''
        if len(a_word_cand) == 1:
            if ('near ' + a_word_cand[0] in obj_new['txt']) is False:
                obj_new['mr']['name'] = a_word_cand[0]
                remove_val = a_word_cand[0]
                flag_name = True
        if flag_name is False:
            if obj_new['mr']['near'] in a_word_cand:
                a_word_cand.remove(obj_new['mr']['near'])
            if len(list(set(a_word_cand))) == 1:
                obj_new['mr']['name'] = a_word_cand[0]
                remove_val = a_word_cand[0]
                flag_name = True
        if remove_val != '':
            a_word_cand.remove(remove_val)

    # (1-7) near and name
    if (obj_new['mr']['name'] == '') and (obj_new['mr']['near'] == ''):
        for near in a_word_cand:
            for article in a_article:
                if ('in' + article + near in obj_new['txt']) or \
                   ('by' + article + near in obj_new['txt']):
                    obj_new['mr']['near'] = near
                    a_word_cand.remove(near)

        if len(list(set(a_word_cand))) == 1:
            if (('near ' + a_word_cand[0]) in obj_new['txt']) is False:
                obj_new['mr']['name'] = a_word_cand[0]
                remove_val = a_word_cand[0]

        if len(list(set(a_word_cand))) == 2:
            for nameA in a_word_cand:
                for nameB in a_word_cand:
                    for food in [' coffee shop ', ' restaurant ']:
                        if 'stunning ' + nameA + food + nameB in obj_new['txt']:
                            obj_new['mr']['near'] = nameA
                            obj_new['mr']['name'] = nameB
                            a_word_cand.remove(nameA)
                            a_word_cand.remove(nameB)

            if 'in the same riverfront location' in obj_new['txt']:
                loc_A = obj_new['txt'].find(a_word_cand[0])
                loc_B = obj_new['txt'].find(a_word_cand[1])
                if loc_A < loc_B:
                    near = a_word_cand[0]
                    name = a_word_cand[1]
                else:
                    near = a_word_cand[1]
                    name = a_word_cand[0]
                obj_new['mr']['near'] = near
                obj_new['mr']['name'] = name
                a_word_cand.remove(near)
                a_word_cand.remove(name)

    # (1-8) near
    if (len(list(set(a_word_cand))) == 1) and \
       (obj_new['mr']['name'] != '') and (obj_new['mr']['near'] == ''):
        if a_word_cand[0] + ' area of' in obj_new['txt']:
            obj_new['mr']['near'] = a_word_cand[0]
            a_word_cand.remove(a_word_cand[0])

    # check (1)(2) status
    # remove invalid data G
    if (obj_new['mr']['name'] != '') and \
       (obj_new['mr']['name'] == obj_new['mr']['near']):
        obj_new['remarks'] = 'weird NAME/NEARs are appeared in txt'
        if verbose_flag is True:
            print('[name/near:G]('+str(obj_new['id'])+') '+obj_new['remarks'])
        return obj_new

    if len(list(set(a_word_cand))) >= 2:
        # remove invalid data H (OK)
        if (obj_new['mr']['name'] == '') or (obj_new['mr']['near'] == ''):
            obj_new['remarks'] = 'weird NAME/NEARs are appeared in txt'
            if verbose_flag is True:
                print('[name/near:H]('+str(obj_new['id'])+') '+obj_new['remarks'])
            return obj_new

    elif len(list(set(a_word_cand))) == 1:
        if ((obj_new['mr']['name'] == '') and (obj_new['mr']['near'] != '')) or \
           ((obj_new['mr']['name'] != '') and (obj_new['mr']['near'] == '')):
            if (obj_new['mr']['name'] == a_word_cand[0]) or \
               (obj_new['mr']['near'] == a_word_cand[0]):
                if ('called ' + a_word_cand[0] in obj_new['txt']) and \
                   ('named ' + a_word_cand[0] in obj_new['txt']):
                    # remove invalid data I
                    obj_new['remarks'] = 'weird NAME/NEARs are appeared in txt'
                    if verbose_flag is True:
                        print('[name/near:I]('+str(obj_new['id'])+') '+obj_new['remarks'])
                    return obj_new

            else:
                # remove invalid data J (OK)
                obj_new['remarks'] = 'weird NAME/NEARs are appeared in txt'
                if verbose_flag is True:
                    print('[name/near:J]('+str(obj_new['id'])+') '+obj_new['remarks'])
                return obj_new

    if verbose_flag is True:
        # check (1) near
        if (obj_new['mr']['near'] == '') and (mr_old['near'] != ''):
            print('[NULL:near] ('+mr_old['near']+')')
            print(a_word_cand)
            print(obj_new['txt'])

        # check (2) name
        if obj_new['mr']['name'] == '':
            print('[NULL:name] ('+mr_old['name']+')')
            print(a_word_cand)
            print(obj_new['txt'])

    obj_new['reason']['name'] = obj_new['mr']['name']
    obj_new['reason']['near'] = obj_new['mr']['near']

    return obj_new


# (3) eatType (coffee shop, pub, restaurant)
def extract_eatType(obj_new, verbose_flag, mr_old):
    # coffee shop
    if ('coffee' in obj_new['txt']) or ('cafe' in obj_new['txt']):
        obj_new['mr']['eatType'] = 'coffee shop'
        if ('coffee' in obj_new['txt']):
            obj_new['reason']['eatType'] = 'coffee'
        else:
            obj_new['reason']['eatType'] = 'cafe'

        if ('near the coffee' in obj_new['txt']):
            obj_new['mr']['eatType'] = ''
        if ('near the cafe' in obj_new['txt']) and \
           (('cafe' in obj_new['mr']['near']) is False):
            obj_new['mr']['eatType'] = ''
        if (('cafe' in obj_new['mr']['name']) or ('cafe' in obj_new['mr']['near'])) and \
           (('coffee' in obj_new['txt']) is False) and \
           (obj_new['txt'].count('cafe') == 1):
            obj_new['mr']['eatType'] = ''

    # pub
    if (' pub' in obj_new['txt']) or \
       ('-pub' in obj_new['txt']) or \
       (obj_new['txt'][0:len('pub')] == 'pub') or \
       ('public house' in obj_new['txt']):
        '''
        if ('public restroom' in obj_new['txt']) is False:
            obj_new['mr']['eatType'] = 'pub'
            obj_new['reason']['eatType'] = 'pub'
        else:
            if (' pub ' in obj_new['txt']):
                obj_new['mr']['eatType'] = 'pub'
                obj_new['reason']['eatType'] = 'pub'
        '''
        obj_new['mr']['eatType'] = 'pub'
        obj_new['reason']['eatType'] = 'pub'

    # restaurant
    if 'restaurant' in obj_new['txt']:
        obj_new['mr']['eatType'] = 'restaurant'
        obj_new['reason']['eatType'] = 'restaurant'

    if verbose_flag is True:
        if (obj_new['mr']['eatType'] == '') and (mr_old['eatType'] != ''):
            print('[NULL:eatType] ('+mr_old['eatType']+')')
            print(obj_new['txt'])

    if obj_new['mr']['eatType'] == '':
        obj_new['reason']['eatType'] = ''

    return obj_new

# (4) food (chinese, english, fast food, french, indian, italian, japanese)
def extract_food(obj_new, value_list, verbose_flag, mr_old):
    a_cand = []
    a_cand_txt = []

    txt = obj_new['txt'].replace('breakfast', '')
    txt = txt.replace('english sterling', '')
    txt = txt.replace('british sterling', '')

    a_list = copy.deepcopy(value_list['food'])
    a_list.append('american')
    a_list.append('british')
    a_list.append('canadian')
    a_list.append('thai')

    for val in a_list:
        if val in txt:
            if (val == 'british') and ('british pound' in txt):
                pass
            elif 'not '+val in txt:
                pass
            elif (val == 'french') and ('french fries' in txt):
                pass
            else:
                a_cand.append(val.replace('british', 'english'))
                a_cand_txt.append(val)

    # fast food
    a_fastfood = ['fast food', 'fast-food', 'fast service', 'food fast', 'offerint fast', 'offers fast', 'food is fast']
    for val in a_fastfood:
        if (val in txt) and (('fast food' in a_cand) is False):
            a_cand.append('fast food')
            a_cand_txt.append(val)

    if verbose_flag is True:
        if (len(a_cand) > 1) and (('indian' in a_cand) is False):
            print('FOOD candidate: '+str(a_cand))
            print(txt)

    if (obj_new['mr']['food'] == '') and (' uk' in txt):
        obj_new['mr']['food'] = 'english'
        obj_new['reason']['food'] = ' uk'

    if (obj_new['mr']['food'] == '') and (' usa.' in txt):
        obj_new['mr']['food'] = 'american'
        obj_new['reason']['food'] = ' usa.'

    if (obj_new['mr']['food'] == '') and ('united states' in txt):
        obj_new['mr']['food'] = 'american'
        obj_new['reason']['food'] = 'united states'

    if ('indian' in obj_new['mr']['name']) or \
       ('indian' in obj_new['mr']['near']):
        if len(a_cand) == 1:
            if obj_new['txt'].count('indian') > 1:
                obj_new['mr']['food'] = 'indian'
                obj_new['reason']['food'] = 'indian'
        else:
            for i in range(len(a_cand)):
                if a_cand[i] != 'indian':
                    obj_new['mr']['food'] = a_cand[i]
                    #obj_new['reason']['food'] = a_cand[i]
                    obj_new['reason']['food'] = a_cand_txt[i]
                    break
    else:
        for i in range(len(a_cand)):
            obj_new['mr']['food'] = a_cand[i]
            #obj_new['reason']['food'] = a_cand[i]
            obj_new['reason']['food'] = a_cand_txt[i]

    # taste of Italy
    if (obj_new['mr']['food'] == '') and \
       ('taste of italy' in obj_new['txt']):
        obj_new['mr']['food'] = 'italian'
        obj_new['reason']['food'] = 'taste of italy'

    # pasta is Italian food?
    if (obj_new['mr']['food'] == '') and \
       ('pasta' in obj_new['txt']):
        obj_new['mr']['food'] = 'italian'
        obj_new['reason']['food'] = 'pasta'

    # sushi is japanese, but japanese is sushi..?
    if (obj_new['mr']['food'] == '') and \
       ('sushi' in obj_new['txt']):
        obj_new['mr']['food'] = 'japanese'
        obj_new['reason']['food'] = 'sushi'

    # food from japan
    if (obj_new['mr']['food'] == '') and \
       ('food from japan.' in obj_new['txt']):
        obj_new['mr']['food'] = 'japanese'
        obj_new['reason']['food'] = 'food from japan.'

    if verbose_flag is True:
        if (obj_new['mr']['food'] == '') and (mr_old['food'] != ''):
            print('[NULL:food] ('+mr_old['food']+')')
            print(obj_new['txt'])

    return obj_new

# (5) priceRange
def extract_priceRange(obj_new, value_list, verbose_flag, mr_old):
    a_price_20_25 = [
        '$20.00',
        '$22',
        '$24',
        '$25.00',
        '$20 to $25',
        '$20-$25',
        '$20.00-$25.00',
        '$20-25',
        '$20 price',
        '$20-price',
        '$20 and $25',
        '20 to 25',
        '20$-25',
        '20-25',
        '20-25$',
        '20-25lb',
        '20 through 25',
        'above $20',
        'between 20 and 25',
        'between $20 and $25',
        'between twenty and twenty five',
        'between twenty and twenty-five',
        'from $20',
        'from 20',
        'more than 20',
        'more than $20',
        'over 20',
        'over $20',
        'priced at about $25',
        'twenty to twenty five',
        'twenty to twenty-five',
        'under $25'
    ]
    a_price_20_25_tmp = [
        '$20 range',
        '$20 price range',
        '$20 food',
        '$20 japanese food',
        '20 pound meal',
        '20 pounds or so',
        'about 20',
        'about $20',
        'approximately $20',
        'around 20',
        'around $20',
        'around the $20',
        'around twenty pounds',
        'averages $20',
        'in the $20 price range',
        'in the 20 pound price range',
        'is a $20',
        'only cost $20',
        'price is $20',
        'price of $20',
        'price of only $20',
        'price range is 20',
        'price range of 20',
        'price range of $20',
        'pricing of $20',
        'roughly $20',
        'spend $20 or so'
    ]
    a_price_less_20 = [
        '$8',
        '$10',
        '$19.99',
        '20 below',
        '20 less',
        '20 pound and below',
        '20 pound or below',
        '20 pounds or less',
        '20 and below',
        '20 and less',
        '20 and lower',
        '20 and under',
        '20 or below',
        '20 or less',
        'below 20',
        'below $20',
        'below twenty',
        'cheaper than $20',
        'less than $20',
        'less than 20',
        'less than 20lb',
        'less than twenty',
        'less the mere price of 20',
        'low near to 20',
        'lower $20',
        'lower than 20',
        'lower than $20',
        'lower prices to $20',
        'lower prices than $20',
        'no more than $20',
        'under $20',
        'under 20',
        'under twenty',
        'up to $20',
        'very low near to 20',
        'within a price range of twenty pounds',
        'within twenty'
    ]
    a_price_more_30 = [
        '30$',
        '30pound',
        '30 and up price',
        '30 pound',
        '30 or more',
        '$30',
        '$35',
        '$30 and above',
        '$30 and over',
        '$30 and up',
        '$30 minimum',
        '$30 or more',
        '$30 plus',
        '$30 price minimum',
        '$30-priced',
        '$30 upwards',
        'above 30',
        'above thirty',
        'average cost is $30',
        'as low as $30',
        'cheap at $30',
        'cost is $30',
        'exceeding 30',
        'from $30',
        'greater than 30',
        'higher than 30',
        'in the 30 price range',
        'minimum cost of $30',
        'more $30',
        'more than $30',
        'more than 30',
        'more than thirty',
        'over $30',
        'over 30',
        'over thirty',
        'price range is about 30',
        'price range of about 30',
        'price range of 30',
        'price range of $30',
        'starting at 30',
        'starting at $30',
        'the cheapest item is $30',
        'thirty and up',
        'thirty pounds and above',
        'upwards of 30'
    ]
    a_price_cheap = [
        'below average',
        'below-average',
        'cheap american food',
        'cheap and cheerful chinese food',
        'cheap british food',
        'cheap canadian food',
        'cheap chinese food',
        'cheap coffee shop',
        'cheap eats',
        'cheap english pub',
        'cheap english restaurant',
        'cheap fast food',
        'cheap french food',
        'cheap indian food',
        'cheap italian food',
        'cheap japanese food',
        'cheap food',
        'cheap place',
        'cheap price',
        'cheap pricing',
        'cheap pub',
        'cheaply price',
        'cheaply-price',
        'cheap restaurant',
        'discount price',
        'inexpensive',
        'is a cheap',
        'is cheap',
        'low cost',
        'low price',
        'low pricing',
        'low food price range',
        'low range price',
        'low in cost',
        'low in price',
        'low, but so are the price',
        'low-cost',
        'low-price',
        'lower price',
        'lower-price',
        'lower than average',
        'lowest price',
        'price is low',
        'price range is low',
        'priced low',
        'prices are cheap',
        'prices are a steal',
        'prices are in the low',
        'prices are low',
        'prices are very low',
        'prices low',
        'the prices at @NAME@ are low',
        'with cheap'
    ]
    a_price_cheap_tmp = [
        'prices will blow you away',
        'bargain food',
        'bargain price',
        'low rated price',
        'price is less than expected',
        'budget price',
        'prices and quality are substandard',
        'prices are amazing',
        'affordable',
        'affordably price',
        'attractive price',
        'conveniently price',
        'prices are competitive',
        'competitive price',
        'competitively price',
        'economically price',
        'exclusively priced',
        'less than average',
        'less than expected',
        'reduced price',
        'remarkable price',
        'tight budget',
        'value price',
        'great price',
        'great value food'
    ]
    a_price_high = [
        'costly',
        'costing a lot',
        'exclusive price',
        'expensive',
        'fairly expensive',
        'high customer ratings and prices',
        'high charging',
        'high class price',
        'high cost',
        'high-cost',
        'high end price',
        'high-end price',
        'high in price',
        'high on price',
        'high price',
        'high range',
        'high ranging price',
        'high customer rating, and price',
        'high quality and price',
        'high-price',
        'higher cost',
        'higher end price',
        'higher end of the price',
        'higher in price',
        'higher price',
        'higher than average',
        'higher than normal price',
        'higher than usual price',
        'highly price',
        'highly-price',
        'higher-price',
        'higher-than-average price',
        'more than the average price',
        'not cheap',
        'overpriced',
        'overly price',
        'price a little high',
        'price high',
        'price is a bit high',
        'price is a little high',
        'price is also very high',
        'price is fairly high',
        'price is high',
        'price is in the high',
        'price is kind of high',
        'price is more than average',
        'price is pretty high',
        'price range being high',
        'price range begin high',
        'price range high',
        'price range is a bit steep',
        'price range is a little high',
        'price range is little high',
        'price range is high',
        'price range is on the high',
        'price range is quite high',
        'price range is somewhat high',
        'price range is typically high',
        'price range is very high',
        'price range at the wrestlers is said to be high',
        'price range of begin high',
        'price range of high',
        'price ranged high',
        'price ranges to high',
        'price range of food there is high',
        'priced a bit high',
        'priced a little high',
        'priced high',
        'priced in the higher range',
        'priced in the higher margin',
        'priced on the higher end',
        'prices a bit high',
        'prices are a bit high',
        'prices are a little high',
        'prices are high',
        'prices are on the high',
        'prices are quite high',
        'prices are ridiculously high',
        'prices are somewhat high',
        'prices in the higher range',
        'price is steep',
        'prices are somewhat steep',
        'prices at zizzi, a coffee shop in riverside, might be high',
        'prices being on the high',
        'prices for this restaurant are high',
        'prices in the high-end range',
        'prices ranging in the high',
        'prices that range high',
        'prices of the food can be high',
        'price of the food is high',
        'prices on the higher end',
        'prices on the higher side',
        'pricey',
        'prices of their english food can be high',
        'price range of the fitzbillies is high',
        'pricing on the high end',
        'price range of the restaurant taste of cambridge is high',
        'price of this food is high',
        'price of its beverages is high',
        'price range is a little more than normal',
        'prices at the english pub are high',
        'priced in the higher margin',
        'rather expensive',
        'rich price',
        'upper price range',
        'upper range price',
        'upper-end price'
    ]
    a_price_high_tmp = [
        'above average',
        'at a price',
        'charges a bit more than the average',
        'decent-priced',
        'decent price',
        'decent pricing',
        'decently price',
        'premium price',
        'prices are decent',
        'price is in a decent range',
        'price range is a bit higher than most',
        'price range is decent',
        'price ranges are not shabby',
        'prices as well as the reviews are decent',
        'professionally price',
        'upscale price',
        'worth the price'
    ]
    a_price_moderate = [
        'reasonable',
        '@A@ cost',
        '@A@ customer price range',
        '@A@ fee',
        '@A@ in price',
        '@A@ in pricing',
        '@A@ price',
        '@A@ pricing',
        '@B@ pricing',
        '@A@ range',
        '@A@-price',
        '@B@ price',
        '@B@-price',
        'average food price',
        'average rating and price',
        'average service and prices',
        'averaged price',
        'averaged-price',
        'averagely rated and priced',
        'average in both customer ratings and price range',
        'average cambridge price',
        'averages prices',
        'medium price',
        'medium-price',
        'medium range price',
        'medium-range price',
        'mid cost',
        'mid price',
        'mid range bracket',
        'mid range price',
        'mid ranged price',
        'middle price',
        'middle range price',
        'middling price',
        'mid-cost',
        'mid-level price',
        'mid-price',
        'mid-range pri',
        'moder price',
        'modest price',
        'modestly price',
        'normal price',
        'price @A@',
        'price are @A@',
        'price are @A@',
        'price are really @A@',
        'price is @A@',
        'price is pretty @A@',
        'price range @A@',
        'price range are @A@',
        'price range in @A@',
        'price range in the @A@',
        'price range is @A@',
        'price range is about @A@',
        'price range is from very @A@',
        'price range of @A@',
        'price range that is @A@',
        'price range that is rather @A@',
        'price range there is @A@',
        'price range which is @A@',
        'price ranges are @A@',
        'price ranging @A@',
        'price range and its rating is average',
        'price range and customer rating are both rated as average',
        'price range for this restaurant is @A@',
        'priced @A@',
        'priced in @A@',
        'prices @A@',
        'prices are @A@',
        'prices are fairly @A@',
        'prices are in the @A@',
        'prices are middle',
        'prices are mid-level',
        'prices are ok',
        'prices are quite @A@',
        'prices are very @A@',
        'prices and customer ratings are @A@',
        'prices fall in the @A@',
        'prices for meals are @A@',
        'prices in the @A@',
        'prices range in the @A@',
        'prices range is @A@',
        'prices range is really @A@',
        'prices range that is rather @A@',
        'prices ranges are @A@',
        'pricing is @A@',
        'remains @A@',
        'worth the bite'
    ]
    a_price_moderate_tmp = [
        'accessible price',
        'price range is a little more than your mom and pop restaurant',
        'quality is all right for the money',
        'excellent price',
        'fantastic price',
        'fair price',
        'fair-price',
        'fairly price',
        'fairly-price',
        'good price',
        'gourmet price',
        'mid-level price',
        'modern price',
        'modernly price',
        'nice price',
        'okay price',
        'price is not that bad',
        'regularly priced',
        'sensibly price',
        'suitable price',
        'well priced',
        'with a price tag to match'
    ]
    a_variation_pricerange_moderate_A = ['average', 'moderate', 'reasonable']
    a_variation_pricerange_moderate_B = ['averagely', 'moderately', 'moderating', 'reasonably']

    # all status
    obj_new['mr']['priceRange'] = ''
    flag = False
    if flag is False:
        a_reason = []
        a_loc = []
        for keyword in a_price_less_20:
            if keyword in obj_new['txt']:
                obj_new['mr']['priceRange'] = 'less than $20'
                #obj_new['reason']['priceRange'] = keyword
                #flag = True
                #break
                a_reason.append(keyword)
                a_loc.append(obj_new['txt'].find(keyword))
        if len(a_reason) > 0:
            obj_new['reason']['priceRange'] = a_reason[np.array(a_loc).argmin()]
            flag = True

    if flag is False:
        a_reason = []
        a_loc = []
        for keyword in a_price_more_30:
            if keyword in obj_new['txt']:
                obj_new['mr']['priceRange'] = 'more than $30'
                #obj_new['reason']['priceRange'] = keyword
                #flag = True
                #break
                a_reason.append(keyword)
                a_loc.append(obj_new['txt'].find(keyword))
        if len(a_reason) > 0:
            obj_new['reason']['priceRange'] = a_reason[np.array(a_loc).argmin()]
            flag = True

    if flag is False:
        a_reason = []
        a_loc = []
        for keyword in a_price_20_25:
            if keyword in obj_new['txt']:
                obj_new['mr']['priceRange'] = '$20-25'
                #obj_new['reason']['priceRange'] = keyword
                #flag = True
                #break
                a_reason.append(keyword)
                a_loc.append(obj_new['txt'].find(keyword))
        if len(a_reason) > 0:
            obj_new['reason']['priceRange'] = a_reason[np.array(a_loc).argmin()]
            flag = True

    if flag is False:
        a_reason = []
        a_loc = []
        for keyword in a_price_20_25_tmp:
            if keyword in obj_new['txt']:
                obj_new['mr']['priceRange'] = '$20-25'
                #obj_new['reason']['priceRange'] = keyword
                #flag = True
                #break
                a_reason.append(keyword)
                a_loc.append(obj_new['txt'].find(keyword))
        if len(a_reason) > 0:
            obj_new['reason']['priceRange'] = a_reason[np.array(a_loc).argmin()]
            flag = True

    if flag is False:
        a_reason = []
        a_loc = []
        for keyword in a_price_high:
            if keyword in obj_new['txt']:
                obj_new['mr']['priceRange'] = 'high'
                #obj_new['reason']['priceRange'] = keyword
                #flag = True
                #break
                a_reason.append(keyword)
                a_loc.append(obj_new['txt'].find(keyword))
        if len(a_reason) > 0:
            obj_new['reason']['priceRange'] = a_reason[np.array(a_loc).argmin()]
            flag = True

    if flag is False:
        a_reason = []
        a_loc = []
        for keyword in a_price_high_tmp:
            if keyword in obj_new['txt']:
                obj_new['mr']['priceRange'] = 'high'
                #obj_new['reason']['priceRange'] = keyword
                #flag = True
                #break
                a_reason.append(keyword)
                a_loc.append(obj_new['txt'].find(keyword))
        if len(a_reason) > 0:
            obj_new['reason']['priceRange'] = a_reason[np.array(a_loc).argmin()]
            flag = True

    if flag is False:
        a_reason = []
        a_loc = []
        for keyword in a_price_moderate:
            if '@A@' in keyword:
                a_reason_tmp = []
                a_loc_tmp = []
                for word_A in a_variation_pricerange_moderate_A:
                    keyword_tmp = keyword.replace('@A@', word_A)
                    if keyword_tmp in obj_new['txt']:
                        obj_new['mr']['priceRange'] = 'moderate'
                        #obj_new['reason']['priceRange'] = keyword_tmp
                        #flag = True
                        #break
                        a_reason_tmp.append(keyword_tmp)
                        a_loc_tmp.append(obj_new['txt'].find(keyword_tmp))
                #if flag is True:
                #    break
                if len(a_reason_tmp) > 0:
                    obj_new['reason']['priceRange'] = a_reason_tmp[np.array(a_loc_tmp).argmin()]
                    flag = True
                    break
            elif '@B@' in keyword:
                a_reason_tmp = []
                a_loc_tmp = []
                for word_B in a_variation_pricerange_moderate_B:
                    keyword_tmp = keyword.replace('@B@', word_B)
                    if keyword_tmp in obj_new['txt']:
                        obj_new['mr']['priceRange'] = 'moderate'
                        #obj_new['reason']['priceRange'] = keyword_tmp
                        #flag = True
                        #break
                        a_reason_tmp.append(keyword_tmp)
                        a_loc_tmp.append(obj_new['txt'].find(keyword_tmp))
                #if flag is True:
                #    break
                if len(a_reason_tmp) > 0:
                    obj_new['reason']['priceRange'] = a_reason_tmp[np.array(a_loc_tmp).argmin()]
                    flag = True
                    break
            else:
                if keyword in obj_new['txt']:
                    obj_new['mr']['priceRange'] = 'moderate'
                    #obj_new['reason']['priceRange'] = keyword
                    #flag = True
                    #break
                    a_reason.append(keyword)
                    a_loc.append(obj_new['txt'].find(keyword))
        if (flag is False) and (len(a_reason) > 0):
            obj_new['reason']['priceRange'] = a_reason[np.array(a_loc).argmin()]
            flag = True

    if flag is False:
        a_reason = []
        a_loc = []
        for keyword in a_price_moderate_tmp:
            if '@A@' in keyword:
                a_reason_tmp = []
                a_loc_tmp = []
                for word_A in a_variation_pricerange_moderate_A:
                    keyword_tmp = keyword.replace('@A@', word_A)
                    if keyword_tmp in obj_new['txt']:
                        obj_new['mr']['priceRange'] = 'moderate'
                        #obj_new['reason']['priceRange'] = keyword_tmp
                        #flag = True
                        #break
                        a_reason_tmp.append(keyword_tmp)
                        a_loc_tmp.append(obj_new['txt'].find(keyword_tmp))
                #if flag is True:
                #    break
                if len(a_reason_tmp) > 0:
                    obj_new['reason']['priceRange'] = a_reason_tmp[np.array(a_loc_tmp).argmin()]
                    flag = True
                    break
            elif '@B@' in keyword:
                a_reason_tmp = []
                a_loc_tmp = []
                for word_B in a_variation_pricerange_moderate_B:
                    keyword_tmp = keyword.replace('@B@', word_B)
                    if keyword_tmp in obj_new['txt']:
                        obj_new['mr']['priceRange'] = 'moderate'
                        #obj_new['reason']['priceRange'] = keyword_tmp
                        #flag = True
                        #break
                        a_reason_tmp.append(keyword_tmp)
                        a_loc_tmp.append(obj_new['txt'].find(keyword_tmp))
                #if flag is True:
                #    break
                if len(a_reason_tmp) > 0:
                    obj_new['reason']['priceRange'] = a_reason_tmp[np.array(a_loc_tmp).argmin()]
                    flag = True
                    break
            else:
                if keyword in obj_new['txt']:
                    obj_new['mr']['priceRange'] = 'moderate'
                    #obj_new['reason']['priceRange'] = keyword
                    #flag = True
                    #break
                    a_reason.append(keyword)
                    a_loc.append(obj_new['txt'].find(keyword))
        if (flag is False) and (len(a_reason) > 0):
            obj_new['reason']['priceRange'] = a_reason[np.array(a_loc).argmin()]
            flag = True

    if flag is False:
        a_reason = []
        a_loc = []
        for keyword in a_price_cheap:
            if '@NAME@' in keyword:
                a_reason_tmp = []
                a_loc_tmp = []
                for word_name in value_list['name']:
                    keyword_tmp = keyword.replace('@NAME@', word_name)
                    if keyword_tmp in obj_new['txt']:
                        obj_new['mr']['priceRange'] = 'cheap'
                        #obj_new['reason']['priceRange'] = keyword_tmp
                        #flag = True
                        #break
                        a_reason_tmp.append(keyword_tmp)
                        a_loc_tmp.append(obj_new['txt'].find(keyword_tmp))
                #if flag is True:
                #    break
                if len(a_reason_tmp) > 0:
                    obj_new['reason']['priceRange'] = a_reason_tmp[np.array(a_loc_tmp).argmin()]
                    flag = True
                    break
            else:
                if keyword in obj_new['txt']:
                    obj_new['mr']['priceRange'] = 'cheap'
                    #obj_new['reason']['priceRange'] = keyword
                    #flag = True
                    #break
                    a_reason.append(keyword)
                    a_loc.append(obj_new['txt'].find(keyword))
        if (flag is False) and (len(a_reason) > 0):
            obj_new['reason']['priceRange'] = a_reason[np.array(a_loc).argmin()]
            flag = True

    if flag is False:
        a_reason = []
        a_loc = []
        for keyword in a_price_cheap_tmp:
            if '@NAME@' in keyword:
                a_reason_tmp = []
                a_loc_tmp = []
                for word_name in value_list['name']:
                    keyword_tmp = keyword.replace('@NAME@', word_name)
                    if keyword_tmp in obj_new['txt']:
                        obj_new['mr']['priceRange'] = 'cheap'
                        #obj_new['reason']['priceRange'] = keyword_tmp
                        #flag = True
                        #break
                        a_reason_tmp.append(keyword_tmp)
                        a_loc_tmp.append(obj_new['txt'].find(keyword_tmp))
                #if flag is True:
                #    break
                if len(a_reason_tmp) > 0:
                    obj_new['reason']['priceRange'] = a_reason_tmp[np.array(a_loc_tmp).argmin()]
                    flag = True
                    break
            else:
                if keyword in obj_new['txt']:
                    obj_new['mr']['priceRange'] = 'cheap'
                    #obj_new['reason']['priceRange'] = keyword
                    #flag = True
                    #break
                    a_reason.append(keyword)
                    a_loc.append(obj_new['txt'].find(keyword))
        if (flag is False) and (len(a_reason) > 0):
            obj_new['reason']['priceRange'] = a_reason[np.array(a_loc).argmin()]
            flag = True

    if (obj_new['mr']['priceRange'] == '') and ('cheap' in obj_new['txt']):
        #print('[CHEAP!!]]('+str(obj_new['id'])+') ('+str(obj_new['mr']['priceRange'])+')')
        #print(obj_new['txt'])
        obj_new['mr']['priceRange'] = 'cheap'
        obj_new['reason']['priceRange'] = 'cheap'
        flag = True

    # check opposite words/phrases
    a_check_cheap = ['inexpensive']
    a_reason = []
    a_loc = []
    for cheap in a_check_cheap:
        if cheap in obj_new['txt']:
            obj_new['mr']['priceRange'] = 'cheap'
            #obj_new['reason']['priceRange'] = cheap
            a_reason.append(cheap)
            a_loc.append(obj_new['txt'].find(cheap))
    if len(a_reason) > 0:
        obj_new['reason']['priceRange'] = a_reason[np.array(a_loc).argmin()]

    a_check_high = ['not cheap']
    a_reason = []
    a_loc = []
    for high in a_check_high:
        if high in obj_new['txt']:
            obj_new['mr']['priceRange'] = 'high'
            #obj_new['reason']['priceRange'] = high
            a_reason.append(high)
            a_loc.append(obj_new['txt'].find(high))
    if len(a_reason) > 0:
        obj_new['reason']['priceRange'] = a_reason[np.array(a_loc).argmin()]

    # rename 'high' -> 'expensive'
    if obj_new['mr']['priceRange'] == 'high':
        obj_new['mr']['priceRange'] = 'expensive'

    if verbose_flag is True:
        if (obj_new['mr']['priceRange'] == '') and (mr_old['priceRange'] != ''):
            print('[NULL:priceRange] ('+mr_old['priceRange']+')')
            print(obj_new['txt'])

    return obj_new

# (6) customer rating (1 out of 5, 3 out of 5, 5 out of 5, average, high, low)
def extract_customer_rating(obj_new, value_list, verbose_flag, mr_old):
    a_customer_1 = [
        '1 customer rating',
        '1 on a scale of',
        '1 on the scale of',
        '1 out of 5',
        '1 out of five',
        '1 star',
        '1 to 5',
        '1-5',
        '1-out-of-5',
        '1-star',
        'one out of a possible five',
        'one out of 5',
        'one out of five',
        'one star',
        'one to five',
        'one-star',
        'rated 1',
        'rated number 1',
        'rating it as 1',
        'customer rating of one'
    ]
    a_customer_3 = [
        '3 customer rating',
        '3 on a scale of',
        '3 on the scale of',
        '3 out of 5',
        '3 out of five',
        '3 rating on a scale of',
        '3 star',
        '3 to 5',
        '3, on a scale of',
        '3-5',
        '3-out-of-5',
        '3-star',
        '3/5',
        '3 point rating out of 5',
        'three out of 5',
        'three out of five',
        'three star',
        'three to five',
        'three-star',
        'rating of 3',
        'rating it as 3'
    ]
    a_customer_5 = [
        '5 customer rating',
        '5 out of 5',
        '5 out of five',
        '5 star',
        '5 to 5',
        '5-5',
        '5-out-of-5',
        '5-star',
        'five out of 5',
        'five out of five',
        'five star',
        'five to five',
        'five-star',
        'rating it as 5'
    ]
    a_customer_low = [
        '@LOW@ are below average',
        '@LOW@ are low',
        '@LOW@ are not high',
        '@LOW@ are poor',
        '@LOW@ are quite low',
        '@LOW@ as low',
        '@LOW@ being low',
        '@LOW@ below average',
        '@LOW@ browns cambridge low',
        '@LOW@ clowns as low',
        '@LOW@ in low',
        '@LOW@ is bad',
        '@LOW@ is bit low',
        '@LOW@ is currently low',
        '@LOW@ is low',
        '@LOW@ is poor',
        '@LOW@ is pretty low',
        '@LOW@ is quite low',
        '@LOW@ is rather low',
        '@LOW@ is somewhat low',
        '@LOW@ is a tad low',
        '@LOW@ is very low',
        '@LOW@ is very poor',
        '@LOW@ it as low',
        '@LOW@ it low',
        '@LOW@ loch fyne as low',
        '@LOW@ low',
        '@LOW@ midsummer house low',
        '@LOW@ of low',
        '@LOW@ pretty low',
        '@LOW@ range is low',
        '@LOW@ score of low',
        '@LOW@ that is low',
        '@LOW@ the coffee shop as low',
        '@LOW@ the place low',
        '@LOW@ there are low',
        '@LOW@ this low',
        '@LOW@ very low',
        'bad @LOW@',
        'bad customer @LOW@',
        'badly @LOW@',
        'customer rating of it is low',
        'customer rating, however, is low',
        'customer reviews are not great',
        'customers have rated @NAME@ located close to @NEAR@ as low',
        'not have high review',
        'low @LOW@',
        'low a @LOW@',
        'low approval @LOW@',
        'low client @LOW@',
        'low consumer @LOW@',
        'low customer @LOW@',
        'low customer approval @LOW@',
        'low customer satisfaction @LOW@',
        'low customer service @LOW@',
        'low customer-@LOW@',
        'low customer-@LOW@',
        'low customers @LOW@',
        'low in customer @LOW@',
        'low in the @LOW@',
        'low priced and @LOW@',
        'low prices and @LOW@',
        'low quality',
        'low satisfaction',
        'low star @LOW@',
        'low starred',
        'low-@LOW@',
        'low-customer-@LOW@',
        'low-quality',
        'lower than average @LOW@',
        'lower @LOW@',
        'lowly @LOW@',
        'lowly-@LOW@',
        'mediocre @LOW@',
        'not rated highly',
        'not got a good @LOW@',
        'not have good review',
        'not highly @LOW@',
        'not of very good quality',
        'not @LOW@ well',
        '@LOW@ poor',
        'poor @LOW@',
        'poor customer @LOW@',
        'poor in @LOW@',
        'poor quality',
        'poor standard',
        'poor-@LOW@',
        'poor-quality',
        'poorly @LOW@',
        'poorly-@LOW@',
        'ratings for @NAME@ restaurant are low',
        'reviews aren\'t great',
        'terrible @LOW@'
    ]
    a_customer_average = [
        'not 1 out of 5 rank but in the moderate range',
        ' as average',
        ', average.'
        '@AVE@ @NAME@ as average',
        '@AVE@ @NAME@ average',
        '@AVE@ for @NAME@ is average',
        '@AVE@ about average',
        '@AVE@ an average',
        '@AVE@ are average',
        '@AVE@ are only average',
        '@AVE@ as an average',
        '@AVE@ as average',
        '@AVE@ as \'average\'',
        '@AVE@ at average',
        '@AVE@ average',
        '@AVE@ being average',
        '@AVE@ by customers as average',
        '@AVE@ in average',
        '@AVE@ is about average',
        '@AVE@ is an average',
        '@AVE@ is as average',
        '@AVE@ is average',
        '@AVE@ is \'average\'',
        '@AVE@ is just average',
        '@AVE@ is only average',
        '@AVE@ is typically average',
        '@AVE@ it as average',
        '@AVE@ it at average',
        '@AVE@ it average',
        '@AVE@ of average',
        '@AVE@ on average',
        '@AVE@ on the average',
        '@AVE@ that is average',
        '@AVE@ the establishment as average',
        '@AVE@ the food as average',
        '@AVE@ the food average',
        '@AVE@ them average',
        '@AVE@ this as average',
        '@AVE@ this place an average',
        '@AVE@ this pub average',
        '@AVE@ to be average',
        '@AVE@ were average',
        '@AVE@ which are average',
        '@AVE@: average',
        'average @AVE@',
        'average by customer @AVE@',
        'average consumer @AVE@',
        'average customer @AVE@',
        'average customer satisfaction @AVE@',
        'average customer service @AVE@',
        'average customer-@AVE@',
        'average customers @AVE@',
        'average customer\'s @AVE@',
        'average family friendly @AVE@',
        'average in @AVE@',
        'average in customer @AVE@',
        'average place',
        'average price @AVE@',
        'average price and @AVE@',
        'average quality',
        'average restaurant @AVE@',
        'average satisfaction @AVE@',
        'average user @AVE@',
        'average-@AVE@',
        'average-quality',
        'averagely @AVE@',
        'averagely-@AVE@',
        'averaged @AVE@',
        'customer reviews have been average',
        'customer satisfaction is average',
        'customers rate their experience as average',
        'customers rate @NAME@ coffee shop, near @NEAR@, average',
        'customers rate @NAME@ pub, near @NEAR@, average',
        'customer rating of this shop is average',
        'customer rating so far average',
        'customer rating however is only average',
        'customer rating is really great, they have a yes average',
        'customers rating they think it is average',
        'customer ratings so far are average',
        'mid range customer @AVE@',
        'mid range customer\' @AVE@',
        'mid-ranged rating',
        'moderate @AVE@',
        'moderate customer @AVE@',
        'moderate customer\' @AVE@',
        'moderately @AVE@',
        'moderately-rated',
        'prices and customer ratings are @AVE@',
        'rating by customers is average',
        'ratings for @NAME@ restaurant are average',
        'rated and priced averagely',
        'your average pub'
    ]
    a_customer_average_tmp = [
        'good quality',
        'good standard',
        'good-quality',
        'okay reviews',
        'well priced quality'
    ]
    a_customer_high = [
        ' as high',
        '9 to 10 stars',
        '@HIGH@ above average',
        '@HIGH@ are above average',
        '@HIGH@ are decent',
        '@HIGH@ are great',
        '@HIGH@ are high',
        '@HIGH@ are so high',
        '@HIGH@ are very high',
        '@HIGH@ as high',
        '@HIGH@ good',
        '@HIGH@ high',
        '@HIGH@ in high',
        '@HIGH@ is above average',
        '@HIGH@ is high',
        '@HIGH@ is not low',
        '@HIGH@ is not abysmal',
        '@HIGH@ is relative high',
        '@HIGH@ is so high',
        '@HIGH@ is very high',
        '@HIGH@ it as high',
        '@HIGH@ it high',
        '@HIGH@ it very high',
        '@HIGH@ like high',
        '@HIGH@ not low',
        '@HIGH@ of high',
        '@HIGH@ quite high',
        '@HIGH@ that is high',
        '@HIGH@ the punter high',
        '@HIGH@ this restaurant high',
        '@HIGH@ very high',
        '@HIGH@ where high',
        '@HIGH@ wildwood high',
        '@HIGH@ the @NAME@ pub highly',
        'customer rating for @NAME@ is @HIGH@',
        'customers rate it very well',
        'customer rating for this coffee shop is high',
        'customer rating for this restaurant is high',
        'decent @HIGH@',
        'decent reviews',
        'excellent @HIGH@',
        'excellent customer @HIGH@',
        'excellent quality',
        'excellently @HIGH@',
        'good @HIGH@',
        'good customer @HIGH@',
        'great @HIGH@',
        'great customer @HIGH@',
        'great quality',
        'great-quality',
        'greatly @HIGH@',
        'high @HIGH@',
        'high customer approval rate',
        'high customer @HIGH@',
        'high customer\' @HIGH@',
        'high customer satisfaction',
        'high customer service',
        'high customer service @HIGH@',
        'high customer-@HIGH@',
        'high customers @HIGH@',
        'high end quality',
        'high prices and @HIGH@',
        'high quality',
        'high satisfaction',
        'high standard',
        'high yes @HIGH@',
        'high-@HIGH@',
        'high @HIGH@',
        'high ranking in customer',
        'high-quality',
        'higher customer @HIGH@',
        'higher @HIGH@',
        'highly @HIGH@',
        'highly consumer @HIGH@',
        'highly customer @HIGH@',
        'highly priced and @HIGH@',
        'highly rated',
        'highly-@HIGH@',
        'highly-consumer-@HIGH@',
        'highly-customer-@HIGH@',
        'perfect @HIGH@', 
        'perfect customer @HIGH@',
        'pretty good @HIGH@',
        'quality is amazing',
        'quality is very high',
        'quality is top notch',
        'ratings for @NAME@ restaurant are high',
        'scores high',
        'top-rated',
        'top quality customer @HIGH@',
        'well @HIGH@',
        'well-@HIGH@'
    ]
    a_variation_customer_rating = [
        'rate', 'rated', 'rates', 'rating', 'ratings', 'review', 'reviews'
    ]
    obj_new['mr']['customer rating'] = ''
    flag = False
    a_reason = []
    a_loc = []
    for keyword in a_customer_1:
        if keyword in obj_new['txt']:
            obj_new['mr']['customer rating'] = '1 out of 5'
            #obj_new['reason']['customer rating'] = keyword
            #flag = True
            #break
            a_reason.append(keyword)
            a_loc.append(obj_new['txt'].find(keyword))
    if (flag is False) and (len(a_reason) > 0):
        obj_new['reason']['customer rating'] = a_reason[np.array(a_loc).argmin()]
        flag = True

    if flag is False:
        a_reason = []
        a_loc = []
        for keyword in a_customer_3:
            if keyword in obj_new['txt']:
                obj_new['mr']['customer rating'] = '3 out of 5'
                #obj_new['reason']['customer rating'] = keyword
                #flag = True
                #break
                a_reason.append(keyword)
                a_loc.append(obj_new['txt'].find(keyword))
        if (flag is False) and (len(a_reason) > 0):
            obj_new['reason']['customer rating'] = a_reason[np.array(a_loc).argmin()]
            flag = True

    if flag is False:
        a_reason = []
        a_loc = []
        for keyword in a_customer_5:
            if keyword in obj_new['txt']:
                obj_new['mr']['customer rating'] = '5 out of 5'
                #obj_new['reason']['customer rating'] = keyword
                #flag = True
                #break
                a_reason.append(keyword)
                a_loc.append(obj_new['txt'].find(keyword))
        if (flag is False) and (len(a_reason) > 0):
            obj_new['reason']['customer rating'] = a_reason[np.array(a_loc).argmin()]
            flag = True

    if flag is False:
        a_reason = []
        a_loc = []
        for keyword in a_customer_low:
            if '@LOW@' in keyword:
                for word in a_variation_customer_rating:
                    keyword_tmp = keyword.replace('@LOW@', word)
                    if keyword_tmp in obj_new['txt']:
                        obj_new['mr']['customer rating'] = 'low'
                        #obj_new['reason']['customer rating'] = keyword_tmp
                        #flag = True
                        #break
                        a_reason.append(keyword_tmp)
                        a_loc.append(obj_new['txt'].find(keyword_tmp))
                #if flag is True:
                #    break
            else:
                if keyword in obj_new['txt']:
                    obj_new['mr']['customer rating'] = 'low'
                    #obj_new['reason']['customer rating'] = keyword
                    #flag = True
                    #break
                    a_reason.append(keyword)
                    a_loc.append(obj_new['txt'].find(keyword))
        if (flag is False) and (len(a_reason) > 0):
            obj_new['reason']['customer rating'] = a_reason[np.array(a_loc).argmin()]
            flag = True

    if flag is False:
        a_reason = []
        a_loc = []
        for keyword in a_customer_average:
            if '@AVE@' in keyword:
                for word_ave in a_variation_customer_rating:
                    keyword_tmp = keyword.replace('@AVE@', word_ave)
                    if '@NAME@' in keyword:
                        for word_name in value_list['name']:
                            keyword_tmp2 = keyword_tmp.replace('@NAME@', word_name)
                            if keyword_tmp2 in obj_new['txt']:
                                obj_new['mr']['customer rating'] = 'average'
                                #obj_new['reason']['customer rating'] = keyword_tmp2
                                #flag = True
                                #break
                                a_reason.append(keyword_tmp2)
                                a_loc.append(obj_new['txt'].find(keyword_tmp2))

                            if '@NEAR@' in keyword:
                                for word_near in value_list['near']:
                                    keyword_tmp3 = keyword_tmp2.replace('@NEAR@', word_near)
                                    if keyword_tmp3 in obj_new['txt']:
                                        obj_new['mr']['customer rating'] = 'average'
                                        #obj_new['reason']['customer rating'] = keyword_tmp3
                                        #flag = True
                                        #break
                                        a_reason.append(keyword_tmp3)
                                        a_loc.append(obj_new['txt'].find(keyword_tmp3))
                        #if flag is True:
                        #    break
                    else:
                        if keyword_tmp in obj_new['txt']:
                            obj_new['mr']['customer rating'] = 'average'
                            #obj_new['reason']['customer rating'] = keyword_tmp
                            #flag = True
                            #break
                            a_reason.append(keyword_tmp)
                            a_loc.append(obj_new['txt'].find(keyword_tmp))
            else:
                if keyword in obj_new['txt']:
                    obj_new['mr']['customer rating'] = 'average'
                    #obj_new['reason']['customer rating'] = keyword
                    #flag = True
                    #break
                    a_reason.append(keyword)
                    a_loc.append(obj_new['txt'].find(keyword))
                if '@NAME@' in keyword:
                    for word_name in value_list['name']:
                        keyword_tmp2 = keyword.replace('@NAME@', word_name)
                        if keyword_tmp2 in obj_new['txt']:
                            obj_new['mr']['customer rating'] = 'average'
                            #obj_new['reason']['customer rating'] = keyword_tmp2
                            #flag = True
                            #break
                            a_reason.append(keyword_tmp2)
                            a_loc.append(obj_new['txt'].find(keyword_tmp2))

                        if '@NEAR@' in keyword:
                            for word_near in value_list['near']:
                                keyword_tmp3 = keyword_tmp2.replace('@NEAR@', word_near)
                                if keyword_tmp3 in obj_new['txt']:
                                    obj_new['mr']['customer rating'] = 'average'
                                    #obj_new['reason']['customer rating'] = keyword_tmp3
                                    #flag = True
                                    #break
                                    a_reason.append(keyword_tmp3)
                                    a_loc.append(obj_new['txt'].find(keyword_tmp3))
        if (flag is False) and (len(a_reason) > 0):
            obj_new['reason']['customer rating'] = a_reason[np.array(a_loc).argmin()]
            flag = True

    if flag is False:
        a_reason = []
        a_loc = []
        for keyword in a_customer_average_tmp:
            if '@AVE@' in keyword:
                for word_ave in a_variation_customer_rating:
                    keyword_tmp = keyword.replace('@AVE@', word_ave)
                    if '@NAME@' in keyword:
                        for word_name in value_list['name']:
                            keyword_tmp2 = keyword_tmp.replace('@NAME@', word_name)
                            if keyword_tmp2 in obj_new['txt']:
                                obj_new['mr']['customer rating'] = 'average'
                                #obj_new['reason']['customer rating'] = keyword_tmp2
                                #flag = True
                                #break
                                a_reason.append(keyword_tmp2)
                                a_loc.append(obj_new['txt'].find(keyword_tmp2))
                        #if flag is True:
                        #    break
                    else:
                        if keyword_tmp in obj_new['txt']:
                            obj_new['mr']['customer rating'] = 'average'
                            #obj_new['reason']['customer rating'] = keyword_tmp
                            #flag = True
                            #break
                            a_reason.append(keyword_tmp)
                            a_loc.append(obj_new['txt'].find(keyword_tmp))
            else:
                if keyword in obj_new['txt']:
                    obj_new['mr']['customer rating'] = 'average'
                    #obj_new['reason']['customer rating'] = keyword
                    #flag = True
                    #break
                    a_reason.append(keyword)
                    a_loc.append(obj_new['txt'].find(keyword))
                if '@NAME@' in keyword:
                    for word_name in value_list['name']:
                        keyword_tmp2 = keyword.replace('@NAME@', word_name)
                        if keyword_tmp2 in obj_new['txt']:
                            obj_new['mr']['customer rating'] = 'average'
                            #obj_new['reason']['customer rating'] = keyword_tmp2
                            #flag = True
                            #break
                            a_reason.append(keyword_tmp2)
                            a_loc.append(obj_new['txt'].find(keyword_tmp2))
                        if '@NEAR@' in keyword:
                            for word_near in value_list['near']:
                                keyword_tmp3 = keyword_tmp2.replace('@NEAR@', word_near)
                                if keyword_tmp3 in obj_new['txt']:
                                    obj_new['mr']['customer rating'] = 'average'
                                    #obj_new['reason']['customer rating'] = keyword_tmp3
                                    #flag = True
                                    #break
                                    a_reason.append(keyword_tmp3)
                                    a_loc.append(obj_new['txt'].find(keyword_tmp3))
        if (flag is False) and (len(a_reason) > 0):
            obj_new['reason']['customer rating'] = a_reason[np.array(a_loc).argmin()]
            flag = True

    if flag is False:
        a_reason = []
        a_loc = []
        for keyword in a_customer_high:
            if '@HIGH@' in keyword:
                for word_high in a_variation_customer_rating:
                    keyword_tmp = keyword.replace('@HIGH@', word_high)
                    if '@NAME@' in keyword:
                        for word_name in value_list['name']:
                            keyword_tmp2 = keyword_tmp.replace('@NAME@', word_name)
                            if keyword_tmp2 in obj_new['txt']:
                                obj_new['mr']['customer rating'] = 'high'
                                #obj_new['reason']['customer rating'] = keyword_tmp2
                                #flag = True
                                #break
                                a_reason.append(keyword_tmp2)
                                a_loc.append(obj_new['txt'].find(keyword_tmp2))
                            if '@NEAR@' in keyword:
                                for word_near in value_list['near']:
                                    keyword_tmp3 = keyword_tmp2.replace('@NEAR@', word_near)
                                    if keyword_tmp3 in obj_new['txt']:
                                        obj_new['mr']['customer rating'] = 'high'
                                        #obj_new['reason']['customer rating'] = keyword_tmp3
                                        #flag = True
                                        #break
                                        a_reason.append(keyword_tmp3)
                                        a_loc.append(obj_new['txt'].find(keyword_tmp3))
                        #if flag is True:
                        #    break
                    else:
                        if keyword_tmp in obj_new['txt']:
                            obj_new['mr']['customer rating'] = 'high'
                            #obj_new['reason']['customer rating'] = keyword_tmp
                            #flag = True
                            #break
                            a_reason.append(keyword_tmp)
                            a_loc.append(obj_new['txt'].find(keyword_tmp))
                #if flag is True:
                #    break
            else:
                if keyword in obj_new['txt']:
                    obj_new['mr']['customer rating'] = 'high'
                    #obj_new['reason']['customer rating'] = keyword
                    #flag = True
                    #break
                    a_reason.append(keyword)
                    a_loc.append(obj_new['txt'].find(keyword))
        if (flag is False) and (len(a_reason) > 0):
            obj_new['reason']['customer rating'] = a_reason[np.array(a_loc).argmin()]
            flag = True

    if verbose_flag is True:
        if (obj_new['mr']['customer rating'] == '') and (mr_old['customer rating'] != ''):
            print('[NULL:customer rating] ('+mr_old['customer rating']+')')
            print(obj_new['txt'])

    return obj_new

# (7) area
def extract_area(obj_new, verbose_flag, mr_old):
    a_area_centre = [
        'area centre',
        'centre of cambridge',
        'centre of city',
        'centre of the city',
        'centre of town',
        'centre city',
        'cities centre',
        'city centre',
        'city-centre',
        'city\'s centre',
        'in the centre',
        'in the town centre',
        'town centre'
    ]
    a_area_center_no = [
        'outskirts of the city',
        'outside the city',
        'outside of the city',
        'north of city',
        'north of the city',
        'south of the city',
        'northern part of the city',
        'ranch city',
        'end of the city'
    ]
    a_area_riverside = [
        'along side the river',
        'along the river',
        'alongside the river',
        'at the river',
        'banks of the river',
        'beside the river',
        'by a river',
        'by the river',
        'close to the river',
        'edge of the river',
        'from the river',
        'in the river',
        'in river side',
        'is a river side',
        'margin of the river',
        'located by a river',
        'located in the river side',
        'located next to the river',
        'located off the river',
        'located on the river',
        'near a river',
        'near the river',
        'near the thames',
        'next to a river',
        'next to the river',
        'off the river',
        'on the river',
        'overlooks the river',
        'over-looking the river',
        'riverfront',
        'river side',
        'riverside',
        'side of the river',
        'underneath the river',
        'with a river',
        'along the waterfront',
        'located near the water',
        'on the waterfront',
        'next to the water\'s',
        'located by the water',
    ]
    obj_new['mr']['area'] = ''
    flag = False    
    a_reason = []
    a_loc = []
    for keyword in a_area_centre:
        if keyword in obj_new['txt']:
            obj_new['mr']['area'] = 'city centre'
            #obj_new['reason']['area'] = keyword
            #flag = True
            #break
            a_reason.append(keyword)
            a_loc.append(obj_new['txt'].find(keyword))
    if (flag is False) and (len(a_reason) > 0):
        obj_new['reason']['area'] = a_reason[np.array(a_loc).argmin()]
        flag = True

    if flag is False:
        if 'river' in obj_new['txt']:
            obj_new['mr']['area'] = 'riverside'
            obj_new['reason']['area'] = 'river'

    if verbose_flag is True:
        if (obj_new['mr']['area'] == '') and (mr_old['area'] != ''):
            print('[NULL:area] ('+mr_old['area']+')')
            print(obj_new['txt'])

    return obj_new

# (8) familyFriendly
def extract_familyFriendly(obj_new, verbose_flag, mr_old):
    a_family_yes = [
        '@FAMILY@ are allowed',
        '@FAMILY@ are welcome',
        '@FAMILY@ are always welcome',####(2022/9/24)
        '@FAMILY@ are more than welcome',
        '@FAMILY@ are very welcome',
        '@FAMILY@ atmosphere',
        '@FAMILY@ can gather hear',
        '@FAMILY@ family place',
        '@FAMILY@ are friendly',
        '@FAMILY@ dining',
        '@FAMILY@ friend',
        '@FAMILY@ friendly',
        '@FAMILY@ is welcome',
        '@FAMILY@ orientated',
        '@FAMILY@ oriented',
        '@FAMILY@ place',
        '@FAMILY@ space',
        '@FAMILY@ style',
        '@FAMILY@-approved',
        '@FAMILY@-friendliness',
        '@FAMILY@-friendly',
        '@FAMILY@-oriented',
        '@FAMILY@ restaurant',
        '@FAMILY@ will be welcome',
        '@FAMILY@ welcome',
        '@FAMILY@ appropriated',
        'accept all @FAMILY@',
        'accommodate @FAMILY@',
        'accommodates @FAMILY@',
        'allow @FAMILY@',
        'allows @FAMILY@',
        'bring all the @FAMILY@',
        'bring the whole @FAMILY@',
        'bring the @FAMILY@',
        'bring your @FAMILY@',
        'caters to @FAMILY@',
        'customers and @FAMILY@ are friendly',
        'families of all ages',#####(2022/09/24)
        'for you and the @FAMILY@',
        'for all the @FAMILY@',
        'for @FAMILY@',
        'for the whole @FAMILY@',
        'for whole @FAMILY@',
        'for the entire @FAMILY@',
        'for all the @FAMILY@',
        'for adults and kids',
        'friendly clientele',
        'friendly @FAMILY@',
        'friendly for @FAMILY@',
        'friendly to @FAMILY@',
        'friendly with @FAMILY@',
        'family restaurant',
        'family coffee shop',
        'good place to bring @FAMILY@',
        'has @FAMILY@',
        'ideal for anyone on a @FAMILY@',
        'is very friendly place',
        'love @FAMILY@',#####(2022/9/24)
        'offers @FAMILY@',
        'opened to all age groups',
        'place for @FAMILY@',
        'place for your @FAMILY@',
        'place for all the @FAMILY@',
        'relax with @FAMILY@',
        'relax with the @FAMILY@',
        'relax with your @FAMILY@',
        'relax with friends and @FAMILY@',
        'says yes to @FAMILY@',
        'serves @FAMILY@',
        'suitable for everyone and @FAMILY@',
        'suitable for @FAMILY@',
        'tailoring to all ages',#####(2022/9/24)
        'welcoming @FAMILY@',
        'welcome @FAMILY@',
        'welcomes @FAMILY@',
        'welcomes the entire @FAMILY@',
        'welcomes the whole @FAMILY@',
        'welcomes your whole @FAMILY@',
        'whole @FAMILY@ will enjoy',
        'with @FAMILY@',
        'you can take your @FAMILY@',#####(2022/9/24)
        'yes to @FAMILY@',
        'your @FAMILY@ want'#####(2022/9/24),
        'you and your family can',
        'you\'ve got @FAMILY@'
    ]
    a_family_no = [
        '@FAMILY@ are not accommodated',
        '@FAMILY@ are not allowed',
        '@FAMILY@ are not catered',
        '@FAMILY@ are not friendly',
        '@FAMILY@ are not permitted',
        '@FAMILY@ are not welcome',
        '@FAMILY@ aren\'t welcome',
        '@FAMILY@\'s are not welcome',
        '@FAMILY@ aren\'t allowed',
        '@FAMILY@ friendly no',
        '@FAMILY@-friendly no',
        '@FAMILY@ not permitted',
        '@FAMILY@ not welcome',
        '@FAMILY@ should not visit',
        '@FAMILY@ unfriendly',
        '@FAMILY@-unfriendly',
        '@FAMILY@-free',
        '@FAMILY@ free environment',
        '@FAMILY@ and coffee don\'t mix',
        '@FAMILY@ were not being polite',
        '21 and up',
        'adult client',
        'adult crowd',
        'adult directed',
        'adult environment',
        'adult establish',
        'adult establishment',
        'adult friendly',
        'adult only',
        'adult oriented',
        'adult place',
        'adult taste',
        'adult themed',
        'adult-centric',
        'adult-friendly',
        'adult-oriented',
        'adult-only',
        'adults only',
        'adults-only',
        'adults over the age of 19',
        'adults should not bring their @FAMILY@',
        'adults-only',
        'adult parties only',
        'adult atmosphere',
        'adult chinese',
        'adult french',
        'adult indian',
        'adult english',
        'adult japanese',
        'adult, japanese',
        'adult 5 out of 5',
        'adult italian',
        'adult coffee shop',
        'adult dining',
        'adult eatery',
        'adult fast food',
        'adult patron',
        'adult pub',
        'adult restaurant',
        'adult focused',
        'adult location',
        'adult type atmosphere',
        'adult gathering',
        'adult setting',
        'age minimum is 21',
        'anti-@FAMILY@',
        'aimed at adult',
        'aimed at older',
        'appreciates an adult patron',
        'aren\'t friendly to @FAMILY@',
        'aren\'t however @FAMILY@',
        'aren\'t @FAMILY@ friendly',
        'aren\'t @FAMILY@-friendly',
        'by no means @FAMILY@',
        'bringing @FAMILY@ may not',
        'bringing @FAMILY@ is not',
        'n\'t bring @FAMILY@',
        'n\'t bring the @FAMILY@',
        'n\'t bring your @FAMILY@',
        'n\'t bring the whole @FAMILY@',
        'n\'t provide @FAMILY@',
        'n\'t take @FAMILY@',
        'n\'t take the @FAMILY@',
        'n\'t take your @FAMILY@',
        'not bring @FAMILY@',
        'not bring the @FAMILY@',
        'not bring your @FAMILY@',
        'not bring the whole @FAMILY@',
        'not geared towards @FAMILY@',
        'childless',
        'discerning adult',
        'does not serve @FAMILY@',
        'does not accept @FAMILY@',
        'does not allow @FAMILY@',
        'does not cater',
        'does not care for @FAMILY@',
        'does not feel very @FAMILY@',
        'does not welcome @FAMILY@',
        'does not offer cuisine the @FAMILY@',
        'doesn\'t accept @FAMILY@',
        'doesn\'t allow @FAMILY@',
        'doesn\'t serve @FAMILY@',
        'doesn\'t support @FAMILY@',
        'doesn\'t welcome @FAMILY@',
        'doesn\'t cater to @FAMILY@',
        'doesn\'t particularly cater to @FAMILY@',
        'do not have @FAMILY@',
        'do not like @FAMILY@',
        'don\'t accept your @FAMILY@',
        'don\'t bring your @FAMILY@',
        'don\'t bring the @FAMILY@',
        'don\'t take @FAMILY@',
        'don\'t take the @FAMILY@',
        'don\'t take your @FAMILY@',
        'don\'t like @FAMILY@',
        'don\'t like the @FAMILY@',
        'don\'t love @FAMILY@',
        'don\'t love the @FAMILY@',
        'don\'t want to be near @FAMILY@',
        'exclusive adult',
        'family dining is what you seek, this is not it',
        'find a babysitter',
        'for adult',
        'for some adult',
        'for an adult',
        'for all adult',
        'for the busy adult',
        'for our adult',
        'hire a babysitter',
        'mature',####(2022/9/24)
        'isn\'t @FAMILY@',
        'isn\'t @FAMILY@ friendly',
        'isn\'t considered @FAMILY@',
        'isn\'t good for @FAMILY@',
        'isn\'t much for the @FAMILY@',
        'isn\'t really @FAMILY@ friendly',
        'isn\'t really @FAMILY@-friendly',
        'isn\'t very @FAMILY@ friendly',
        'isn\'t very @FAMILY@-friendly',
        'isn\'t place for @FAMILY@',
        'leave @FAMILY@ at home',
        'no amenities for @FAMILY@',
        'no @FAMILY@',
        'no @FAMILY@ friendly',
        'no @FAMILY@-friendly',
        'no facilities for @FAMILY@',
        'no facility for @FAMILY@',
        'no for @FAMILY@',
        'no friendly for @FAMILY@',
        'no go for @FAMILY@',
        'no good for @FAMILY@',
        'no highchairs',
        'no longer @FAMILY@',
        'no noisy @FAMILY@ allowed',
        'no respite for weary parents',
        'no room for a whole @FAMILY@',
        'no to @FAMILY@',
        'no-@FAMILY@-friendly',
        'non @FAMILY@',
        'non-@FAMILY@',
        'not @FAMILY@',
        'not a friendly shop',
        'not a place to bring @FAMILY@',
        'not a place to bring your @FAMILY@',
        'not a place to take @FAMILY@',
        'not a place to take your @FAMILY@',
        'not a very @FAMILY@',
        'not a good family environment',
        'not a good choice for @FAMILY@',
        'not a good location to bring @FAMILY@',
        'not actively welcome @FAMILY@',
        'not accommodate @FAMILY@',
        'not all age',
        'not allow @FAMILY@',
        'not allowed',
        'not appropriate for @FAMILY@',
        'not be @FAMILY@',
        'not be considered @FAMILY@ friendly',
        'not be considered @FAMILY@-friendly',
        'not being @FAMILY@ friendly',
        'not being @FAMILY@-friendly',
        'not classified as @FAMILY@-friendly',
        'not conducive for @FAMILY@',
        'not considered @FAMILY@',
        'not down as @FAMILY@',
        'not especially @FAMILY@',
        'not exactly @FAMILY@',
        'not for all the @FAMILY@',
        'not for whole @FAMILY@',
        'not for the whole @FAMILY@',
        'not for @FAMILY@',
        'not-for-@FAMILY@',
        'not friendly for @FAMILY@',
        'not friendly to @FAMILY@',
        'not friendly with @FAMILY@',
        'not a good place to take @FAMILY@',
        'not good for @FAMILY@',
        'not good for the @FAMILY@',
        'not good for your @FAMILY@',
        'not good location to bring @FAMILY@',
        'not have childhood environment',
        'not however @FAMILY@',
        'not intended for @FAMILY@',
        'not intended for the whole @FAMILY@',
        'not interested in @FAMILY@',
        'not known as @FAMILY@',
        'not known to be @FAMILY@',
        'not likable by @FAMILY@',
        'not offer @FAMILY@',
        'not offer a menu for all ages',
        'not open to @FAMILY@',
        'not opened to all age',
        'not openly welcome @FAMILY@',
        'not oriented toward @FAMILY@',
        'not permit @FAMILY@',
        'not provide @FAMILY@',
        'not really @FAMILY@ friendly',
        'not really @FAMILY@-friendly',
        '@FAMILY@ are not really welcome,'
        'not really welcome @FAMILY@',
        'not so @FAMILY@',
        '@FAMILY@ are not recommended',
        'not recommended for @FAMILY@',
        'not recommended to take @FAMILY@',
        'not recommended to bring @FAMILY@',
        'not recommended for your @FAMILY@',
        'not recommended to take your @FAMILY@',
        'not recommended to bring your @FAMILY@',
        'not serve @FAMILY@',
        'not so @FAMILY@ friendly',
        'not so @FAMILY@-friendly',
        'not suitable @FAMILY@',
        'not suitable place for @FAMILY@',
        'not suitable for young @FAMILY@',
        'not suitable for @FAMILY@',
        'not suitable for customers',
        'not suited for @FAMILY@',
        'not the friendliest place to take the @FAMILY@',
        'not the best place to bring your @FAMILY@',
        'not the most @FAMILY@',
        'not the type of place people bring their @FAMILY@',
        'not to @FAMILY@',
        'not too @FAMILY@',
        'not very @FAMILY@ friendly',
        'not very @FAMILY@-friendly',
        'not viewed as @FAMILY@',
        'not welcoming to @FAMILY@',
        'not welcoming towards @FAMILY@',
        'only adult parties are welcomed',
        'open tall ages',
        'out with @FAMILY@',
        'serve adult',
        'single adult',
        'towards adult',
        'to adult',
        'to an adult'
        'unfriendly @FAMILY@',
        'leave your @FAMILY@',
        'your @FAMILY@ would not find suitable',
        'you don\'t mind leaving the @FAMILY@',
        'wouldn\'t take @FAMILY@',
        'wouldn\'t take your @FAMILY@',
        'wouldn\'t recommend bringing your @FAMILY@'
    ]
    a_article = ['', 'a ', 'the ']
    a_family = ['family', 'families', 'kid', 'kids', 'kiddos', 'child', 'children', 'youngster', 'youngsters']
    a_variation_family = []
    for article in a_article:
        for family in a_family:
            a_variation_family.append(article+family)

    # all status
    obj_new['mr']['familyFriendly'] = ''
    flag = False
    a_reason = []
    a_loc = []
    for keyword in a_family_no:
        if (keyword == 'for adult') and \
           (('adult and kid' in obj_new['txt']) or \
            ('adults and kid' in obj_new['txt'])):
            continue

        if '@FAMILY@' in keyword:
            for keyword_family in a_variation_family:
                keyword_tmp = keyword.replace('@FAMILY@', keyword_family)
                if keyword_tmp in obj_new['txt']:            
                    obj_new['mr']['familyFriendly'] = 'no'
                    #obj_new['reason']['familyFriendly'] = keyword_tmp
                    #flag = True
                    #break
                    a_reason.append(keyword_tmp)
                    a_loc.append(obj_new['txt'].find(keyword_tmp))
            #if flag is True:
            #    break
        else:
            if keyword in obj_new['txt']:            
                obj_new['mr']['familyFriendly'] = 'no'
                #obj_new['reason']['familyFriendly'] = keyword
                #flag = True
                #break
                a_reason.append(keyword)
                a_loc.append(obj_new['txt'].find(keyword))
    if (flag is False) and (len(a_reason) > 0):
        obj_new['reason']['familyFriendly'] = a_reason[np.array(a_loc).argmin()]
        flag = True

    if flag is False:
        a_reason = []
        a_loc = []
        for keyword in a_family_yes:
            if '@FAMILY@' in keyword:
                for keyword_family in a_variation_family:
                    keyword_tmp = keyword.replace('@FAMILY@', keyword_family)
                    if keyword_tmp in obj_new['txt']:
                        obj_new['mr']['familyFriendly'] = 'yes'
                        #obj_new['reason']['familyFriendly'] = keyword_tmp
                        #flag = True
                        #break
                        a_reason.append(keyword_tmp)
                        a_loc.append(obj_new['txt'].find(keyword_tmp))
                #if flag is True:
                #    break
            else:
                if keyword in obj_new['txt']:
                    obj_new['mr']['familyFriendly'] = 'yes'
                    #obj_new['reason']['familyFriendly'] = keyword
                    #flag = True
                    #break
                    a_reason.append(keyword)
                    a_loc.append(obj_new['txt'].find(keyword))
        if (flag is False) and (len(a_reason) > 0):
            obj_new['reason']['familyFriendly'] = a_reason[np.array(a_loc).argmin()]
            flag = True

    if verbose_flag is True:
        if (obj_new['mr']['familyFriendly'] == '') and (mr_old['familyFriendly'] != ''):
            print('[NULL:familyFriendly] ('+mr_old['familyFriendly']+')')
            print(obj_new['txt'])

    return obj_new


# obtain MR extension (order/idx_sen/num_sen)
def obtain_extension(obj):
    # order
    txt_lex = obj['txt']
    if obj['mr']['name'] != '':
        txt_lex = txt_lex.replace(obj['mr']['name'], 'NAME')
    if obj['mr']['near'] != '':
        txt_lex = txt_lex.replace(obj['mr']['near'], 'NEAR')

    a_loc = {}
    for attr in obj['reason']:
        if obj['reason'][attr] != '':
            if attr == 'name':
                a_loc[attr] = txt_lex.find('NAME')
            elif attr == 'near':
                a_loc[attr] = txt_lex.find('NEAR')
            else:
                a_loc[attr] = txt_lex.find(obj['reason'][attr])
        else:
            a_loc[attr] = len(txt_lex)+10
    a_tmp = sorted(a_loc.items(), key=lambda x:x[1])
    j = 1
    for i in range(len(a_tmp)):
        attr = a_tmp[i][0]
        if obj['reason'][attr] != '':
            obj['order'][attr] = j
            j += 1

    # idx_sen
    loc_sen = []
    for j in range(len(txt_lex)):
        if (txt_lex[j] == '.') or (txt_lex[j] == '?'):
            loc_sen.append(j)
    idx_sen = {}
    for attr in obj['mr']:
        idx_sen[attr] = 0
        if obj['mr'][attr] != '':
            if (attr == 'name') or (attr == 'near'):
                loc_value = txt_lex.find(attr.upper())
            else:
                loc_value = txt_lex.find(obj['reason'][attr])
            for j in range(len(loc_sen)):
                if loc_value < loc_sen[j]:
                    idx_sen[attr] = j+1
                    break
    obj['idx_sen'] = idx_sen

    # num_sen
    obj['num_sen'] = obj['txt'].count('.') + obj['txt'].count('?')

    return obj


# MR correction
def correct_mr(a_obj_in, value_list, verbose_flag):
    a_obj_out = []

    for obj in a_obj_in:
        mr_old = obj['mr']
        obj_new = {
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
            'reason': {
                'name': '',
                'eatType': '',
                'food': '',
                'priceRange': '',
                'customer rating': '',
                'area': '',
                'familyFriendly': '',
                'near': ''
            },
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
            'txt': obj['txt'],
            'num_sen': 0,
            'id': obj['id'],
            'remarks': obj['remarks']
        }

        # (1)(2) name and near
        obj_new = extract_name_near(obj_new, value_list, verbose_flag, mr_old)

        # (3) eatType (coffee shop, pub, restaurant)
        obj_new = extract_eatType(obj_new, verbose_flag, mr_old)

        # (4) food (chinese, english, fast food, french, indian, italian, japanese)
        obj_new = extract_food(obj_new, value_list, verbose_flag, mr_old)

        # (5) priceRange
        obj_new = extract_priceRange(obj_new, value_list, verbose_flag, mr_old)

        # (6) customer rating (1 out of 5, 3 out of 5, 5 out of 5, average, high, low)
        obj_new = extract_customer_rating(obj_new, value_list, verbose_flag, mr_old)

        # (7) area
        obj_new = extract_area(obj_new, verbose_flag, mr_old)

        # (8) familyFriendly
        obj_new = extract_familyFriendly(obj_new, verbose_flag, mr_old)

        # (9) MR extension
        obj_new = obtain_extension(obj_new)

        # (10) back to original
        for attr in obj_new['mr']:
            obj_new['mr'][attr] = obj_new['mr'][attr].replace('%%%', '\'').replace('$', '£').replace('cafe', 'café')
        obj_new['txt'] = obj_new['txt'].replace('%%%', '\'').replace('$', '£').replace('cafe', 'café')

        obj['new'] = obj_new
        a_obj_out.append(obj)

    return a_obj_out


# capicalisation
def capitalisation(a_obj_in):
    a_country = [
        'American',
        'British',
        'Canadian',
        'Chinese',
        'English',
        'French',
        'Indian',
        'Italian',
        'Japanese',
        'Thai'
    ]

    a_obj_out = []
    for obj in a_obj_in:
        # name and near
        name = obj['new']['mr']['name']
        near = obj['new']['mr']['near']
        obj['new']['mr']['name'] = name.upper()
        obj['new']['mr']['near'] = near.upper()
        obj['new']['txt'] = obj['new']['txt'].replace(name, name.upper())
        obj['new']['txt'] = obj['new']['txt'].replace(near, near.upper())

        # country name
        for country in a_country:
            if (country == 'French') and ('french fries' in obj['new']['txt']):
                continue
            if country.lower() in obj['new']['mr']['food']:
                obj['new']['mr']['food'] = country
            if country.lower() in obj['new']['txt']:
                obj['new']['txt'] = obj['new']['txt'].replace(country.lower(), country)

        # 1st letter
        a_loc = [0]
        flag = False
        for j in range(1, len(obj['new']['txt'])):
            if (obj['new']['txt'][j] == '.') or (obj['new']['txt'][j] == '?'):
                flag = True
            else:
                if flag is True:
                    if obj['new']['txt'][j] != ' ':
                        a_loc.append(j)
                        flag = False

        txt = obj['new']['txt']
        for idx in a_loc:
            txt = txt[:idx] + txt[idx].upper() + txt[idx+1:]

        txt = txt.replace(' i ', ' I ')
        txt = txt.replace(' i\'', ' I\'')

        obj['new']['txt'] = txt
        a_obj_out.append(obj)

    return a_obj_out


# delexicalisation
def delexicalisation(a_obj_in):
    a_obj_out = []
    for obj in a_obj_in:
        obj['new']['mr_lex'] = copy.deepcopy(obj['new']['mr'])
        obj['new']['txt_lex'] = copy.deepcopy(obj['new']['txt'])
        if obj['new']['mr']['name'] != '':
            obj['new']['mr_lex']['name'] = 'NAME'
            obj['new']['txt_lex'] = obj['new']['txt_lex'].replace(obj['new']['mr']['name'], 'NAME')
        if obj['new']['mr']['near'] != '':
            obj['new']['mr_lex']['near'] = 'NEAR'
            obj['new']['txt_lex'] = obj['new']['txt_lex'].replace(obj['new']['mr']['near'], 'NEAR')
        # number of sentence
        obj['new']['num_sen'] = obj['new']['txt_lex'].count('.') + obj['new']['txt_lex'].count('?')
        a_obj_out.append(obj)

    return a_obj_out


# dump file
def dump_json(a_obj_in, fname):
    a_obj_reason = []
    a_obj_out = []
    for obj in a_obj_in:
        a_obj_reason.append({'org': obj['org'], 'new': obj['new']})
        if obj['new']['remarks'] != '':
            continue
        obj_out = {
            'id': obj['new']['id'],
            'mr': {
                'value': obj['new']['mr'],
                'value_lex': obj['new']['mr_lex'],
                'order': obj['new']['order'],
                'idx_sen': obj['new']['idx_sen'],
                'num_sen': obj['new']['num_sen']
            },
            'txt': obj['new']['txt'],
            'txt_lex': obj['new']['txt_lex']
        }
        a_obj_out.append(obj_out)

    with open(fname[:-5]+'_reason.json', 'w', encoding='utf-8') as fo:
        json.dump(a_obj_reason, fo, ensure_ascii=False, indent=4, sort_keys=False)
    with open(fname, 'w', encoding='utf-8') as fo:
        json.dump(a_obj_out, fo, ensure_ascii=False, indent=4, sort_keys=False)

    return


# main
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='input json file')
    parser.add_argument('-iv', help='input MR value file')
    parser.add_argument('-o', help='output json file')
    parser.add_argument('-v', help='verbose debug information', action='store_true')
    args = parser.parse_args()

    print('** correct_mr: E2E MR correction **')
    print(' input            : '+str(args.i))
    print(' input (MR value) : '+str(args.iv))
    print(' output           : '+str(args.o))

    # input json file
    with open(args.i, 'r', encoding='utf-8') as f_in:
        a_obj_in = json.load(f_in)

    # value list
    with open(args.iv, 'r', encoding='utf-8') as f_list:
        value_list = json.load(f_list)

    # manually add name
    value_list['name'].append('ah mama mia')
    value_list['name'].append('st. john\'s college')
    value_list['name'].append('glisson road')
    value_list['name'].append('chesterton road')
    value_list['name'].append('the red pointer')

    # analyse
    a_obj_out = correct_mr(a_obj_in, value_list, args.v)

    # capitalise
    a_obj_out = capitalisation(a_obj_out)

    # delexicalise
    a_obj_out = delexicalisation(a_obj_out)

    # output json file
    dump_json(a_obj_out, args.o)

    print('** done **')

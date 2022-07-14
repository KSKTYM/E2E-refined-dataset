#! python

import json
import copy
import argparse

# (1) extend object
def extend_obj(a_obj_in):
    a_obj_out = []
    for obj_in in a_obj_in:
        obj_out = {
            'org': {
                'mr': obj_in['mr'],
                'txt': obj_in['txt']
            },
            'mr': copy.deepcopy(obj_in['mr']),
            'txt': copy.deepcopy(obj_in['txt']),
            'remarks': '',
            'id': obj_in['id']
        }
        a_obj_out.append(obj_out)

    return a_obj_out

## (2) remove weird sentence
def remove_sentences(a_obj):
    a_remove_sentences = [
        'Café',
        'A cheap hotel near Cambridge is Fitzbillies, part of the chain called Express by Holiday Inn.  This hotel was rated 5 out of 5.',
        'Fast food kid friendly 1 out of 5 Burger King riverside the coffee shop The Eagle moderate',
        'the coffee shop The Eagle moderate Fast food kid friendly 1 out of 5 Burger King riverside',
        'There is a Yippee Noodle Bar with high customer ratings called Strada. It serves Italian food and is a pub',
        'Loch Fyne has fast food on the riverside with a rating of 1 out of 5 for the restaurant The Rice Boat',
        'Burger King is a Fast food restaurant with menus ranging around £20-25 near the city centre. It has a high customer rating with a coffee shop named The Eagle, but no, it is not kid friendly.',
        'The Cotto ranges between twenty and twenty-five dollars with a high customer rating. The Portland Arms serves Italian food near the riverside.',
        'The Portland Arms serves Italian food near the riverside. The Cotto ranges between twenty and twenty-five dollars with a high customer rating.',
        'The Rice Boat at riverside provides French food Loch Fyne which has a customer Rating of 1 out of 5.',
        'Clare Hall is known for Fast food and coffee shop style bakeries although, customers only rate them average the Clowns are quite amusing.',
        'Burger King is near the coffee shop Blue Spice which has an average customer rating.',
        '\"Near Clare Hall area, price range 23, Bibimbap House, McDonalds.\"',
        '\"Near Clare Hall area, price range 24, Bibimbap House, Wendy\'s.\"'
    ]
    for obj in a_obj:
        for sentence in a_remove_sentences:
            if obj['org']['txt'] == sentence:
                obj['remarks'] = 'weird sentence'
                #obj['txt'] = ''
                #print(str(obj['id'])+': '+str(sentence))
                break
    return a_obj

## (3) error correction
def correct_error(a_obj_in, verbose_flag):
    a_obj_out = []

    for i, obj in enumerate(a_obj_in):
        if verbose_flag is True:
            print('['+str(i)+']')
            print(obj['txt'])

        # (A) normalisation
        for attr in obj['mr']:
            data = obj['mr'][attr]
            obj['mr'][attr] = filter_normalise(obj['mr'][attr], False, verbose_flag)
            # check
            if (verbose_flag is True) and \
               (data.lower().replace('£', '$').replace('café', 'cafe') != obj['mr'][attr]):
                print('ATTRIBUTE: '+attr)
                print(data)
                print(obj['mr'][attr])
        obj['txt'] = filter_normalise(obj['txt'], True, verbose_flag)

        # (B) typo correction
        obj = filter_typo(obj, verbose_flag)

        # (C) quotation error
        obj = filter_quotation(obj, verbose_flag)

        # (D) remove overlapping region
        obj = filter_overlap(obj, verbose_flag)

        # (E) for hand processing on excel (back to original by m_correct_mr.py later)
        if ('\"') in obj['txt']:
            for attr in obj['mr']:
                obj['mr'][attr] = obj['mr'][attr].replace('\"', '%%%')
            obj['txt'] = obj['txt'].replace('\"', '%%%')

        # check quotation error
        if (verbose_flag is True) and \
           ((obj['txt'].count('%%%') % 2) != 0):
            print('[QUOTATION error]')
            print(obj['txt'])

        if verbose_flag is True:
            print(obj['txt'])

        a_obj_out.append(obj)

    return a_obj_out

## (5-A) txt normalisation
def dump_proc(name, value_old, value_new, verbose_flag):
    if (verbose_flag is True) and (value_old != value_new):
        print(name)
        print(value_new)

def filter_normalise(txt, txt_flag, verbose_flag):
    if txt == '':
        return txt

    # lower
    txt = txt.lower()

    ## for Excel
    # café -> cafe
    txt = txt.replace('café', 'cafe')

    # dollar/euro -> pound
    txt = txt.replace('european dollars', 'pounds')
    txt = txt.replace('european dollar', 'pound')
    txt = txt.replace('british pound', 'pound')
    txt = txt.replace('dollar', 'pound')
    if ('euro' in txt) and (('europe' in txt) is False):
        txt = txt.replace('euro', 'pound')

    # £ -> $
    txt = txt.replace('l20', '£20')
    txt = txt.replace('l 20', '£20')
    txt = txt.replace('e20', '£20')
    txt = txt.replace('20 £', '£20')
    txt = txt.replace('20£', '£20')
    txt = txt.replace('£20 pounds', '£20')
    txt = txt.replace('20 pounds', '£20')
    txt = txt.replace('20 pound', '£20')
    txt = txt.replace('20gbp', '£20')
    txt = txt.replace('20lb', '£20')
    txt = txt.replace('20l', '£20')
    txt = txt.replace('20s', '£20')
    txt = txt.replace('20 gbp', '£20')
    txt = txt.replace('20 quid', '£20')
    txt = txt.replace('20-25lb', '£20-25')
    txt = txt.replace('20-25l', '£20-25')
    txt = txt.replace('20-25pounds', '£20-25')
    txt = txt.replace('20-25 pounds', '£20-25')
    txt = txt.replace('20 and £25', '£20-25')
    txt = txt.replace('20 and 25 pounds', '£20-25')
    txt = txt.replace('20 to 25 £', '£20-25')
    txt = txt.replace('20 to 25 pounds', '£20-25')
    txt = txt.replace('20 - 25 pounds', '£20-25')
    txt = txt.replace('20 and 25 pound', '£20-25')
    txt = txt.replace('20 to 25 pound', '£20-25')
    txt = txt.replace('20 - 25 pound', '£20-25')
    txt = txt.replace('20- 25lb', '£20-25')
    txt = txt.replace('20- 25l', '£20-25')
    txt = txt.replace('20-25 gbp', '£20-25')
    txt = txt.replace('20£-25', '£20-25')
    txt = txt.replace('25£', '£25')
    txt = txt.replace('l25', '£25')
    txt = txt.replace('e25', '£25')
    txt = txt.replace('l30', '£30')
    txt = txt.replace('e30', '£30')
    txt = txt.replace('f30', '£30')
    txt = txt.replace('30.£', '£30')
    txt = txt.replace('30£', '£30')
    txt = txt.replace('30 £', '£30')
    txt = txt.replace('30lbs', '£30')
    txt = txt.replace('30 lbs', '£30')
    txt = txt.replace('30lb', '£30')
    txt = txt.replace('30l', '£30')
    txt = txt.replace('30pounds', '£30')
    txt = txt.replace('30pound', '£30')
    txt = txt.replace('30 pounds', '£30')
    txt = txt.replace('30 pound', '£30')
    txt = txt.replace('30gbp', '£30')
    txt = txt.replace('30 gbp', '£30')
    txt = txt.replace('30 quid', '£30')
    txt = txt.replace('£30 +', '£30')
    txt = txt.replace('£', '$')
    txt = txt.replace('$$', '$')

    # British English
    txt = txt.replace('center', 'centre')
    txt = txt.replace('english sterling', 'british sterling')
    txt = txt.replace('favor', 'favour')
    txt = txt.replace('flavor', 'flavour')
    txt = txt.replace('neighbor', 'neighbour')
    txt = txt.replace('specializ', 'specialis')
    txt = txt.replace('traveling', 'travelling')
    txt = txt.replace('organiz', 'organis')
    txt = txt.replace('socialize', 'socialise')

    '''
    # American/Canadian -> English
    txt = txt.replace(' usa', ' uk')
    txt = txt.replace('american', 'english')
    txt = txt.replace('canadian', 'english')
    '''

    # normalise0 (".....")
    if txt[0] == '\"' and txt[-1] == '\"':
        txt_old = txt
        txt = txt[1:-1]
        dump_proc('(norm00)', txt_old, txt, verbose_flag)

    # normalise1 ('  ')
    if '  ' in txt:
        txt_old = txt
        while ('  ' in txt):
            txt = txt.replace('  ', ' ')
        dump_proc('(norm01)', txt_old, txt, verbose_flag)

    # normalise2 ("")
    if '\"\"' in txt:
        txt_old = txt
        txt = txt.replace('\"\"', '\'')
        dump_proc('(norm02)', txt_old, txt, verbose_flag)

    # normalise3 (,,)
    if ',,' in txt:
        txt_old = txt
        txt = txt.replace(',,', ',')
        dump_proc('(norm03)', txt_old, txt, verbose_flag)

    # normalise4 (...)
    if '...' in txt:
        txt_old = txt
        txt = txt.replace('...', '.')
        dump_proc('(norm04)', txt_old, txt, verbose_flag)

    # normalise5 (..)
    while ('..' in txt):
        txt_old = txt
        txt = txt.replace('..', '.')
        dump_proc('(norm05)', txt_old, txt, verbose_flag)

    # normalise6 (.,)
    if '.,' in txt:
        txt_old = txt
        if txt.endswith('.,'):
            txt = txt.replace('.,', '.')
        else:
            txt = txt.replace('.,', ',')
        dump_proc('(norm06)', txt_old, txt, verbose_flag)

    # normalise7 (,.)
    if ',.' in txt:
        txt_old = txt
        if txt.endswith(',.'):
            txt = txt.replace(',.', '.')
        else:
            txt = txt.replace(',.', ',')
        dump_proc('(norm07)', txt_old, txt, verbose_flag)

    # normalise8 (. .)
    while ('. .' in txt):
        txt_old = txt
        txt = txt.replace('. .', '.')
        dump_proc('(norm08)', txt_old, txt, verbose_flag)

    # normalise9 (, .)
    if ', .' in txt:
        txt_old = txt
        if txt.endswith(', .'):
            txt = txt.replace(', .', '.')
        else:
            txt = txt.replace(', .', ',')
        dump_proc('(norm09)', txt_old, txt, verbose_flag)

    # normalise10 (. ,)
    if '. ,' in txt:
        txt_old = txt
        if txt.endswith('. ,'):
            txt = txt.replace('. ,', '.')
        else:
            txt = txt.replace('. ,', ',')
        dump_proc('(norm10)', txt_old, txt, verbose_flag)

    # normalise11 ( .)(should be check by eyes)
    if ' .' in txt:
        txt_old = txt
        txt = txt.replace(' .', '.')
        dump_proc('(norm11)', txt_old, txt, verbose_flag)

    # normalise12 ( ,)
    if ' ,' in txt:
        txt_old = txt
        txt = txt.replace(' ,', ',')
        dump_proc('(norm12)', txt_old, txt, verbose_flag)

    # normalise13 (.')
    if '.\'' in txt:
        txt_old = txt
        txt = txt.replace('.\'', '\'.')
        dump_proc('(norm13)', txt_old, txt, verbose_flag)

    # normalise14 (add space right after period(.))
    if '.' in txt:
        txt_old = txt
        for i in range(len(txt)-1):
            if (txt[i] == '.') and \
               (txt[i+1] != ' ') and \
               (txt[i+1] != '0') and \
               (txt[i+1] != '1') and \
               (txt[i+1] != '2') and \
               (txt[i+1] != '3') and \
               (txt[i+1] != '4') and \
               (txt[i+1] != '5') and \
               (txt[i+1] != '6') and \
               (txt[i+1] != '7') and \
               (txt[i+1] != '8') and \
               (txt[i+1] != '9') and \
               (txt[i+1] != '$'):
                txt = txt[:i+1] + ' ' + txt[i+1:]
        dump_proc('(norm14)', txt_old, txt, verbose_flag)

    # normalise15 (add space right after comma(,))
    if ',' in txt:
        txt_old = txt
        for i in range(len(txt)-1):
            if (txt[i] == ',') and (txt[i+1] != ' '):
                txt = txt[:i+1] + ' ' + txt[i+1:]
        dump_proc('(norm15)', txt_old, txt, verbose_flag)

    # normalise16 (t' s -> t's)
    if 't\' s' in txt:
        txt_old = txt
        txt = txt.replace('t\' s', 't\'s')
        dump_proc('(norm16)', txt_old, txt, verbose_flag)

    # normalise16-2 (. 's -> 's)
    if '. \'s' in txt:
        txt_old = txt
        txt = txt.replace('. \'s', '\'s')
        dump_proc('(norm16-2)', txt_old, txt, verbose_flag)                

    # normalise17 (its' -> its)
    if 'its\'' in txt:
        txt_old = txt
        txt = txt.replace('its\'', 'its')
        dump_proc('(norm17)', txt_old, txt, verbose_flag)

    # normalise18 (remove space at begining/end of txt)
    if txt.startswith(' ') or txt.endswith(' '):
        txt_old = txt
        txt = txt.rstrip(' ').lstrip(' ')
        dump_proc('(norm18)', txt_old, txt, verbose_flag)

    # normalise19 (apostrophe)
    txt_old = txt
    a_loc = []
    for i in range(len(txt)):
        if txt[i] == '\'':
            flag = True
            if (i < len(txt) - 2) and \
               (txt[i+2] == ' ') and \
               ((txt[i+1] == 's') or (txt[i+1] == 'd')):
                # it's
                # I'd
                flag = False
            if (i < len(txt) - 2) and \
               (txt[i+1] == 's') and \
               ((txt[i+2] == '.') or (txt[i+2] == ',') or (txt[i+2] == ';') or (txt[i+2] == ':') or (txt[i+2] == '?')):
                # hoge's.
                flag = False
            if (i == len(txt) - 2) and \
               (txt[i+1] == 's'):
                # hoge's
                flag = False
            if (i > 0) and (i < len(txt) - 2) and \
               (txt[i+2] == ' ') and \
               (((txt[i-1] == 'n') and (txt[i+1] == 't')) or \
                ((txt[i-1] == 'i') and (txt[i+1] == 'm'))):
                # isn't
                # I'm
                flag = False
            if (i > 1) and (i < len(txt) - 1) and \
               (txt[i-2] == ' ') and \
               (txt[i-1] == 'd') and (txt[i+1] == 'o'):
                # d'oeuvre
                flag = False
            if i < len(txt) - 3:
                if (txt[i+3] == ' ') and \
                   (((txt[i+1] == 'l') and (txt[i+2] == 'l')) or \
                    ((txt[i+1] == 'r') and (txt[i+2] == 'e')) or \
                    ((txt[i+1] == 'v') and (txt[i+2] == 'e'))):
                    # you'll
                    # you're
                    # you've
                    flag = False
            if flag is True:
                txt = txt[:i] + '"' + txt[i+1:]
    dump_proc('(norm19)', txt_old, txt, verbose_flag)

    # normalise20 (hyphen)
    if txt_flag is True:
        txt_old = txt
        len_txt = len(txt)
        for i in range(len_txt):
            if txt[i:i+2] == ' -':
                loc = i
                if (loc+len(' -') < len(txt)) and (txt[loc+len(' -')] != ' ') and (txt[loc+len(' -')] != '-'):
                    txt = txt[:loc+len(' -')] + ' ' + txt[loc+len(' -'):]

        for i in range(len_txt):
            if txt[i:i+2] == '- ':
                loc = i
                if (loc > 0) and (txt[loc-1] != ' ') and (txt[loc-1] != '-'):
                    txt = txt[:loc] + ' ' + txt[loc:]

        if ' -- ' in txt:
            txt = txt.replace(' -- ', ' - ')
        if '--' in txt:
            txt = txt.replace('--', ' ')
        dump_proc('(norm20)', txt_old, txt, verbose_flag)

    # normalise21 (hyphen)
    a_front = ['non', 'over', 'adult', 'fast', 'take']
    a_back = ['$', '£', 'friendly', 'price', 'rated', 'star']
    a_number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    if txt_flag is True:
        if ' - ' in txt:
            # front
            for word in a_front:
                if word+' - ' in txt:
                    txt_old = txt
                    loc = txt.find(word+' - ')
                    txt = txt[:loc+len(word)]+'-'+txt[loc+len(word+' - '):]
                    dump_proc('(norm21-1)', txt_old, txt, verbose_flag)

            # back
            for word in a_back:
                if ' - '+word in txt:
                    txt_old = txt
                    loc = txt.find(' - '+word)
                    txt = txt[:loc]+'-'+txt[loc+len(' - '):]
                    dump_proc('(norm21-2)', txt_old, txt, verbose_flag)

            # number
            for numA in a_number:
                for numB in a_number:
                    if numA+' - '+numB in txt:
                        txt_old = txt
                        loc = txt.find(numA+' - '+numB)
                        txt = txt[:loc+len(numA)]+'-'+txt[loc+len(numA+' - '):]
                        dump_proc('(norm21-3)', txt_old, txt, verbose_flag)

        for num in a_number:
            if '$ '+num in txt:
                txt_old = txt
                txt = txt.replace('$ '+num, '$'+num)
                dump_proc('(norm21-4)', txt_old, txt, verbose_flag)

    # normalise22 (add space between than and $)
    if 'than$' in txt:
        txt_old = txt
        txt = txt.replace('than$', 'than $')
        dump_proc('(norm22)', txt_old, txt, verbose_flag)

    # normalise23 (txt should not end with comma)
    if txt_flag is True:
        if txt.endswith(','):
            txt_old = txt
            txt = txt[:len(txt)-1]+'.'
            dump_proc('(norm23)', txt_old, txt, verbose_flag)

    # normalise24 (add period at end of txt)
    if txt_flag is True:
        if (txt.endswith('?') is False) and (txt.endswith('.') is False):
            txt_old = txt
            txt += '.'
            dump_proc('(norm24)', txt_old, txt, verbose_flag)

    # normalise25 change values
    a_word_norm25_A = ['$ 20-25', '$-25', '$20-$30', '$20-$25', '$20.00-$25.00', '$20.00 $25.00', '$20-15', '$20-2', '$20-26', '$20-30$', '$20-50', '$25-25', '20$-30$', '20-$25', '20-25$', '20-25 $', '20-50']
    a_word_norm25_B = [' out of', ' rating', ' star']
    a_word_norm25_C = ['out of ', 'rated at ', 'rating of ']
    a_word_norm25_D = ['9 on a scale of 1-10', '9 to 10 stars']
    if txt_flag is True:
        for word in a_word_norm25_A:
            a_post = [' ', '.', ',']
            for post in a_post:
                if word + post in txt:
                    txt_old = txt
                    txt = txt.replace(word + post, '$20-25'+post)
                    dump_proc('(norm25)', txt_old, txt, verbose_flag)
        for word in a_word_norm25_B:
            if '4' + word in txt:
                txt_old = txt
                txt = txt.replace('4' + word, '5' + word)
                dump_proc('(norm25)', txt_old, txt, verbose_flag)
        for word in a_word_norm25_C:
            if word + '4' in txt:
                txt_old = txt
                txt = txt.replace(word + '4',  word + '5')
                dump_proc('(norm25)', txt_old, txt, verbose_flag)
        for word in a_word_norm25_D:
            if word in txt:
                txt_old = txt
                txt = txt.replace(word,  '5 out of 5')
                dump_proc('(norm25)', txt_old, txt, verbose_flag)
        if 'rating of out of 5' in txt:
            txt_old = txt
            txt = txt.replace('rating of out of 5', 'rating of 5 out of 5')
            dump_proc('(norm25)', txt_old, txt, verbose_flag)
        if '$8' in txt:
            txt_old = txt
            txt = txt.replace('$8', '$20')
            dump_proc('(norm25)', txt_old, txt, verbose_flag)
        if '$9.50' in txt:
            txt_old = txt
            txt = txt.replace('$9.50', '$20')
            dump_proc('(norm25)', txt_old, txt, verbose_flag)
        if '$9.5' in txt:
            txt_old = txt
            txt = txt.replace('$9.5', '$20')
            dump_proc('(norm25)', txt_old, txt, verbose_flag)
        if '$10' in txt:
            txt_old = txt
            txt = txt.replace('$10', '$20')
            dump_proc('(norm25)', txt_old, txt, verbose_flag)
        if '$19.99' in txt:
            txt_old = txt
            txt = txt.replace('$19.99', '$20')
            dump_proc('(norm25)', txt_old, txt, verbose_flag)
        if '$20.50' in txt:
            txt_old = txt
            txt = txt.replace('$20.50', '$20')
            dump_proc('(norm25)', txt_old, txt, verbose_flag)
        if '$22' in txt:
            txt_old = txt
            txt = txt.replace('$22', '$20')
            dump_proc('(norm25)', txt_old, txt, verbose_flag)
        if '$24' in txt:
            txt_old = txt
            txt = txt.replace('$24', '$20')
            dump_proc('(norm25)', txt_old, txt, verbose_flag)
        if '$25.00' in txt:
            txt_old = txt
            txt = txt.replace('$25.00', '$25')
            dump_proc('(norm25)', txt_old, txt, verbose_flag)
        if '$30.00' in txt:
            txt_old = txt
            txt = txt.replace('$30.00', '$30')
            dump_proc('(norm25)', txt_old, txt, verbose_flag)
        if '$30.99' in txt:
            txt_old = txt
            txt = txt.replace('$30.99', '$30')
            dump_proc('(norm25)', txt_old, txt, verbose_flag)
        if '$32' in txt:
            txt_old = txt
            txt = txt.replace('$32', '$30')
            dump_proc('(norm25)', txt_old, txt, verbose_flag)
        if '$35' in txt:
            txt_old = txt
            txt = txt.replace('$35', '$30')
            dump_proc('(norm25)', txt_old, txt, verbose_flag)
        if '$20.00' in txt:
            txt_old = txt
            txt = txt.replace('$20.00', '$20')
            dump_proc('(norm25)', txt_old, txt, verbose_flag)
        if '20.00' in txt:
            txt_old = txt
            txt = txt.replace('20.00', '$20')
            dump_proc('(norm25)', txt_old, txt, verbose_flag)
        if '3.5' in txt:
            txt_old = txt
            txt = txt.replace('3.5', '3')
            dump_proc('(norm25)', txt_old, txt, verbose_flag)
        if '4.5' in txt:
            txt_old = txt
            txt = txt.replace('4.5', '5')
            dump_proc('(norm25)', txt_old, txt, verbose_flag)
        if '3.33' in txt:
            txt_old = txt
            txt = txt.replace('3.33', '3')
            dump_proc('(norm25)', txt_old, txt, verbose_flag)
        if 'more than 40' in txt:
            txt_old = txt
            txt = txt.replace('more than 40', 'more than 30')
            dump_proc('(norm25)', txt_old, txt, verbose_flag)
        if 'above $25' in txt:
            txt_old = txt
            txt = txt.replace('above $25', 'above $30')
            dump_proc('(norm25)', txt_old, txt, verbose_flag)
        if 'below ten' in txt:
            txt_old = txt
            txt = txt.replace('below ten', 'below $20')
            dump_proc('(norm25)', txt_old, txt, verbose_flag)
        if '1-2 stars' in txt:
            txt_old = txt
            txt = txt.replace('1-2 stars', '1 star')
            dump_proc('(norm25)', txt_old, txt, verbose_flag)
        if '6 stars' in txt:
            txt_old = txt
            txt = txt.replace('6 stars', '5 stars')
            dump_proc('(norm25)', txt_old, txt, verbose_flag)
        if 'price range is $20.' in txt:
            txt_old = txt
            txt = txt.replace('$20.', '$20-25.')
            dump_proc('(norm25)', txt_old, txt, verbose_flag)
        if 'price range of $20,' in txt:
            txt_old = txt
            txt = txt.replace('$20,', '$20-25,')
            dump_proc('(norm25)', txt_old, txt, verbose_flag)

    # normalise26 insert lacked value
    if txt_flag is True:
        if 'has a price range in' in txt:
            txt_old = txt
            txt = txt.replace('has a price range', 'has a moderate price range')
            dump_proc('(norm26)', txt_old, txt, verbose_flag)
        if 'is friendly' in txt:
            txt_old = txt
            txt = txt.replace('is friendly', 'is family friendly')
            dump_proc('(norm26)', txt_old, txt, verbose_flag)

    # normalise27 reduce double value
    if txt_flag is True:
        if 'cheap and reasonable' in txt:
            txt_old = txt
            txt = txt.replace('cheap and reasonable', 'reasonable')
            dump_proc('(norm27)', txt_old, txt, verbose_flag)
        if 'moderately cheap' in txt:
            txt_old = txt
            txt = txt.replace('moderately cheap', 'cheap')
            dump_proc('(norm27)', txt_old, txt, verbose_flag)
        if 'japanese fast food' in txt:
            txt_old = txt
            txt = txt.replace('japanese fast food', 'fast food')
            dump_proc('(norm27)', txt_old, txt, verbose_flag)

    # normlise28 no space right before ":"/";"
    if txt_flag is True:
        if ' :' in txt:
            txt_old = txt
            txt = txt.replace(' :', ':')
            dump_proc('(norm28)', txt_old, txt, verbose_flag)
        if ' ;' in txt:
            txt_old = txt
            txt = txt.replace(' ;', ';')
            dump_proc('(norm28)', txt_old, txt, verbose_flag)

    return txt

## (5-B) typo
def filter_typo(obj, verbose_flag):
    ## named entities
    # e-1) correct: Crowne Plaza Hotel, wrong: Crown Plaza Hotel
    # e-2) correct: Wrestlers, wrong: Wrestlerss [wrestlers, the eagle, the mill, travellers rest beefeater, zizzi, giraffe, the waterman, aromi, loch fyne, the punter, the cricketers]
    # e-3) correct: cotto, wrong: cotton
    # e-4) correct: fitzbillies, wrong: fitzbilies
    # e-5) correct: golden curry, wrong: golden city
    # e-6) correct: raja indian cuisine, wrong: raja cuisine
    # e-7) correct: cafe brazil, wrong: cafe brazilian
    # e-8) correct: yippee noodle bar, wrong: yippee noddle bart
    # e-9) correct: cafe sicilia, wrong: cafe sicilian
    # e-10) correct: st. john's college, wrong: st john's college
    # e-11) correct: raja indian cuisine, wrong: raja
    # e-12) correct: golden palace., wrong: golden palace. n.

    ## numbers
    # n-1) correct: 1 out of 5, wrong: ['1 of of 5', '1 out 5', '1out of 5', '1 our of 5', '1out5', '1-out of 5]
    # n-2) correct: ['5 the', '5 and', '5 star', '5 located', '5 customer'] , wrong: ['5the', '5and', '5star', '5located', '5customer']
    # n-3) correct: than ['1', '2', ..., '0', '$'] , wrong: then
    # n-4) correct: 30 and, wrong: 30and
    # n-5) correct: $30 and, wrong: $and
    # n-6) correct: $30, wrong: ['$3o', '$0']
    # n-7) correct: of 5, wrong: or5
    # n-8) correct: ., wrong: .6.
    # n-9) correct: rating 3, wrong: rating3
    # n-10) correct: a 1, wrong: a1
    # n-11) correct: ['1', '3', '5', 'one', 'three', 'five'] star, wrong: ['1', '3', '5', 'one', 'three', 'five'] start
    # n-12) correct: 5 stars, wrong: 5 tars
    # n-13) correct: more than 30, wrong: more than french 30
    # n-14) correct: less than 20, wrong: ['less than french 20', 'less 20']
    # n-15) correct: price is less than $20, wrong: price is than $20
    # n-16) correct: less than $20, wrong: ['less $20', 'less the $20']
    # n-17) correct: for less than $20., wrong: for less.
    # n-18) correct: rating it as ['1', '3', '5'], wrong: rating it a ['1', '3', '5']
    # n-19) correct: 3 out of 5 rated, wrong: 2 out of 3 price rated
    # n-20) correct: to 5, wrong: to5

    ## indefinite articles
    # i-1) correct: an {a|e|i|o|u}, wrong: a {a|e|i|o|u}
    # i-2) correct: a {b|c|d|f|g|h|j|k|l|m|n|p|q|r|s|t|u|v|w|x|y|z}, wrong: an {b|c|d|f|g|h|j|k|l|m|n|p|q|r|s|t|u|v|w|x|y|z}

    ## typos
    # t-a1) correct: a, wrong: s
    # t-a2) correct: an, wrong: am
    # t-a3) correct: an average, wrong: ad averate
    # t-a4) correct: and, wrong: ['ad', 'ans']
    # t-a5) correct: and are not, wrong: and re not
    # t-a6) correct: and has, wrong: a has
    # t-a7) correct: and is not, wrong: an dis not
    # t-a8) correct: areas, wrong: ares
    # t-a9) correct: at, wrong: y (?)
    # t-a10) correct: at a, wrong: a t a
    # t-a11) correct: ', and', wrong: '. and'
    # t-a12) correct: a non-children, wrong: anon-children
    # t-a13) correct: are, wrong: . are

    # t-b1) correct: be, wrong: e
    # t-b2) correct: begin, wrong: ['of begin', 'for begin', 'as well as not begin']
    # t-b3) correct: beside, wrong: besides from

    # t-c1) correct: can't, wrong: cant
    # t-c2) correct: care, wrong: carer
    # t-c3) correct: centre ['of', 'city'], wrong: centre. ['of', 'city']
    # t-c4) correct: cheap, wrong: cheep
    # t-c5) correct: chinese, wrong; chines
    # t-c6) correct: city, wrong: city city
    # t-c7) correct: city centre, wrong: ['cit', 'cite'] centre
    # t-c8) correct: clientele, wrong: clentele
    # t-c9) correct: close by, wrong: close by is
    # t-c10) correct: close to, wrong: close ['of', 'ti']
    # t-c11) correct: coffee house, wrong: coffeehouse
    # t-c12) correct: coffee shop, wrong: ['coffee ship', 'coffee shot', 'coffee shoo', 'coffee chop', 'coffee show']
    # t-c13) correct: customer, wrong: costumer
    # t-c14) correct: ['city', 'city centre'] near, wrong: ['city', 'city centre'] after
    # t-c15) correct: ['customer\'s', 'restaurant\'s', 'shop\'s'], wrong: ['customers\'', 'restaurants\'', 'shops\''] 
    # t-c16) correct: customer rating is low, wrong: customer rating is cheap
    # t-c17) correct: customer rating it as , wrong: customer rating it a
    # t-c18) correct: chinese, wrong: steve's chinese

    # t-d1) correct: dessert, wrong: desert

    # t-e1) correct: eat, wrong: eat t
    # t-e2) correct: entree, wrong: en tree
    # t-e3) txt starts with 'es '
    # t-e4) correct: even though, wrong: eve though

    # t-f1) correct: food, wrong: rood
    # t-f2) correct: for, wrong: foe
    # t-f3) correct: for more, wrong: fore more
    # t-f4) correct: ['for', 'with'] its, wrong ['for', 'with'] it's
    # t-f5) correct: ['for $', 'is $', 'the $', 'of $', 'over $'], wrong: ['for$', 'is$', 'the$', 'of$', 'over$']
    # t-f6) correct: friendly, wrong: friend;y
    # t-f7) correct: fast food, wrong: fast found 

    # t-g1) correct: great, wrong: grate

    # t-h1) correct: hamburgers, wrong: hamgurgers
    # t-h2) correct: has, wrong: ha
    # t-h3) correct: has, wrong: '\'s has'
    # t-h4) correct: high, wrong: ['hugh, 'hight, hi']

    # t-i1) correct: in, wrong: n
    # t-i2) correct: in a, wrong: ina
    # t-i3) correct: indian, wrong: ['india', 'indiana']
    # t-i4) correct: in the, wrong: ['int he', 'in t he']
    # t-i5) correct: in the, wrong: n the
    # t-i6) correct: is, wrong: ['is is', 'has is', 'id']
    # t-i7) correct: it, wrong: ['ot', 'i t']
    # t-i8) correct: it is next to, wrong: next to it is
    # t-i9) correct: it is, wrong: ['ia', 'it s']
    # t-i10) correct: it offers, wrong: t offers
    # t-i11) correct: its, wrong: thats
    # t-i12) correct: its neighbour, wrong: it's neighbour
    # t-i13) correct: it\'s, wrong: it\"
    # t-i14) correct: it's ['not', 'located'], wrong: its ['not', 'located']

    # t-k1) correct: kids, wrong: kid's
    # t-k2) correct: kid friendly, wrong: kind friendly

    # t-l1) correct: less, wrong: ['lees', 'lest']
    # t-l2) correct: let's go, wrong: lets go
    # t-l3) correct: located at, wrong: located ['after', 'we']
    # t-l4) correct: located in, wrong: locate din
    # t-l5) correct: located near, wrong: located new
    # t-l6) correct: lower than, wrong: lover that
    # t-l7) correct: low, wrong: ['lo', 'ow']
    # t-l8) correct: ['less', 'more', 'lower'] than, wrong: ['less', 'more', 'lower'] that
    # t-l9) correct: ['located', 'river'] beside, wrong: ['located', 'river'] besides
    # t-l10) correct: lower than $20, wrong: lower $20

    # t-m1) correct: moderate, wrong: moder
    # t-m2) correct: more than, wrong: more then
    # t-m3) correct: more, wrong: ['moire', 'ore']

    # t-n1) correct: near, wrong: ['neat', 'rear', 'nears', 'bear', 'ear', 'near it is']
    # t-n2) correct: near the, wrong: near ['de', 'he']
    # t-n3) correct: near to, wrong: near yo
    # t-n4) correct: nestled, wrong: nested
    # t-n5) correct: next to, wrong: next
    # t-n6) correct: not, wrong: ['mot', 'no t', 't not']

    # t-o1) correct: of, wrong: ['0f', 'fro', 'o']
    # t-o2) correct: on, wrong: don
    # t-o3) correct: out of, wrong: out ff
    # t-o4) correct: one, wrong: one-one

    # t-p1) correct: place, wrong: lace
    # t-p2) correct: place to, wrong: play to
    # t-p3) correct: pounds, wrong: ponds
    # t-p4) correct: price, wrong: ['prize, 'prance', 'prince']
    # t-p5) correct: priced, wrong: pried
    # t-p6) correct: price range, wrong: price ['rant', 'ranch', 'rand', 'rang']
    # t-p7) correct: pub, wrong: ['pug, 'pump', 'pun', 'pup']
    # t-p8) correct: ['pub', 'restaurant'], wrong: ['pubpe', 'restaurantpe']
    # t-p9) correct: pub,, wrong: pup,

    # t-r1) correct: range, wrong: ['rage', 'rang', 'ranger', 'rant']
    # t-r2) correct: range., wrong: ran.
    # t-r3) correct: rating, wrong: ['raring', 'ratting', 'ranting']
    # t-r4) correct: rating of, wrong: ['rating g of
    # t-r5) correct: ratings are, wrong: ratings is
    # t-r6) correct: restaurant, wrong: restaurantr
    # t-r7) correct: restaurant and, wrong: restaurant and restaurant
    # t-r8) correct: restaurant near, wrong: restaurant ['need', 'hear']
    # t-r9) correct: right off, wrong: right off of
    # t-r10) correct: river, wrong: rive
    # t-r11) correct: road, wrong: rd
    # t-r12) correct: rating., wrong: rating and.
    # t-r13) correct: rating of, wrong: rating f
    # t-r14) correct: restaurant, wrong: restaurant l
    # t-r15) correct: range., wrong: rant.
    # t-r16) correct: river., wrong: rive.
    # t-r17) correct: price range, wrong: price rage

    # t-s1) correct: selection of English, wrong: selection of of English
    # t-s2) correct: served, wrong: sered
    # t-s3) correct: serves, wrong: ['servers', 'server', 'seven']
    # t-s4) correct: steak, wrong: stake
    # t-s5) correct: switched, wrong: swhiched
    # t-s6) correct: sushi, wrong: sushigh

    # t-t1) correct: take, wrong: tale
    # t-t2) correct: tapas, wrong: tapa
    # t-t3) correct: than $20, wrong: then$20
    # t-t4) correct: that, wrong: hat
    # t-t5) correct: that, wrong: tat
    # t-t6) correct: the, wrong: ['the the', 'thew', 'th']
    # t-t7) correct: the fast, wrong: th fast
    # t-t8) correct: there's a, wrong: theres a
    # t-t9) correct: there is, wrong: theres is
    # t-t10) correct: though, wrong: thought
    # t-t11) correct: to rest, wrong: to est
    # t-t12) correct: too expensive, wrong: to expensive

    # t-w1) correct: where, wrong: whee
    # t-w2) correct: which, wrong: ['witch', 'winch']
    # t-w3) correct: wine, wrong: whine
    # t-w4) correct: with a, wrong: wit a
    # t-w5) correct: won't, wrong: wont
    # t-w6) correct: with, wrong: ['whit', 'wit h', 'when th']

    # t-y1) correct: yippee, wrong: yippe

    a_word_e2 = ['aromi', 'giraffe', 'loch fyne', 'the cricketers', 'the eagle', 'the mill', 'the punter', 'the waterman', 'travellers rest beefeater', 'wrestlers', 'zizzi']
    a_word_e4 = ['fitzbilies', 'fitzbilles']
    a_word_n1 = ['1', '3', '5', 'five', 'one', 'three']
    a_word_n2 = ['5and', '5customer', '5located', '5star', '5the']
    a_word_n3 = ['$', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    a_word_n6 = ['$0', '$3o']
    #a_word_n11 = ['1', '3', '5', 'five', 'one', 'three']
    a_word_n11 = a_word_n1
    a_word_n14 = ['less 20', 'less than french 20']
    a_word_n16 = ['less $20', 'less the $20']

    a_word_ta4 = [' ad ', ' an d ', ' and and ', ' ans ']
    a_word_tb2 = ['as well as not begin', 'for begin', 'of begin']
    a_word_tc3 = ['city', 'of']
    a_word_tc7 = ['cit', 'cite']
    a_word_tc10 = ['of', 'ti']
    a_word_tc12 = ['coffee chop', 'coffee ship', 'coffee shoo', 'coffee shot', 'coffee show']
    a_word_tc14 = ['city', 'city centre']
    a_word_tc15 = ['customer', 'restaurant', 'shop']
    a_word_tc15_post = ['menu', 'prices', 'rating', 'reviews']
    a_word_tf4 = ['for', 'with']
    a_word_tf5 = ['for', 'is', 'of', 'over', 'the']
    a_word_th4 = ['hight', 'hugh', 'hi']
    a_word_ti3 = ['india', 'indiana']
    a_word_ti4 = ['in t he', 'int he']
    a_word_ti6 = ['has is', 'id', 'is is', 'sis']
    a_word_ti7 = ['i t', 'ot']
    a_word_ti9 = ['ia', 'it s']
    a_word_ti14 = ['a', 'located', 'not']
    a_word_tl1 = ['lees', 'lest']
    a_word_tl3 = ['after', 'we']
    a_word_tl7 = ['lo', 'ow']
    a_word_tl8 = ['less', 'lower', 'more']
    a_word_tl9 = ['located', 'river']
    a_word_tm3 = ['moire', 'ore']
    a_word_tn1 = ['bear', 'ear', 'nea', 'near it is', 'nears', 'neat', 'rear']
    a_word_tn2 = ['de', 'he']
    a_word_to1 = ['0f', 'fro', 'o']
    a_word_tp4 = ['prance', 'prince', 'prize']
    a_word_tp6 = ['ranch', 'rand', 'rang', 'rant']
    a_word_tp7 = [' pug ', ' pump ', ' pun ', ' pup ', ' rub ']
    a_word_tp8 = ['pub', 'restaurant', 'shop']
    a_word_tr1 = ['rage', 'rang', 'ranger', 'rant']
    a_word_tr3 = [' ranting', ' raring', ' ratting']
    a_word_tr8 = ['hear', 'need']
    a_word_ts3 = [' server ', ' servers ', ' seven ']
    a_word_tt6 = ['th', 'the the', 'thee', 'thew']
    a_word_tw2 = ['winch', 'witch']
    a_word_tw6 = ['when th', 'whit', 'wit h']

    ## named entities
    '''
    if ('crown plaza hotel' in obj['txt']) and (obj['mr']['near'] == ''):
        obj['mr']['near'] = 'crowne plaza hotel'
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('crown ', 'crowne ')
        dump_proc('(e-1)', value_old, obj['txt'], verbose_flag)
    '''        
    if ('crown plaza hotel' in obj['txt']):
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('crown plaza', 'crowne plaza')
        dump_proc('(e-1)', value_old, obj['txt'], verbose_flag)

    for word in a_word_e2:
        if (word+'s ' in obj['txt']) or \
           (word+'s.' in obj['txt']) or \
           (word+'s,' in obj['txt']) or \
           (word+'s:' in obj['txt']) or \
           (word+'s;' in obj['txt']) or \
           (word+'s?' in obj['txt']):
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(word+'s', word)
            dump_proc('(e-2)', value_old, obj['txt'], verbose_flag)

    if 'cotton' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('cotton', 'cotto')
        dump_proc('(e-3)', value_old, obj['txt'], verbose_flag)

    for word in a_word_e4:
        if word in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(word, 'fitzbillies')
            dump_proc('(e-4)', value_old, obj['txt'], verbose_flag)

    if 'golden city' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('golden city', 'golden curry')
        dump_proc('(e-5)', value_old, obj['txt'], verbose_flag)

    if 'raja cuisine' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('raja cuisine', 'raja indian cuisine')
        dump_proc('(e-6)', value_old, obj['txt'], verbose_flag)

    if 'cafe brazilian' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('cafe brazilian', 'cafe brazil')
        dump_proc('(e-7)', value_old, obj['txt'], verbose_flag)

    if 'yippee noodle bart' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('yippee noodle bart', 'yippee noodle bar')
        dump_proc('(e-8)', value_old, obj['txt'], verbose_flag)

    if 'cafe sicilian' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('cafe sicilian', 'cafe sicilia')
        dump_proc('(e-9)', value_old, obj['txt'], verbose_flag)

    if 'st john\'s college' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('st john', 'st. john')
        dump_proc('(e-10)', value_old, obj['txt'], verbose_flag)

    if 'raja located' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('raja located', 'raja indian cuisine located')
        dump_proc('(e-11)', value_old, obj['txt'], verbose_flag)

    if 'golden palace. n.' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('golden palace. n.', 'golden palace.')
        dump_proc('(e-12)', value_old, obj['txt'], verbose_flag)

    ## numbers
    value_old = obj['txt']
    for word in a_word_n1:
        if word+' of of 5' in obj['txt']:
            obj['txt'] = obj['txt'].replace(word+' of of 5', word+' out of 5')
        elif word+' of 5' in obj['txt']:
            obj['txt'] = obj['txt'].replace(word+' of 5', word+' out of 5')
        elif word+' out if 5' in obj['txt']:
            obj['txt'] = obj['txt'].replace(word+' out if 5', word+' out of 5')
        elif word+' of out 5' in obj['txt']:
            obj['txt'] = obj['txt'].replace(word+' of out 5', word+' out of 5')
        elif word+' out of a 5' in obj['txt']:
            obj['txt'] = obj['txt'].replace(word+' out of a 5', word+' out of 5')
        elif word+' out of,' in obj['txt']:
            obj['txt'] = obj['txt'].replace(word+' out of,', word+' out of 5,')
        elif word+' out of.' in obj['txt']:
            obj['txt'] = obj['txt'].replace(word+' out of.', word+' out of 5.')
        elif word+'of5' in obj['txt']:
            obj['txt'] = obj['txt'].replace(word+'of5', word+' out of 5')
        elif word+' out 5' in obj['txt']:
            obj['txt'] = obj['txt'].replace(word+' out 5', word+' out of 5')
        elif word+' our of 5' in obj['txt']:
            obj['txt'] = obj['txt'].replace(word+' our of 5', word+' out of 5')
        elif word+' out or 5' in obj['txt']:
            obj['txt'] = obj['txt'].replace(word+' out or 5', word+' out of 5')
        elif word+'out of 5' in obj['txt']:
            obj['txt'] = obj['txt'].replace(word+'out of 5', word+' out of 5')
        elif word+'out5' in obj['txt']:
            obj['txt'] = obj['txt'].replace(word+'out5', word+' out of 5')
        elif word+' out of5' in obj['txt']:
            obj['txt'] = obj['txt'].replace(word+' out of5', word+' out of 5')
        elif word+'-out of 5' in obj['txt']:
            obj['txt'] = obj['txt'].replace(word+'-out of 5', word+' out of 5')
        elif word+'-out-of-5' in obj['txt']:
            obj['txt'] = obj['txt'].replace(word+'-out-of-5', word+' out of 5')
        elif word+' of of five' in obj['txt']:
            obj['txt'] = obj['txt'].replace(word+' of of five', word+' out of five')
        elif word+' of five' in obj['txt']:
            obj['txt'] = obj['txt'].replace(word+' of five', word+' out of five')
        elif word+'offive' in obj['txt']:
            obj['txt'] = obj['txt'].replace(word+'offive', word+' out of five')
        elif word+' out five' in obj['txt']:
            obj['txt'] = obj['txt'].replace(word+' out five', word+' out of five')
        elif word+' our of five' in obj['txt']:
            obj['txt'] = obj['txt'].replace(word+' our of five', word+' out of five')
        elif word+'out of five' in obj['txt']:
            obj['txt'] = obj['txt'].replace(word+'out of five', word+' out of five')
        elif word+' out offive' in obj['txt']:
            obj['txt'] = obj['txt'].replace(word+' out offive', word+' out of five')
        elif word+' out of customer' in obj['txt']:
            obj['txt'] = obj['txt'].replace(word+' out of customer', word+' out of 5 customer')
    if '2 out of 5' in obj['txt']:
        obj['txt'] = obj['txt'].replace('2 out of 5', '3 out of 5')
    if 'of out of 5' in obj['txt']:
        obj['txt'] = obj['txt'].replace('of out of 5', 'of 5 out of 5')
    if 'rating out of 5' in obj['txt']:
        obj['txt'] = obj['txt'].replace('rating out of 5', 'rating 5 out of 5')
    if 'with a out of 5 rating' in obj['txt']:
        obj['txt'] = obj['txt'].replace('with a out of 5 rating', 'with 1 out of 5 rating')

    dump_proc('(n-1)', value_old, obj['txt'], verbose_flag)

    for word in a_word_n2:
        if word in obj['txt']:
            value_old = obj['txt']
            new_word_n2 = word.replace('5', '5 ')
            obj['txt'] = obj['txt'].replace(word, new_word_n2)
            dump_proc('(n-2)', value_old, obj['txt'], verbose_flag)

    for word in a_word_n3:
        if 'then ' + word in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace('then ', 'than ')
            dump_proc('(n-3)', value_old, obj['txt'], verbose_flag)

    if '30and' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('30and', '30 and')
        dump_proc('(n-4)', value_old, obj['txt'], verbose_flag)

    if '$and' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('$and', '$30 and')
        dump_proc('(n-5)', value_old, obj['txt'], verbose_flag)

    for word in a_word_n6:
        if word in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(word, '$30')
            dump_proc('(n-6)', value_old, obj['txt'], verbose_flag)

    if 'or5' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('or5', 'of 5')
        dump_proc('(n-7)', value_old, obj['txt'], verbose_flag)

    if '.6.' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('.6.', '.')
        dump_proc('(n-8)', value_old, obj['txt'], verbose_flag)

    if 'rating3' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('rating3', 'rating 3')
        dump_proc('(n-9)', value_old, obj['txt'], verbose_flag)

    if 'a1' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('a1', 'a 1')
        dump_proc('(n-10)', value_old, obj['txt'], verbose_flag)

    for word in a_word_n11:
        if word+' start ' in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(word+' start ', word+' star ')
            dump_proc('(n-11)', value_old, obj['txt'], verbose_flag)

    if '5 tars' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('5 tars', '5 stars')
        dump_proc('(n-12)', value_old, obj['txt'], verbose_flag)

    if 'more than french 30' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('more than french 30', 'more than 30')
        dump_proc('(n-13)', value_old, obj['txt'], verbose_flag)

    for word in a_word_n14:
        if word in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(word, 'less than 20')
            dump_proc('(n-14)', value_old, obj['txt'], verbose_flag)

    if 'price is than $20' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('price is than $20', 'price is less than $20')
        dump_proc('(n-15)', value_old, obj['txt'], verbose_flag)

    for word in a_word_n16:
        if word in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(word, 'less than $20')
            dump_proc('(n-16)', value_old, obj['txt'], verbose_flag)

    if 'for less.' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('for less.', 'for less than $20.')
        dump_proc('(n-17)', value_old, obj['txt'], verbose_flag)

    if 'rating it a ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('rating it a ', 'rating it as ')
        dump_proc('(n-18)', value_old, obj['txt'], verbose_flag)

    if '2 out of 3 price rated' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('2 out of 3 price rated', '3 out of 5 rated')
        dump_proc('(n-19)', value_old, obj['txt'], verbose_flag)

    if ' to5' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace(' to5', ' to 5')
        dump_proc('(n-20)', value_old, obj['txt'], verbose_flag)

    ## other typos
    if ' s ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace(' s ', ' a ')
        dump_proc('(t-a1)', value_old, obj['txt'], verbose_flag)

    if ' am ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace(' am ', ' an ')
        dump_proc('(t-a2)', value_old, obj['txt'], verbose_flag)

    if ' ad average ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace(' ad average ', ' an average ')
        dump_proc('(t-a3)', value_old, obj['txt'], verbose_flag)

    for word in a_word_ta4:
        if word in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(word,  ' and ')
            dump_proc('(t-a4)', value_old, obj['txt'], verbose_flag)

    if 'and re not' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('and re not', 'and are not')
        dump_proc('(t-a5)', value_old, obj['txt'], verbose_flag)

    if ' a has ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace(' a has ', ' and has ')
        dump_proc('(t-a6)', value_old, obj['txt'], verbose_flag)

    if 'an dis not' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('an dis not', 'and is not')
        dump_proc('(t-a7)', value_old, obj['txt'], verbose_flag)

    if ' ares ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace(' ares ', ' areas ')
        dump_proc('(t-a8)', value_old, obj['txt'], verbose_flag)

    if ' y ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace(' y ', ' at ')
        dump_proc('(t-a9)', value_old, obj['txt'], verbose_flag)

    if ' a t a ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace(' a t a ', ' at a ')
        dump_proc('(t-a10)', value_old, obj['txt'], verbose_flag)

    if '. and' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('. and', ', and')
        dump_proc('(t-a11)', value_old, obj['txt'], verbose_flag)

    if 'anon-children' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('anon-children', 'a non-children')
        dump_proc('(t-a12)', value_old, obj['txt'], verbose_flag)

    if '. aren\'t' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('. aren\'t', ' aren\'t')
        dump_proc('(t-a13)', value_old, obj['txt'], verbose_flag)

    if ' e ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace(' e ', ' be ')
        dump_proc('(t-b1)', value_old, obj['txt'], verbose_flag)

    for word in a_word_tb2:
        if word in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(word, 'begin')
            dump_proc('(t-b2)', value_old, obj['txt'], verbose_flag)

    if 'besides from' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('besides from', 'beside')
        dump_proc('(t-b3)', value_old, obj['txt'], verbose_flag)

    if ' cant ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace(' cant ', ' can\'t ')
        dump_proc('(t-c1)', value_old, obj['txt'], verbose_flag)

    if ' carer ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace(' carer ', ' care ')
        dump_proc('(t-c2)', value_old, obj['txt'], verbose_flag)

    for word in a_word_tc3:
        if 'centre. '+word in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace('centre. '+word, 'centre '+word)
            dump_proc('(t-c3)', value_old, obj['txt'], verbose_flag)

    if 'cheep' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('cheep', 'cheap')
        dump_proc('(t-c4)', value_old, obj['txt'], verbose_flag)

    if 'chines ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('chines ', 'chinese ')
        dump_proc('(t-c5)', value_old, obj['txt'], verbose_flag)

    if ' city city' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace(' city city', ' city')
        dump_proc('(t-c6)', value_old, obj['txt'], verbose_flag)

    for word in a_word_tc7:
        if word + ' centre' in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(word, 'city')
            dump_proc('(t-c7)', value_old, obj['txt'], verbose_flag)

    if 'clentele' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('clentele', 'clientele')
        dump_proc('(t-c8)', value_old, obj['txt'], verbose_flag)

    if 'close by is' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('close by is', 'close by')
        dump_proc('(t-c9)', value_old, obj['txt'], verbose_flag)

    for word in a_word_tc10:
        if 'close '+ word in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace('close '+word, 'close to')
            dump_proc('(t-c10)', value_old, obj['txt'], verbose_flag)

    if 'coffeehouse' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('coffeehouse', 'coffee house')
        dump_proc('(t-c11)', value_old, obj['txt'], verbose_flag)

    for word in a_word_tc12:
        if word in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(word, 'coffee shop')
            dump_proc('(t-c12)', value_old, obj['txt'], verbose_flag)

    if 'costumer' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('costumer', 'customer')
        dump_proc('(t-c13)', value_old, obj['txt'], verbose_flag)

    for word in a_word_tc14:
        if word + ' after' in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(word + ' after', word + ' near')
            dump_proc('(t-c14)', value_old, obj['txt'], verbose_flag)

    for word in a_word_tc15:
        for word_post in a_word_tc15_post:
            if ' '+word+'s\" '+word_post in obj['txt']:
                value_old = obj['txt']
                obj['txt'] = obj['txt'].replace(' '+word+'s\" ', ' '+word+'\'s ')
                dump_proc('(t-c15)', value_old, obj['txt'], verbose_flag)

    if 'customer rating is cheap' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('customer rating is cheap', 'customer rating is low')
        dump_proc('(t-c16)', value_old, obj['txt'], verbose_flag)

    if 'customer rating it a ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('customer rating it a ', 'customer rating it as ')
        dump_proc('(t-c17)', value_old, obj['txt'], verbose_flag)

    if 'steve\'s chinese' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('steve\'s chinese', 'chinese')
        dump_proc('(t-c18)', value_old, obj['txt'], verbose_flag)

    if 'desert' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('desert', 'dessert')
        dump_proc('(t-d1)', value_old, obj['txt'], verbose_flag)

    if 'eat t ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('eat t ', 'eat ')
        dump_proc('(t-e1)', value_old, obj['txt'], verbose_flag)

    if 'en tree' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('en tree', 'entree')
        dump_proc('(t-e2)', value_old, obj['txt'], verbose_flag)

    if obj['txt'].startswith('es '):
        value_old = obj['txt']
        obj['txt'] = obj['txt'].lstrip('es ')
        dump_proc('(t-e3)', value_old, obj['txt'], verbose_flag)

    if ' eve though' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace(' eve though', ' even though')
        dump_proc('(t-e4)', value_old, obj['txt'], verbose_flag)

    if ' foe ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace(' foe ', ' for ')
        dump_proc('(t-f2)', value_old, obj['txt'], verbose_flag)

    if 'rood' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace(' rood', ' food')
        dump_proc('(t-f1)', value_old, obj['txt'], verbose_flag)

    if 'fore more' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('fore more', 'for more')
        dump_proc('(t-f3)', value_old, obj['txt'], verbose_flag)

    for word in a_word_tf4:
        if word+' it\'s' in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(word+' it\'s', word+' its')
            dump_proc('(t-f4)', value_old, obj['txt'], verbose_flag)

    for word in a_word_tf5:
        if word + '$' in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(word + '$' , word + ' $')
            dump_proc('(t-f5)', value_old, obj['txt'], verbose_flag)

    if 'friend;y' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('friend;y', 'friendly')
        dump_proc('(t-f6)', value_old, obj['txt'], verbose_flag)

    if 'fast found' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('fast found', 'fast food')
        dump_proc('(t-f7)', value_old, obj['txt'], verbose_flag)

    if 'grate' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('grate', 'great')
        dump_proc('(t-g1)', value_old, obj['txt'], verbose_flag)

    if 'hamgurgers' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('hamgurgers', 'hamburgers')
        dump_proc('(t-h1)', value_old, obj['txt'], verbose_flag)

    if 'ha ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('ha ', 'has ')
        dump_proc('(t-h2)', value_old, obj['txt'], verbose_flag)

    if '\'s has' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('\'s has', ' has')
        dump_proc('(T-h3)', value_old, obj['txt'], verbose_flag)

    for word in a_word_th4:
        if word+' ' in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(word+' ', 'high ')
            dump_proc('(t-h4)', value_old, obj['txt'], verbose_flag)

    if ' n ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace(' n ', ' in ')
        dump_proc('(t-i1)', value_old, obj['txt'], verbose_flag)

    if ' ina ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace(' ina ', ' in a ')
        dump_proc('(t-i2)', value_old, obj['txt'], verbose_flag)

    for word in a_word_ti3:
        if ' '+word+' ' in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(' '+word+' ', ' indian ')
            dump_proc('(t-i3)', value_old, obj['txt'], verbose_flag)

    for word in a_word_ti4:
        if word in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(word,  'in the')
            dump_proc('(t-i4)', value_old, obj['txt'], verbose_flag)

    if obj['txt'].startswith('n the'):
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('n the', 'in the')
        dump_proc('(t-i5)', value_old, obj['txt'], verbose_flag)

    for word in a_word_ti6:
        if ' '+word+' ' in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(' '+word+' ', ' '+'is'+' ')
            dump_proc('(t-i6)', value_old, obj['txt'], verbose_flag)

    for word in a_word_ti7:
        if ' '+word+' ' in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(' '+word+' ', ' it ')
            dump_proc('(t-i7)', value_old, obj['txt'], verbose_flag)

    if 'next to it is' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('next to it is', 'it is next to')
        dump_proc('(t-i8)', value_old, obj['txt'], verbose_flag)

    for word in a_word_ti9:
        if ' '+word+' ' in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(' '+word+' ', ' it is ')
            dump_proc('(t-i9)', value_old, obj['txt'], verbose_flag)        

    if ' t offers' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace(' t offers', ' it offers')
        dump_proc('(t-i10)', value_old, obj['txt'], verbose_flag)

    if 'thats ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('thats ', 'its ')
        dump_proc('(t-i11)', value_old, obj['txt'], verbose_flag)

    if 'it\'s neighbour' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('it\'s neighbour', 'its neighbour')
        dump_proc('(t-i12)', value_old, obj['txt'], verbose_flag)

    if ' it\" ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace(' it\" ', ' it\'s ')
        dump_proc('(t-i13)', value_old, obj['txt'], verbose_flag)

    for word in a_word_ti14:
        if 'its '+word+' ' in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace('its '+word+' ', 'it\'s '+word+' ')
            dump_proc('(t-i14)', value_old, obj['txt'], verbose_flag)

    if 'kid\'s friendly' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('kid\'s', 'kids')
        dump_proc('(t-k1)', value_old, obj['txt'], verbose_flag)

    if 'kind friendly' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('kind', 'kid')
        dump_proc('(t-k2)', value_old, obj['txt'], verbose_flag)

    for word in a_word_tl1:
        if word in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(word, 'less')
            dump_proc('(t-l1)', value_old, obj['txt'], verbose_flag)

    if 'lets go' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('lets go', 'let\'s go')
        dump_proc('(t-l2)', value_old, obj['txt'], verbose_flag)

    for word in a_word_tl3:
        if 'located ' + word in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace('located '+word, 'located at')
            dump_proc('(t-l3)', value_old, obj['txt'], verbose_flag)

    if 'locate din' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('locate din', 'located in')
        dump_proc('(t-l4)', value_old, obj['txt'], verbose_flag)

    if 'located new' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('located new', 'located near')
        dump_proc('(t-l5)', value_old, obj['txt'], verbose_flag)

    if 'lover that' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('lover that', 'lower than')
        dump_proc('(t-l6)', value_old, obj['txt'], verbose_flag)

    for word in a_word_tl7:
        if ' '+word+' ' in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(' '+word+' ', ' low ')
            dump_proc('(t-l7)', value_old, obj['txt'], verbose_flag)

    for word in a_word_tl8:
        if word+' that' in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(word+' that', word+' than')
            dump_proc('(t-l8)', value_old, obj['txt'], verbose_flag)

    for word in a_word_tl9:
        if word + ' besides' in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(word + ' besides', word + ' beside')
            dump_proc('(t-l9)', value_old, obj['txt'], verbose_flag)

    if 'lower $20' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('lower $20', 'lower than $20')
        dump_proc('(t-l10)', value_old, obj['txt'], verbose_flag)

    if 'moder ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('moder ', 'moderate ')
        dump_proc('(t-m1)', value_old, obj['txt'], verbose_flag)

    if 'more then ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('more then', 'more than')
        dump_proc('(t-m2)', value_old, obj['txt'], verbose_flag)

    for word in a_word_tm3:
        if ' '+word+' ' in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(' '+word+' ', ' more ')
            dump_proc('(t-m3)', value_old, obj['txt'], verbose_flag)

    for word in a_word_tn1:
        if ' ' + word + ' ' in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(word, 'near')
            dump_proc('(t-n1)', value_old, obj['txt'], verbose_flag)

    for word in a_word_tn2:
        if 'near '+word+' ' in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace('near '+word+' ', 'near the ')
            dump_proc('(t-n2)', value_old, obj['txt'], verbose_flag)

    if 'near yo ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('near yo ', 'near to ')
        dump_proc('(t-n3)', value_old, obj['txt'], verbose_flag)

    if 'nested' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('nested', 'nestled')
        dump_proc('(t-n4)', value_old, obj['txt'], verbose_flag)

    if 'located next' in obj['txt']:
        loc = obj['txt'].find('located next')
        if obj['txt'][loc:].startswith('located next to') is False:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace('located next', 'located next to')
            dump_proc('(t-n5)', value_old, obj['txt'], verbose_flag)

    a_word_tn6 = ['mot', 'no t', 't not']
    for word in a_word_tn6:
        if ' '+word+' ' in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(' '+word+' ', ' not ')
            dump_proc('(t-n6)', value_old, obj['txt'], verbose_flag)

    for word in a_word_to1:
        if ' '+word+' ' in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(' '+word+' ', ' of ')
            dump_proc('(t-o1)', value_old, obj['txt'], verbose_flag)

    if ' don ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace(' don ', ' on ')
        dump_proc('(t-o2)', value_old, obj['txt'], verbose_flag)

    if 'out ff' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('out ff', 'out of')
        dump_proc('(t-o3)', value_old, obj['txt'], verbose_flag)

    if 'one-one' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('one-one', 'one')
        dump_proc('(t-o4)', value_old, obj['txt'], verbose_flag)

    if ' lace' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace(' lace', ' place')
        dump_proc('(t-p1)', value_old, obj['txt'], verbose_flag)

    if 'play to' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('play to', 'place to')
        dump_proc('(t-p2)', value_old, obj['txt'], verbose_flag)

    if 'ponds' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('ponds', 'pounds')
        dump_proc('(t-p3)', value_old, obj['txt'], verbose_flag)

    for word in a_word_tp4:
        if word in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(word, 'price')
            dump_proc('(t-p4)', value_old, obj['txt'], verbose_flag)

    if 'pried' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('pried', 'priced')
        dump_proc('(t-p5)', value_old, obj['txt'], verbose_flag)

    for word in a_word_tp6:
        if 'price '+word+' ' in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace('price '+word+' ', 'price range ')
            dump_proc('(t-p6)', value_old, obj['txt'], verbose_flag)
        if 'price '+word+',' in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace('price '+word+',', 'price range,')
            dump_proc('(t-p6)', value_old, obj['txt'], verbose_flag)
        if 'price '+word+'ing' in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace('price '+word+'ing', 'price ranging')
            dump_proc('(t-p6)', value_old, obj['txt'], verbose_flag)

    for word in a_word_tp7:
        if word in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(word,  ' pub ')
            dump_proc('(t-p7)', value_old, obj['txt'], verbose_flag)

    for word in a_word_tp8:
        if word+'pe ' in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(word+'pe ', word+' ')
            dump_proc('(t-p8)', value_old, obj['txt'], verbose_flag)

    if 'pup,' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('pup,', 'pub,')
        dump_proc('(t-p9)', value_old, obj['txt'], verbose_flag)

    for word in a_word_tr1:
        if ' '+word+' ' in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(' '+word+' ',  ' range ')
            dump_proc('(t-r1)', value_old, obj['txt'], verbose_flag)

    if ' ran.' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace(' ran.', ' range.')
        dump_proc('(t-r2)', value_old, obj['txt'], verbose_flag)

    for word in a_word_tr3:
        if word in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(word,  ' rating')
            dump_proc('(t-r3)', value_old, obj['txt'], verbose_flag)

    if 'rating g of' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('rating g of', 'rating of')
        dump_proc('(t-r4)', value_old, obj['txt'], verbose_flag)

    if 'ratings is ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('ratings is ', 'ratings are ')
        dump_proc('(t-r5)', value_old, obj['txt'], verbose_flag)

    if 'restaurantr ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('restaurantr ', 'restaurant ')
        dump_proc('(t-r6)', value_old, obj['txt'], verbose_flag)

    if 'restaurant and restaurant' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('restaurant and restaurant', 'restaurant and')
        dump_proc('(t-r7)', value_old, obj['txt'], verbose_flag)

    for word in a_word_tr8:
        if 'restaurant '+word in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace('restaurant '+word, 'restaurant near')
            dump_proc('(t-r8)', value_old, obj['txt'], verbose_flag)

    if 'right off of ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('right off of ', 'right off ')
        dump_proc('(t-r9)', value_old, obj['txt'], verbose_flag)

    if ' rive ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace(' rive ', ' river ')
        dump_proc('(t-r10)', value_old, obj['txt'], verbose_flag)

    if ' rd' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace(' rd', ' road')
        dump_proc('(t-r11)', value_old, obj['txt'], verbose_flag)

    if 'rating and.' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('rating and.', 'rating.')
        dump_proc('(t-r12)', value_old, obj['txt'], verbose_flag)

    if 'rating f ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('rating f ', 'rating of ')
        dump_proc('(t-r13)', value_old, obj['txt'], verbose_flag)

    if 'restaurant l ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('restaurant l ', 'restaurant ')
        dump_proc('(t-r14)', value_old, obj['txt'], verbose_flag)

    if ' rant.' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace(' rant.', ' range.')
        dump_proc('(t-r15)', value_old, obj['txt'], verbose_flag)

    if ' rive.' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace(' rive.', ' river.')
        dump_proc('(t-r16)', value_old, obj['txt'], verbose_flag)

    if ' price rage' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace(' price rage', ' price range')
        dump_proc('(t-r17)', value_old, obj['txt'], verbose_flag)

    if ' of of ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace(' of of ', ' of ')
        dump_proc('(t-s1)', value_old, obj['txt'], verbose_flag)

    if ' sered ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace(' sered ', ' served ')
        dump_proc('(t-s2)', value_old, obj['txt'], verbose_flag)

    for word in a_word_ts3:
        if word in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(word,  ' serves ')
            dump_proc('(t-s3)', value_old, obj['txt'], verbose_flag)

    if 'stake' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('stake', 'steak')
        dump_proc('(t-s4)', value_old, obj['txt'], verbose_flag)

    if 'swhiched' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('swhiched', 'switched')
        dump_proc('(t-s5)', value_old, obj['txt'], verbose_flag)

    if 'sushigh ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('sushigh ', 'sushi ')
        dump_proc('(t-s6)', value_old, obj['txt'], verbose_flag)

    if 'tale' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('tale', 'take')
        dump_proc('(t-t1)', value_old, obj['txt'], verbose_flag)

    if 'tapa,' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('tapa,', 'tapas,')
        dump_proc('(t-t2)', value_old, obj['txt'], verbose_flag)

    if 'then$20' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('then$20', 'than $20')
        dump_proc('(t-t3)', value_old, obj['txt'], verbose_flag)

    if ' hat ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace(' hat ', ' that ')
        dump_proc('(t-t4)', value_old, obj['txt'], verbose_flag)

    if ' tat' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace(' tat', ' that')
        dump_proc('(t-t5)', value_old, obj['txt'], verbose_flag)

    for word in a_word_tt6:
        if ' ' + word + ' ' in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(' '+word+' ', ' the ')
            dump_proc('(t-t6)', value_old, obj['txt'], verbose_flag)

    if obj['txt'].startswith('th fast'):
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('th fast', 'the fast')
        dump_proc('(t-t7)', value_old, obj['txt'], verbose_flag)

    if 'theres a' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('theres a', 'there\'s a')
        dump_proc('(t-t8)', value_old, obj['txt'], verbose_flag)

    if 'theres is' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('theres is', 'there is')
        dump_proc('(t-t9)', value_old, obj['txt'], verbose_flag)

    if 'thought' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('thought', 'though')
        dump_proc('(t-t10)', value_old, obj['txt'], verbose_flag)

    if 'to est' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('to est', 'to rest')
        dump_proc('(t-t11)', value_old, obj['txt'], verbose_flag)

    if 'to expensive' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('to expensive', 'too expensive')
        dump_proc('(t-t12)', value_old, obj['txt'], verbose_flag)

    if 'whee' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('whee', 'where')
        dump_proc('(t-w1)', value_old, obj['txt'], verbose_flag)

    for word in a_word_tw2:
        if word in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(word, 'which')
            dump_proc('(t-w2)', value_old, obj['txt'], verbose_flag)

    if 'whine' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('whine', 'wine')
        dump_proc('(t-w3)', value_old, obj['txt'], verbose_flag)

    if 'wit a' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('wit a', 'with a')
        dump_proc('(t-w4)', value_old, obj['txt'], verbose_flag)

    if 'wont' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('wont', 'won\'t')
        dump_proc('(t-w5)', value_old, obj['txt'], verbose_flag)

    for word in a_word_tw6:
        if ' '+word+' ' in obj['txt']:
            value_old = obj['txt']
            obj['txt'] = obj['txt'].replace(' '+word+' ', ' with ')
            dump_proc('(t-w6)', value_old, obj['txt'], verbose_flag)

    if 'yippe ' in obj['txt']:
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace('yippe ', 'yippee ')
        dump_proc('(t-y1)', value_old, obj['txt'], verbose_flag)

    ## indefinite articles
    flag = False
    value_old = obj['txt']
    a_tmp = obj['txt'].split(' ')
    for j in range(len(a_tmp)-1):
        if (a_tmp[j] == 'an') and \
           ((a_tmp[j+1].startswith('a') is False) and \
            (a_tmp[j+1].startswith('e') is False) and \
            (a_tmp[j+1].startswith('i') is False) and \
            (a_tmp[j+1].startswith('o') is False) and \
            (a_tmp[j+1].startswith('u') is False)):
            a_tmp[j] = 'a'
            flag = True
    if flag is True:
        obj['txt'] = a_tmp[0]
        for j in range(1, len(a_tmp)):
            obj['txt'] += ' ' + a_tmp[j]
        dump_proc('(i-1)', value_old, obj['txt'], verbose_flag)

    flag = False
    value_old = obj['txt']
    a_tmp = obj['txt'].split(' ')
    for j in range(len(a_tmp)-1):
        if (a_tmp[j] == 'a') and \
           ((a_tmp[j+1].startswith('a') is True) or (a_tmp[j+1].startswith('e') is True) or (a_tmp[j+1].startswith('i') is True) or (a_tmp[j+1].startswith('o') is True) or (a_tmp[j+1].startswith('u') is True)) and \
           (a_tmp[j+1].startswith('one') is False):
            a_tmp[j] = 'an'
            flag = True
    if flag is True:
        obj['txt'] = a_tmp[0]
        for j in range(1, len(a_tmp)):
            obj['txt'] += ' ' + a_tmp[j]
        dump_proc('(i-2)', value_old, obj['txt'], verbose_flag)

    # NAMEs / NEARs
    if (obj['mr']['name'] != '') and (obj['mr']['name']+'s' in obj['txt']):
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace(obj['mr']['name']+'s', obj['mr']['name'])
        dump_proc('(j-1)', value_old, obj['txt'], verbose_flag)
    if (obj['mr']['near'] != '') and (obj['mr']['near']+'s' in obj['txt']):
        value_old = obj['txt']
        obj['txt'] = obj['txt'].replace(obj['mr']['near']+'s', obj['mr']['near'])
        dump_proc('(j-2)', value_old, obj['txt'], verbose_flag)

    return obj

## (5-C) quotation error
def filter_quotation(obj, verbose_flag):
    # (Q-1) add space to hyphen
    for attr in ['name', 'near']:
        if obj['mr'][attr] != '':
            if '-'+obj['mr'][attr] in obj['txt']:
                loc = obj['txt'].find('-'+obj['mr'][attr])
                if (loc > 0) and (obj['txt'][loc-1] != ' '):
                    value_old = obj['txt']
                    obj['txt'] = obj['txt'][:loc] + ' - ' + obj['txt'][loc+len('-'):]
                    dump_proc('(Q-1(pre))', value_old, obj['txt'], verbose_flag)

            if obj['mr'][attr]+'-' in obj['txt']:
                loc = obj['txt'].find(obj['mr'][attr]+'-')
                if ((loc+len(obj['mr'][attr]+'-')) < len(obj['txt'])) and (obj['txt'][loc+len(obj['mr'][attr]+'-')] != ' '):
                    value_old = obj['txt']
                    obj['txt'] = obj['txt'][:loc+len(obj['mr'][attr])] + ' - ' + obj['txt'][loc+len(obj['mr'][attr]+'-'):]
                    dump_proc('(Q-1(post))', value_old, obj['txt'], verbose_flag)
            
    # (Q-2) double-quotation at only prefix ("hoge)
    for attr in ['name', 'near']:
        if obj['mr'][attr] != '':
            if '\"'+obj['mr'][attr]+' ' in obj['txt']:
                postfix = ' '
            elif '\"'+obj['mr'][attr]+'.' in obj['txt']:
                postfix = '.'
            elif '\"'+obj['mr'][attr]+',' in obj['txt']:
                postfix = ','
            elif '\"'+obj['mr'][attr]+':' in obj['txt']:
                postfix = ':'
            elif '\"'+obj['mr'][attr]+';' in obj['txt']:
                postfix = ';'
            elif '\"'+obj['mr'][attr]+'?' in obj['txt']:
                postfix = '?'
            else:
                postfix = ''
            if postfix != '':
                loc = obj['txt'].find('\"'+obj['mr'][attr]+postfix)
                value_old = obj['txt']
                obj['txt'] = obj['txt'][:loc+len(obj['mr'][attr]+postfix)]+'"'+obj['txt'][loc+len(obj['mr'][attr]+postfix):]
                dump_proc('(Q-2)', value_old, obj['txt'], verbose_flag)
                
    # (Q-3) double-quotation at only postfix (hoge")
    for attr in ['name', 'near']:
        if obj['mr'][attr] != '':
            loc = obj['txt'].find(obj['mr'][attr]+'\"')
            if (loc == 0) or \
               ((loc > 0) and obj['txt'][loc-1] == ' '):
                value_old = obj['txt']
                obj['txt'] = obj['txt'][:loc] + '"' + obj['txt'][loc:]
                dump_proc('(Q-3)', value_old, obj['txt'], verbose_flag)

    return obj

## (5-D) remove overlap
def filter_overlap(obj, verbose_flag):
    a_phrase = obj['txt'].split(', ')
    if len(a_phrase) > 1:
        idx_overlap = -1
        for i in range(len(a_phrase)-1):
            for j in range(i+1, len(a_phrase)):
                if a_phrase[i] == a_phrase[j]:
                    idx_overlap = j
                    break
        if idx_overlap >= 0:
            txt = ''
            for i, phrase in enumerate(a_phrase):
                if i == idx_overlap:
                    continue
                if i > 0:
                    txt += ', '
                txt += phrase
            if verbose_flag is True:
                print('[remove overlap]')
                print('org: '+obj['txt'])
                print('new: '+txt)
            obj['txt'] = txt

    return obj

## (4) remove duplication
def remove_duplication(a_obj_in):
    for i in range(len(a_obj_in)):
        for j in range(0, i):
            if (a_obj_in[i]['mr'] == a_obj_in[j]['mr']) and \
               (a_obj_in[i]['txt'] == a_obj_in[j]['txt']):
               a_obj_in[i]['remarks'] = 'dupulicate of '+str(a_obj_in[i]['id'])
    return a_obj_in

## main function
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='input data')
    parser.add_argument('-o', help='output data')
    parser.add_argument('-v', help='verbose flag', action='store_true')
    args = parser.parse_args()

    print('** correct_txt: E2E txt correction **')
    print(' input  (json) : '+str(args.i))
    print(' output (json) : '+str(args.o))

    # (0) obtain original lines
    with open(args.i, 'r', encoding='utf-8') as fi:
        a_obj = json.load(fi)

    # (1) extend object
    a_obj = extend_obj(a_obj)

    # (2) remove weird sentence
    a_obj = remove_sentences(a_obj)

    # (3) error correction
    a_obj = correct_error(a_obj, args.v)

    # (4) remove duplication
    a_obj = remove_duplication(a_obj)

    # (5) dump file
    with open(args.o, 'w', encoding='utf-8') as fo:
        json.dump(a_obj, fo, ensure_ascii=False, indent=4, sort_keys=False)

    print('** done **')

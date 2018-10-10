import random
import string
import logging
from sre_parse import parse

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

#Reference: https://github.com/python/cpython/blob/master/Lib/sre_parse.py

class RandomString:
    
    def __init__(self, max_repeat):
        self.max_repeat = max_repeat # maximum repeat sequence allowed in case of []* and []+
        letters = string.ascii_letters + string.digits + string.punctuation
        self.letters_code = [ord(i) for i in letters]
    
    def add_more_letters(self, extra_letters):
        self.letters_code = self.letters_code + [ord(i) for i in extra_letters]
        
    def dump(self, iregex):
        """
        dump parsed regex output on terminal,
        displaying various opcodes and corresponding
        values
        """
        iregex_parse = parse(iregex)
        iregex_parse.dump()
        
    def __opcode_in__(self, npattern, nlist):
        """
        Generate string recursively
        npatttern: is a pattern list containing tuples in the form => (opcode, literal_value_or_range)
        nlist: list returned with allowed characters
        """
        negate = False
        negate_list = []
        for atuple in npattern:
            logger.debug(atuple)
            opcode = str(atuple[0]).lower()
            if opcode == 'literal':
                if negate:
                    negate_list.append(atuple[1])
                else:
                    nlist.append(atuple[1])
            elif opcode == 'negate':
                negate = True
            elif opcode == 'category':
                category = str(atuple[1]).lower()
                string_list = None
                if category == 'category_digit':
                    string_list = string.digits
                elif category == 'category_word':
                    string_list = string.ascii_letters + string.digits + '_'
                elif category == 'category_not_word':
                    string_list = string.punctuation.replace('_', '')
                elif category == 'category_space':
                    string_list = string.whitespace
                else:
                    logger.error('category: {} not handled'.format(category))
                for i in string_list:
                    if negate:
                        negate_list.append(ord(i))
                    else:
                        nlist.append(ord(i))
            elif opcode == 'in':
                logger.debug('in {}'.format(atuple[1]))
                tlist = self.__opcode_in__(atuple[1], [])
                nlist.append(random.choice(tlist))
                logger.debug(nlist)
            elif opcode == 'not_literal':
                tval = random.choice(self.letters_code)
                logger.debug('{} {}'.format(tval, atuple[1]))
                while tval == atuple[1]:
                    logger.debug('random value not allowed: trying again')
                    tval = random.choice(self.letters_code)
                nlist.append(tval)
            elif opcode == 'any':
                nlist.append(random.choice(self.letters_code))
            elif opcode == 'range':
                low, high = atuple[1]
                for i in range(low, high+1):
                    if negate:
                        negate_list.append(i)
                    else:
                        nlist.append(i)
            elif opcode == 'subpattern':
                logger.debug('subpattern: {}'.format(atuple))
                tlist = self.__opcode_in__(atuple[1][3], [])
                logger.debug(tlist)
                for i in tlist:
                    nlist.append(i)
            elif opcode == 'branch':
                sample_list = []
                if isinstance(atuple[1], list):
                    slist = atuple[1]
                elif isinstance(atuple[1], tuple):
                    slist = atuple[1][1]
                for sublist in slist:
                    tlist = self.__opcode_in__(sublist, [])
                    sample_list.append(tlist.copy())
                sample = random.choice(sample_list)
                for i in sample:
                    nlist.append(i)
            elif opcode in ['max_repeat', 'min_repeat']:
                if str(atuple[1][1]).lower() == 'maxrepeat':
                    max_repeat = self.max_repeat
                else:
                    max_repeat = atuple[1][1]
                rval = random.randint(atuple[1][0], max_repeat)
                pat = atuple[1][2]
                logger.debug('repeating sequence {} times'.format(rval))
                if isinstance(pat.data[0], tuple):
                    subop = str(pat.data[0][0])
                    npat = pat.data[0][1]
                    logger.debug('{} ===>'.format(npat))
                    if subop.lower() == 'in':
                        tlist = self.__opcode_in__(npat, [])
                    elif subop.lower() == 'subpattern':
                        tlist = []
                        for i in range(rval):
                            tmplist = self.__opcode_in__(npat[3], [])
                            tlist = tlist + tmplist
                    elif subop.lower() == 'literal':
                        tlist.append(npat)
                    else:
                        logger.error('opcode not handled {} {}'.format(subop, npat))
                        
                nnlist = [] #new list containing repeated sequence
                if rval == 0:
                    tlist.clear() #clear tlist if repeat is 0 times
                elif rval > 0 and subop.lower() != 'subpattern':
                    for i in range(rval): #select random value from tlist for rval times and append it to nnlist
                        x = random.choices(tlist) 
                        nnlist = nnlist + x
                elif rval > 0 and subop.lower() == 'subpattern':
                    nnlist = nnlist + tlist
                nlist = nlist + nnlist
                
        if negate_list:
            negate_set = set(negate_list)
            for i in self.letters_code:
                if i not in negate_set:
                    nlist.append(i)
        return nlist
    
    def generate_random_string(self, iregex):
        ascii_list = []
        iregex_parse = parse(iregex)
        for op, args in iregex_parse.data:
            ascii_list = ascii_list + self.__opcode_in__([(op, args)], [])
        logger.debug(ascii_list)
        final = [str(chr(i)) for i in ascii_list] #convert ascii integers to corresponding characters
        final_string = ''.join(final)
        return final_string



#!/usr/bin/env python

import itertools
import marshal
import os
import init_dict
from letterize import letterize


word_anas = None
longest_word_len = 0


def load_dict():
    if init_dict.needs_updating():
        init_dict.init_dict()
    global word_anas, longest_word_len
    word_anas, longest_word_len = marshal.load(open('dict.dat', 'rb'))


def all_anagrams(string):
    for cut in range(1, min(longest_word_len, len(string)+1)):
        def anas(left, right):
            for initial_word in word_anas.get(letterize(left), []):
                if right == '':
                    yield [initial_word]
                else:
                    for right_anagram in all_anagrams(right):
                        yield [initial_word] + right_anagram
        for x in itertools.chain(anas(string[:cut], string[cut:]),
                                 anas(string[cut:], string[:cut])):
            yield x


if __name__ == '__main__':
    import sys
    string = ''.join(sys.argv[1:]).lower().replace(' ', '')
    load_dict()
    for ana in all_anagrams(string):
        print ' '.join(ana)


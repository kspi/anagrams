import re
import sys
import marshal
import os
import glob
from letterize import letterize


def whichever_exists(*fs):
    for f in fs:
        if os.path.exists(f):
            return f
    raise Exception('One of {!r} should exist.'.format(fs))


DICTIONARY_FILE = whichever_exists('dict', 'dict.txt', '/usr/share/dict/words')

SHORTWORDS = frozenset(['a', 'an', 'on', 'in', 'at', 'of', 'if', 'we', 'me', 'he', 'be', 'is'])

FORBIDDEN_SYMBOL = re.compile(r'[\WA-Z]')


def needs_updating():
    if not os.path.exists('dict.dat'):
        return True
    for other_f in [DICTIONARY_FILE] + glob.glob('*.py'):
        if os.path.getmtime(other_f) > os.path.getmtime('dict.dat'):
            return True
    return False


def init_dict(verbose=False):
    def log(s, newline=True):
        if verbose:
            if newline:
                print s
            else:
                print s,
                sys.stdout.flush()

    word_anas = dict()
    longest_word_len = 0
    words = 0
    anagram_classes = 0

    log('Loading words ...', newline=False)
    for line in open(DICTIONARY_FILE, 'r'):
        line = line.strip()
        if line != '' and (line in SHORTWORDS or len(line) > 2) and not FORBIDDEN_SYMBOL.search(line):
            words += 1
            letters = letterize(line)
            if letters in word_anas:
                word_anas[letters].append(line)
            else:
                word_anas[letters] = [line]
                anagram_classes += 1
            if len(letters) > longest_word_len:
                longest_word_len = len(letters)
    log('done.')

    log('Words: {words}\nAnagram classes: {anagram_classes}\nLongest word length: {longest_word_len}'.format(**locals()))

    log('Pickling ...', newline=False)
    marshal.dump((word_anas, longest_word_len), open('dict.dat', 'wb'))
    log('done.')


if __name__ == '__main__':
    init_dict(verbose=True)

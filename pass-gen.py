#!/usr/bin/env python
import argparse
import locale
import math
import random
import re

from collections import Counter

locale.setlocale(locale.LC_ALL, '')

def generate(words, how_many=4):
    return ' '.join([random.choice(words) for _ in range(how_many)])


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-w', '--word-file',
                        default='/usr/share/dict/words',
                        help='Path to word file (one word per line)')
    parser.add_argument('-m', '--min-word-length',
                        type=int,
                        default=2,
                        help='Do not use words shorter then this. Default: %(default)d)')
    parser.add_argument('-M', '--max-word-length',
                        type=int,
                        default=6,
                        help='Do not use words longer then this. Default: %(default)d)')
    parser.add_argument('-e', '--encoding',
                        default='utf-8',
                        help='Word file encoding. Default: %(default)s)')
    parser.add_argument('-F', '--word-filter',
                        default='^[a-z]+$',
                        help=('Allow only words that match this regular expression. '
                              'Default: %(default)s'))
    parser.add_argument('-s', '--attempt-rate',
                        default=10**8,
                        type=int,
                        help=('Assume this many brute force attemps per second when '
                              'calculating time to crack'
                              'Default: %(default)d'))
    parser.add_argument('-q', '--quantity',
                        default=4,
                        type=int,
                        help=('Number of words to include in password'
                              'Default: %(default)d'))


    return parser.parse_args()

def format_ttc(seconds):
    days = int(seconds/(60*60*24))
    if days < 365:
        return u'{:n}d'.format(days)
    else:
        return u'{:n}y'.format(int(days/365))

def calc_ttc(combination_count, attempt_rate):
    return combination_count/(2*attempt_rate)


def maybe_decode(thing, encoding):
    if hasattr(thing, 'decode'):
        return thing.decode(encoding)
    return thing


def main():
    args = get_args()
    char_counter = Counter()
    with open(args.word_file) as f:
        filter_re = re.compile(args.word_filter)
        words = [maybe_decode(word, args.encoding) for word
                 in (line.strip() for line in f)
                 if args.min_word_length <= len(word) <= args.max_word_length
                 and filter_re.match(word)]

        for word in words:
            char_counter.update(word)

        print(u'\nFound alphabet of {:n} characters:\n'.format(len(char_counter)))
        for k, v in sorted(char_counter.items()):
            print(u'{} {:>6n}'.format(k, v))

        word_count = len(words)
        print(u'\nFound {:n} words\n'.format(word_count))

        fmt = u'{:>3n} {:>3n} {:>8} {}'
        header = u'E1  E2  TTC      PASSWORD'
        print(header)
        print(u'-'*len(header))

        for k in range(1, args.quantity + 1):
            password = generate(words, how_many=k)
            combination_count = word_count**k
            ttc = calc_ttc(combination_count, args.attempt_rate)
            entropy = int(math.log(combination_count, 2))
            combination_count2 = len(char_counter)**len(password)
            ttc2 = calc_ttc(combination_count2, args.attempt_rate)
            entropy2 = int(math.log(combination_count2, 2))
            print(fmt.format(entropy, entropy2,
                             format_ttc(min(ttc, ttc2)), password))

    print(u'\nTime to crack calculation assumes {:n} attemps per second'
          .format(args.attempt_rate))



if __name__ == '__main__':
    main()

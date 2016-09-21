#!/usr/bin/env python

import random
import math
import argparse
import re

from collections import Counter

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
                        help='Do not use words shorter then this. Default: %(default)s)')
    parser.add_argument('-M', '--max-word-length',
                        type=int,
                        default=6,
                        help='Do not use words longer then this. Default: %(default)s)')
    parser.add_argument('-e', '--encoding',
                        default='utf-8',
                        help='Word file encoding. Default: %(default)s)')
    parser.add_argument('-F', '--word-filter',
                        default='^[a-z]+$',
                        help=('Allow only words that match this regular expression. '
                              'Default: %(default)s'))
    return parser.parse_args()


def main():
    args = get_args()
    char_counter = Counter()
    with open(args.word_file) as f:
        filter_re = re.compile(args.word_filter)
        words = [word.decode(args.encoding) for word
                 in (line.strip() for line in f)
                 if args.min_word_length <= len(word) <= args.max_word_length
                 and filter_re.match(word)]

        for word in words:
            char_counter.update(word)

        print u'Found alphabet of {} characters:'.format(len(char_counter))
        for k, v in sorted(char_counter.items()):
            print u'{} {}'.format(k, v)

        print ''
        word_count = len(words)

        print u'Found %d words' % word_count
        print ''

        fmt = u'{:>3} {:>3} {}'
        header = u'E1  E2  PASSWORD'
        print header
        print u'-'*len(header)

        for k in range(1, 6):
            password = generate(words, how_many=k)
            entropy = int(math.log(word_count**k, 2))
            entropy2 = int(math.log(len(char_counter)**len(password), 2))
            print fmt.format(entropy, entropy2, password)


if __name__ == '__main__':
    main()

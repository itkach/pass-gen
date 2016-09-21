#!/usr/bin/env python

import random
import math
import argparse

def generate(words, how_many=4):
    return ' '.join([random.choice(words) for _ in range(how_many)])


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-w', '--word-file',
                        default='/usr/share/dict/words',
                        help="Path to word file (one word per line)")
    parser.add_argument('-m', '--min-word-length',
                        type=int,
                        default=2,
                        help="Do not use words shorter then this. Default: %(default)s)")
    parser.add_argument('-M', '--max-word-length',
                        type=int,
                        default=6,
                        help="Do not use words longer then this. Default: %(default)s)")

    return parser.parse_args()


def main():
    args = get_args()

    with open(args.word_file) as f:
        words = [word for word in (line.strip() for line in f)
                 if args.min_word_length <= len(word) <= args.max_word_length
                 and not word[0].isupper()]

        word_count = len(words)

        print "Found %d words" % word_count

        for k in range(1, 6):
            passwd = generate(words, how_many=k)
            entropy = int(math.log(word_count**k, 2))
            print k, entropy, '\t', passwd


if __name__ == '__main__':
    main()

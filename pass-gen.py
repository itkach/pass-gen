#!/usr/bin/env python

import random
import math

def generate(words, how_many=4):
    return ' '.join([random.choice(words) for i in range(how_many)])


def main():
    with open('/usr/share/dict/words') as f:
        words = [word for word in (line.strip() for line in f) 
                 if 2 < len(word) < 6 and not word[0].isupper()]

        word_count = len(words)

        print "Found %d words" % word_count

        for k in range(1, 6):        
            passwd = generate(words, how_many=k)
            entropy = int(math.log(word_count**k, 2))
            print k, entropy, '\t', passwd

    
if __name__ == '__main__':
    main()

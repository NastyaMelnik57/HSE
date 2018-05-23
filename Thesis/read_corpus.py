
# coding: utf-8

import pickle
import re
import codecs

# read corpus line by line
lines = []
with codecs.open('ruwac-filtered.out','r',encoding='utf-8') as ruwac:
    for line in ruwac:
        try:
            line = line.strip()
            if line != '':
                words = line.split('\t')
                if len(words) > 2:
                    lines.append(words)
        except:
            pass

with open('ruwac_lines.pickle','wb') as f:
    pickle.dump(lines, f)



# coding: utf-8

# In[ ]:


# coding: utf-8

import sys
import gensim, logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import wget
model_url_rnc = 'http://rusvectores.org/static/models/rusvectores4/RNC/ruscorpora_upos_skipgram_300_5_2018'
modelfile_rnc = wget.download(model_url)
m = 'ruscorpora_upos_skipgram_300_5_2018.vec.gz'
if m.endswith('.vec.gz'):
    model_rnc = gensim.models.KeyedVectors.load_word2vec_format(m, binary=False)
elif m.endswith('.bin.gz'):
    model_rnc = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)
else:
    model_rnc = gensim.models.Word2Vec.load(m)

model_rnc.init_sims(replace=True)

with open('W2V_RNC.pickle','wb') as f:
    pickle.dump(model_rnc, f)


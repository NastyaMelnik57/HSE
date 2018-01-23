
# coding: utf-8

# In[6]:


def poly_hash(s, x=31, p=997):
    h = 0
    for j in range(len(s)-1, -1, -1):
        h = (h * x + ord(s[j]) + p) % p
    return h


# In[133]:


def search_rabin_multi(text, patterns):
            
    # precompute hashes
    x = 31
    p = 997
    
    if type(text) != str:
        raise BaseException('Wrong input')
    if type(patterns) != list:
        raise BaseException('Wrong input')
    else:
        for i in patterns:
            if type(i) != str:
                raise BaseException('Wrong input')
                
    indices = [[] for i in patterns]
    precomputed = [[] for i in patterns]
    for i in range(0, len(patterns)):
        if len(patterns[i]) != 0 and len(text) >= len(patterns[i]):
            precomputed_i = [0] * (len(text) - len(patterns[i]) + 1)
            precomputed_i[-1] = poly_hash(text[-len(patterns[i]):], x, p)
            factor = 1
            for j in range(len(patterns[i])):
                factor = (factor*x + p) % p
            for j in range(len(text) - len(patterns[i])-1, -1, -1):
                precomputed_i[j] = (precomputed_i[j+1] * x + ord(text[j]) - factor * ord(text[j+len(patterns[i])]) + p) % p

            pattern_hash_i = poly_hash(patterns[i], x, p)
            for j in range(len(precomputed_i)):
                if precomputed_i[j] == pattern_hash_i:
                    if text[j: j + len(patterns[i])] == patterns[i]:
                        indices[i].append(j)
    return indices


# In[134]:


search_rabin_multi('1', 123)


# In[129]:


from unittest import *

class SearchRabinMultiTest(TestCase):
    
    def test_error(self):
        text = 123
        text2 = '123'
        patterns = ['1', '2']
        patterns2 = [1, 2]
        self.assertRaises(search_rabin_multi(text, patterns), 'Wrong input')
        self.assertRaises(search_rabin_multi(text2, patterns2), 'Wrong input')
        
    def test_empty(self):
        text = ''
        text2 = 'whatever'
        patterns = []
        patterns2 = ['whatever', 'whatever2']
        self.assertEqual(len(search_rabin_multi(text, patterns)), 0)
        self.assertEqual(len(search_rabin_multi(text2, patterns)), 0)
        self.assertEqual(search_rabin_multi(text, patterns2), [[] for i in range(len(patterns2))])
        self.assertEqual(search_rabin_multi(text2, ['']), [[]])
        
    def test_big_pattern(self):
        text = 'blabla'
        patterns = ['blablabla']
        self.assertEqual(search_rabin_multi(text, patterns), [[]])
        
    def test_count(self):
        text = 'Betty Botter bought some butter,             But, she said, the butter’s bitter.             If I put it in my batter,             It will make my batter bitter.'
        patterns = ['tt', ' i', 'bitter.', 'tty']
        indices = [[2, 8, 27, 66, 75, 113, 149, 156], [101, 104], [73, 154], [2]]
        self.assertListEqual(search_rabin_multi(text, patterns), indices)
        
case = SearchRabinMultiTest()
suite = TestLoader().loadTestsFromModule(case)
TextTestRunner().run(suite)


# При количестве паттерном, равном одному, оценки сложности сверху была равна T + qP. 
# Теперь внешний цикл по n элементам (количество паттерном) и у каждого паттерна свой q_i.
# Поэтому оценка сложности сверху будет О(n*(T+сумма_по_i(q_i*P_i)))

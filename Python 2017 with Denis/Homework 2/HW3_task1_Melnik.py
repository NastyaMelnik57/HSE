
# coding: utf-8

# In[1]:


import pattern
from pattern.web import Wikipedia, plaintext
import string
import re
import nltk
from nltk import trigrams
from nltk import word_tokenize


# In[35]:


class WikiParser:
    def __init__(self):
        pass
    def get_articles(self, start):
        exclude = set(string.punctuation) - set('-')
        article = Wikipedia().article(start)
        links = article.links
        list_of_strings = []
        for link in links:
            linked_article = Wikipedia().article(link)
            if linked_article is not None:
                s = plaintext(linked_article.source)
                s = s.encode('ascii', 'ignore')
                s = s.lower()
                s = ''.join(ch for ch in s if ch not in exclude)
                s = ' '.join(re.split('\s+', s))
                list_of_strings.append(s)
        return list_of_strings


# In[13]:


class TextStatistics:
    def __init__(self, articles):
        self.list = articles
        pass
    
    def get_top_3grams(self, n):
        dict_trigrams = {}
        for article in self.list:
            article = ''.join([i for i in article if ((not i.isdigit()) and (i != '-'))])
            article_trigrams = list(trigrams(article))
            for article_trigram in article_trigrams:
                article_trigram_join = ''.join(article_trigram)
                if article_trigram_join in dict_trigrams:
                    dict_trigrams[article_trigram_join] += 1
                else:
                    dict_trigrams[article_trigram_join] = 1
            list_of_3grams_in_descending_order_by_freq = sorted(dict_trigrams, key=dict_trigrams.get)[-1:-1-n:-1]
            list_of_their_corresponding_freq = [dict_trigrams[x] for x in list_of_3grams_in_descending_order_by_freq]
        return (list_of_3grams_in_descending_order_by_freq, list_of_their_corresponding_freq)
    
    def get_top_words(self, n):
        dict_words = {}
        pos_articles = set(['a', 'an', 'the'])
        pos_prepositions = set(['aboard', 'about', 'above', 'across', 'afore', 'after', 'against', 'along', 'amid', 'amidst', 'among', 'amongst', 'around', 'as', 'aside', 'aslant', 'astride', 'at', 'athwart', 'atop', 'between', 'before', 'behind', 'below', 'beneath', 'beside', 'besides', 'between', 'betwixt', 'beyond', 'by', 'circa', 'despite','down', 'except', 'for', 'from', 'in', 'inside', 'into', 'like', 'near', 'neath', 'next', 'of', 'off', 'on', 'opposite', 'out', 'outside', 'over', 'per', 'through', 'till'', toward', 'towards', 'under', 'underneath', 'unlike', 'until', 'up', 'with', 'without'])
        for article in self.list:
            article = ''.join([i for i in article if ((not i.isdigit()) and (i != '-'))])
            article = ' '.join([i for i in re.split(' ', article) if ((not i in pos_articles) and (not i in pos_prepositions))])
            article_words = article.split()
            for article_word in article_words:
                if article_word in dict_words:
                    dict_words[article_word] += 1
                else:
                    dict_words[article_word] = 1
            list_of_words_in_descending_order_by_freq = sorted(dict_words, key=dict_words.get)[-1:-1-n:-1]
            list_of_their_corresponding_freq = [dict_words[x] for x in list_of_words_in_descending_order_by_freq]
        return (list_of_words_in_descending_order_by_freq, list_of_their_corresponding_freq)


# In[40]:


class Experiment:
    def show_results(self):
        exclude = set(string.punctuation) - set('-')
        parser = WikiParser()
        articles = parser.get_articles("Natural_language_processing")
        stat = TextStatistics(articles)
        top20_3grams = stat.get_top_3grams(20)
        top20_words = stat.get_top_words(20)
        print("top-20 3-gramms: ", top20_3grams)
        print("top-20 words: ", top20_words)
        NLP = Wikipedia().article("Natural_language_processing")
        NLP_parsed = plaintext(NLP.source).lower()
        NLP_parsed = ''.join(ch for ch in NLP_parsed if ch not in exclude)
        NLP_parsed = ' '.join(re.split('\s+', NLP_parsed))
        NLP_parsed.lower()
        statNLP = TextStatistics([NLP_parsed])
        top5_3grams_NLP = statNLP.get_top_3grams(5)
        top5_words_NLP = statNLP.get_top_words(5)
        print("top-5 3-gramms in 'Natural language processing' article and their frequencies: ", top5_3grams_NLP)
        print("top-5 words in 'Natural language processing' article and their frequencies: ", top5_words_NLP)


# In[41]:


exp = Experiment()
exp.show_results()


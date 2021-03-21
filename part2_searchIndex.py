from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords
import string
import re
from nltk.stem import PorterStemmer 
import numpy as np
from collections import defaultdict

def readIndexFile():
    index = {}
    f=open('indexFile.txt', 'r', encoding='utf-8');
    for line in f:
        line=line.rstrip()
        term, postings = line.split('|')    
        postings=postings.split(';')        
        postings=[x.split(':') for x in postings] 
        postings=[ [int(x[0]), map(int, x[1].split(','))] for x in postings ]    
        index[term]=postings
        
    f.close()
    return index
    
index = readIndexFile()

stopwords = stopwords.words('english') 

def preprocess(article):
    
    tokenized = []
    stemmer = PorterStemmer() 
    x = nltk.word_tokenize(article)                              #  Tokenize string to words
    x = [ch.lower() for ch in x if ch.isalpha() or ch == '.']    #  Lower case and drop non-alphabetical tokens

    # To store the cleaned article
    article_clean = []
    for word in x: # Go through every word in your tokenized article
        if (word not in stopwords_english and  # remove stopwords
            word not in string.punctuation):  # remove punctuation
            article_clean.append(word)
            
    # To store the stems
    article_stem = [] 
    for word in article_clean:
        stem_word = stemmer.stem(word)  # stemming word
        article_stem.append(stem_word)  # append to the list

    return article_stem 

def getPostings(words):
    return [index[word] for word in words]

def getIndexFromPostings(postings):
    return [[x[0] for x in p] for p in postings]

def WordQ(index, query):
    q = preprocess(query)
    p = index[q] #indx+loc
    idx = [x[0] for x in p] #indices
    result |= set(idx)

    result = list(result)
    #result.sort()
    print (' '.join(map(str,result)))
    return result

def PhraseQ(index, query):
    q = preprocess(query)
    if len(q)==0:
        print('No results')
        return

    result = set()    
    for word in q:
        p = index[word] #indx+loc
        idx = [x[0] for x in p] #indices
        result |= set(idx)
                
    result = list(result)
    #result.sort()
    print (' '.join(map(str,result)))
    return result
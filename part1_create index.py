import nltk
import pandas as pd
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords
import string
import re
from nltk.stem import PorterStemmer 
import numpy as np
from collections import defaultdict

stopwords_english = stopwords.words('english') 

df1 = pd.read_csv("articles1.csv").head(10000)
df2 = pd.read_csv("articles2.csv").head(10000)
df3 = pd.read_csv("articles3.csv").head(10000)

# unique identifiers:
id1 = df1['id'].tolist()
id2 = df2['id'].tolist()
id3 = df3['id'].tolist()
id_tot = id1 + id2 + id3

# content:
cont1 = df1['content'].tolist()
cont2 = df2['content'].tolist()
cont3 = df3['content'].tolist()
cont_tot = cont1 + cont1 + cont1

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

def word2doc(id_tot,cont_tot):
    word2doc = {}
    for cont_id, content in enumerate(cont_tot):
        prep_file = preprocess(content)
        for indx, word in enumerate(prep_file):
            nested_list = [cont_id]
            nested_list.append([indx])
            try:
                if word2doc[word][-1][0] == id_tot[cont_id]:
                    old_list = word2doc[word]
                    word2doc[word][-1][1] += [indx]
                else:
                    word2doc[word].append([id_tot[cont_id],[indx]])
            except:
                word2doc[word] = [[id_tot[cont_id],[indx]]]
    return word2doc


word2doc2 = word2doc(id_tot, cont_tot)

def saveIndexToFile(vocabulary):
    '''write the inverted index to the file'''
    f = open("indexFile.txt","w", encoding='utf-8')
    for word in vocabulary.keys():
        postinglist=[]
        for p in vocabulary[word]:
            idx = p[0]
            positions = p[1]
            postinglist.append(':'.join([str(idx) ,','.join(map(str,positions))]))
        postingData=';'.join(postinglist)
        #tfData=','.join(map(str,tf[term]))
        #idfData='%.4f' % (numDocuments/df[term])
        #f.write('|'.join((term, postingData, tfData, idfData)))
        f.write(''.join((word,'|',';'.join(postinglist))))
        f.write('\n')
    f.close()
    
saveIndexToFile(word2doc2)   

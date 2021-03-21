# +
import pandas as pd
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords
import string
import re
from porterStemmer import PorterStemmer
import json

stopwords_english = stopwords.words('english') 

df1 = pd.read_csv("articles1.csv").head(41000)
df2 = pd.read_csv("articles2.csv").head(41000)
df3 = pd.read_csv("articles3.csv").head(41000)


# unique identifiers:
id1 = df1['id'].tolist()
id2 = df2['id'].tolist()
id3 = df3['id'].tolist()
id_tot = id1+id2+id3

# content:
cont1 = df1['content'].tolist()
cont2 = df2['content'].tolist()
cont3 = df3['content'].tolist()
cont_tot = cont1+cont1+cont1

porter = PorterStemmer()
def preprocess(content):
    out = re.sub(r'[^a-zA-Z ]','',content)
    out = word_tokenize(out)
    out = [ch.lower() for ch in out if ch.isalpha() or ch == '.']
    
    out = [word for word in out if word not in stopwords_english and word not in string.punctuation]
    out = [porter.stem(word, 0, len(word)-1) for word in out]
    return out


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

def writeIndexToFile(vocabulary):
    '''write the inverted index to the file'''
    f = open("indexFile.txt","w", encoding='utf-8')
    i = 1
    for word in vocabulary.keys():
        postinglist=[]
        for p in vocabulary[word]:
            idx = p[0]
            positions = p[1]
            postinglist.append(':'.join([str(idx) ,','.join(map(str,positions))]))
        f.write(''.join((word,'|',';'.join(postinglist))))
        f.write('\n')
        
        print(f"{i}/{len(vocabulary)}")
        i=i+1
    f.close()
    
writeIndexToFile(word2doc2)    


def readIndex():
    index = {}
    f=open('indexFile.txt', 'r', encoding='utf-8');
    for line in f:
        line=line.rstrip()
        term, postings = line.split('|')    #term='termID', postings='docID1:pos1,pos2;docID2:pos1,pos2'
        postings=postings.split(';')        #postings=['docId1:pos1,pos2','docID2:pos1,pos2']
        postings=[x.split(':') for x in postings] #postings=[['docId1', 'pos1,pos2'], ['docID2', 'pos1,pos2']]
        postings=[ [int(x[0]), map(int, x[1].split(','))] for x in postings ]   #final postings list  
        index[term]=postings
    f.close()
    return index
    
index = readIndex()



# def ftq(word2doc2, query):
#     q = preprocess(query)
#     print(q)
#     if len(q)==0:
#         print('No results')
#         return

#     result = set()
#     freqs = []
    
#     for word in q:
#         p = word2doc2[word] #indx+loc
#         idx = [x[0] for x in p] #indices
#         result |= set(idx)
        
#         freq = [len(x[1]) for x in p] # frequency
#         freqs += freq
#         if word not in q:
#             pass
#         break
        
#     result = list(result)
#     #result.sort()
#     print (' '.join(map(str,result)))
#     print('Its frequency: \n')
#     print (' '.join(map(str,freqs)))
    

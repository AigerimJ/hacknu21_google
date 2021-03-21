import json 
from porterStemmer import PorterStemmer
from nltk.tokenize import word_tokenize
import string
from nltk.corpus import stopwords
import argparse

parser = argparse.ArgumentParser(description='Tokenizer.')
parser.add_argument('query',action='store', type=str, help='path to pretraining dataset')
#parser.add_argument('model_path',action='store', type=str, help='path where to save model')


args = parser.parse_args()


stopwords_english = stopwords.words('english') 


# Opening JSON file 
with open('word2indexsmall.json') as json_file: 
    data = json.load(json_file) 
    
    
    
porter = PorterStemmer()
def preprocess(content):
    import re 
    out = re.sub(r'[^a-z0-9 ]','',content)
    out = content.lower()
    out = word_tokenize(out)
    
    out = [word for word in out if word not in stopwords_english and word not in string.punctuation]
    out = [porter.stem(word, 0, len(word)-1) for word in out]
    return out


term=args.query
# term="Olympic"
print(term)
term = preprocess(term)

try:
    docs=[posting[0] for posting in data[term[0]]]
    print(docs)
except:
    #term is not in index
    docs=[]
    print(docs)

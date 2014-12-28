# -*- coding: utf-8 -*-

from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer, HashingVectorizer, CountVectorizer
import numpy as np

def get_stop_words():
    stop_words = set(['all', 'six', 'less', 'being', 'indeed', 'over', 'move', 'anyway', 'four', 'not', 'own', 'through', 'yourselves', 'fify', 'where', 'mill', 'only', 'find', 'before', 'one', 'whose', 'system', 'how', 'somewhere', 'with', 'thick', 'show', 'had', 'enough', 'should', 'to', 'must', 'whom', 'seeming', 'under', 'ours', 'has', 'might', 'thereafter', 'latterly', 'do', 'them', 'his', 'around', 'than', 'get', 'very', 'de', 'none', 'cannot', 'every', 'whether', 'they', 'front', 'during', 'thus', 'now', 'him', 'nor', 'name', 'several', 'hereafter', 'always', 'who', 'cry', 'whither', 'this', 'someone', 'either', 'each', 'become', 'thereupon', 'sometime', 'side', 'two', 'therein', 'twelve', 'because', 'often', 'ten', 'our', 'eg', 'some', 'back', 'up', 'go', 'namely', 'towards', 'are', 'further', 'beyond', 'ourselves', 'yet', 'out', 'even', 'will', 'what', 'still', 'for', 'bottom', 'mine', 'since', 'please', 'forty', 'per', 'its', 'everything', 'behind', 'un', 'above', 'between', 'it', 'neither', 'seemed', 'ever', 'across', 'she', 'somehow', 'be', 'we', 'full', 'never', 'sixty', 'however', 'here', 'otherwise', 'were', 'whereupon', 'nowhere', 'although', 'found', 'alone', 're', 'along', 'fifteen', 'by', 'both', 'about', 'last', 'would', 'anything', 'via', 'many', 'could', 'thence', 'put', 'against', 'keep', 'etc', 'amount', 'became', 'ltd', 'hence', 'onto', 'or', 'con', 'among', 'already', 'co', 'afterwards', 'formerly', 'within', 'seems', 'into', 'others', 'while', 'whatever', 'except', 'down', 'hers', 'everyone', 'done', 'least', 'another', 'whoever', 'moreover', 'couldnt', 'throughout', 'anyhow', 'yourself', 'three', 'from', 'her', 'few', 'together', 'top', 'there', 'due', 'been', 'next', 'anyone', 'eleven', 'much', 'call', 'therefore', 'interest', 'then', 'thru', 'themselves', 'hundred', 'was', 'sincere', 'empty', 'more', 'himself', 'elsewhere', 'mostly', 'on', 'fire', 'am', 'becoming', 'hereby', 'amongst', 'else', 'part', 'everywhere', 'too', 'herself', 'former', 'those', 'he', 'me', 'myself', 'made', 'twenty', 'these', 'bill', 'cant', 'us', 'until', 'besides', 'nevertheless', 'below', 'anywhere', 'nine', 'can', 'of', 'your', 'toward', 'my', 'something', 'and', 'whereafter', 'whenever', 'give', 'almost', 'wherever', 'is', 'describe', 'beforehand', 'herein', 'an', 'as', 'itself', 'at', 'have', 'in', 'seem', 'whence', 'ie', 'any', 'fill', 'again', 'hasnt', 'inc', 'thereby', 'thin', 'no', 'perhaps', 'latter', 'meanwhile', 'when', 'detail', 'same', 'wherein', 'beside', 'also', 'that', 'other', 'take', 'which', 'becomes', 'you', 'if', 'nobody', 'see', 'though', 'may', 'after', 'upon', 'most', 'hereupon', 'eight', 'but', 'serious', 'nothing', 'such', 'why', 'a', 'off', 'whereby', 'third', 'i', 'whole', 'noone', 'sometimes', 'well', 'amoungst', 'yours', 'their', 'rather', 'without', 'so', 'five', 'the', 'first', 'whereas', 'once'])
    return stop_words


from sklearn.datasets import fetch_20newsgroups
news = fetch_20newsgroups(subset='all')
print type(news.data), type(news.target), type(news.target_names)
print news.target_names
print len(news.data)
print len(news.target)
#print news.data[0]
#print news.target[0], news.target_names[news.target[0]]
ALPHA = 1

if __name__ == '__main__':
    
    stop_words = get_stop_words()
    
    '''        
    clf_7 = Pipeline([
            ('vect', TfidfVectorizer(
                        stop_words=stop_words,
                        token_pattern=ur"\b[a-z0-9_\-\.]+[a-z][a-z0-9_\-\.]+\b",         
            )),
            ('clf', MultinomialNB(alpha=0.01)),
        ]) 
    
    clf_7.fit(news.data, news.target)
    for d in news.data[0:10]:
        print d
        print '--------------'
    '''
    
    clf = MultinomialNB(alpha=ALPHA)
    cv = CountVectorizer(stop_words=stop_words, min_df=2)
    cv = CountVectorizer()
    #import pdb
    #pdb.set_trace()
    x1 = cv.fit_transform(news.data[0:10]).toarray()
    y1 = news.target[0:10]
    
    x2 = cv.fit_transform(news.data[11:20]).toarray()
    y2 = news.target[11:20]
    
    x3 = cv.fit_transform(news.data[21:30]).toarray()
    y3 = news.target[21:30]
    #print X
    #print y1, y2
    #print cv.get_feature_names()
    #print news.target[0:10]
    #print news.target[0:5]
    #print news.target[5:10]
    print np.unique(news.target[0:30])
    
    clf.partial_fit(x1, y1, classes=np.unique(news.target[0:30]))
    clf.partial_fit(x2, y2)
    clf.partial_fit(x3, y3)
    
    
    
    
        
    
    print 'Done'
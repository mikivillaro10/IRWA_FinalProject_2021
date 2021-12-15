from collections import defaultdict
from array import array
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import numpy as np
import collections
import emoji
from numpy import linalg as la
import string
import re
import pandas as pd
from gensim.models.word2vec import Word2Vec

def process_word(word, stop_words):
    """
    Preprocess each word of the tweet getting rid of URLs, punctuation sings and stop words
    
    Argument:
    word -- string (text) to be preprocessed
    stop_words -- list of stop words to get rid of
    
    Returns:
    word - the resulting processed word. False in case we don't want that word
    """
    
# Eliminate URLs
    word = re.sub(r'http\S+', '', word) 

# Eliminate ampersands
    word = re.sub(r'&\S+', '', word) 

    if not word:
        return False

# Get rid of punctuation marks except "#" and "@"
    if word[0] == '#':
        word = '#' + word.translate(str.maketrans('', '', string.punctuation)) 
        return word

    elif word[0] == '@':
        word = '@' + word.translate(str.maketrans('', '', string.punctuation)) 
        return word
    
    elif '¿' in word:
        word = word.replace('¿', '')
    
    else:
        word = word.translate(str.maketrans('', '', string.punctuation))

# Get rid of strings like '-'
    if len(word) <= 1 and not word.isdigit(): 
        return False
    
# Eliminate the stopwords 
    elif word not in stop_words: 
        return word

    
def build_terms(line):
    """
    Preprocess the tweet text calling the process_word function, stemming,
    transforming in lowercase and return the tokens of the text.
    
    Argument:
    line -- string (text) to be preprocessed
    
    Returns:
    line - a list of tokens corresponding to the input text after the preprocessing
    """

    stemmer = PorterStemmer()
    
    stop_words = set()
    for lang in stopwords.fileids():
         stop_words |= set(stopwords.words(lang))
            
    line = emoji.get_emoji_regexp().sub("", line)
    
    line= line.lower()## Transform in lowercase
    line= line.split() ## Tokenize the text to get a list of terms
    templine=[]
    for word in line:      
        word = process_word(word, stop_words)
        if word:
            templine.append(word)
            
    line= templine
    line= [stemmer.stem(word) for word in line] ## perform stemming
    return line


def create_index(tweets, X):
    """
    Implement the inverted index
    
    Argument:
    lines -- collection of tweets
    
    Returns:
    index - the inverted index (implemented through a Python dictionary) containing terms as keys and the corresponding
    list of tweets where these keys appears in (and the positions) as values.
    """
    index = defaultdict(list)
    num_tweets = len(tweets)
    
    tweet2vec = defaultdict(list)
    
    for tweet in tweets:
        line = tweets[tweet]['full_text']
        line_arr = line.replace("\n", ' ')
        tweet_id = tweet
        terms = build_terms(''.join(line_arr))
        
        if len(terms) == 0:
            continue
        
        tweet2vec[tweet] = np.array([0.0]*len(X[terms[0]]))
        
        for term in terms:
            tweet2vec[tweet] += np.array(X[term])
        
        tweet2vec[tweet] = tweet2vec[tweet] / len(terms)
        
        current_tweet_index = {}

        for position, term in enumerate(terms):  
            try:
                current_tweet_index[term][1].append(position)
            except:
                current_tweet_index[term]=[tweet_id, array('I',[position])] 


        for term_page, posting_page in current_tweet_index.items():
            index[term_page].append(posting_page)


    return index, tweet2vec
    
    
def load_index(tweets):

    clean_tweets = {}
    for tweet in tweets:
        line = tweets[tweet]['full_text']
        line_arr = line.replace("\n", ' ')
        terms = build_terms(''.join(line_arr))
        clean_tweets[tweet] = terms
        
    sentences = clean_tweets.values()

    model = Word2Vec(sentences, workers=4, min_count=1, window=10, sample=1e-5)

    index, tweet2vec = create_index(tweets, model.wv)
	
    return index, tweet2vec, model
	
	
	
	

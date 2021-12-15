
from myapp.core.index import build_terms
import numpy as np

from myapp.search.objects import ResultItem, Document


def check_index(word, index): 
    if word in index:
        return index[word]
    else:
        return []

def search_in_corpus(query, tweets, search_id, corpus, index, tweet2vec, model):    
    
    
    query_words = build_terms(query) # Separate query by preprocessed terms
    
    docs = {}
    for word in query_words: # Save the documents in which query terms appear
        docs[word] = [val[0] for val in check_index(word, index)]
        if len(docs[word]) == 0:
            return ""
    
    doc_list = list(docs.values())
    final_doc_list = doc_list[0]
    for list_ in doc_list:
        final_doc_list = list(set(final_doc_list) & set(list_))
     
    # 2. apply ranking
    """
    Perform the ranking of the results of a search based on the tf-idf weights
    
    Argument:
    query -- list of query terms
    tweets -- list of tweets, to rank, matching the query
    index -- inverted index data structure
    
    Returns:
    Print the list of ranked tweets
    """
    
    terms = query_words
    
    # We will first have to compute each query as a normalized vector of words
    X = model.wv
    query_vector = np.array([0.0]*len(X[terms[0]])) # Create the query vector
    
    for word in terms:
        query_vector += np.array(X[word]) # Add the words
    
    query_vector = query_vector/len(terms) # Normalize
    
    
    tweet_scores=[ [np.dot(curtweetVec, query_vector), tweet] for tweet, curtweetVec in tweet2vec.items() ]
    tweet_scores.sort(reverse=True) # Compute and sort by scores

    result_tweets = [x[1] for x in tweet_scores] # Return the top ranked tweets of the query
    scores = [x[0] for x in tweet_scores]    
    
    if len(result_tweets) == 0:
        print("No results found, try again")
        return False

    
    res = []
    size = len(corpus)
    ll = list(corpus.values())
    aux = 0
    for i in result_tweets:
        item: Document = ll[int(i)]
        res.append(ResultItem(item.id, item.title, item.description, item.doc_date,
                              "doc_details?id={}&search_id={}&param2=2".format(item.id, search_id), scores[aux]))
    aux += 1

    # for index, item in enumerate(corpus['Id']):
    #     # DF columns: 'Id' 'Tweet' 'Username' 'Date' 'Hashtags' 'Likes' 'Retweets' 'Url' 'Language'
    #     res.append(DocumentInfo(item.Id, item.Tweet, item.Tweet, item.Date,
    #                             "doc_details?id={}&search_id={}&param2=2".format(item.Id, search_id), random.random()))

    # simulate sort by ranking
    res.sort(key=lambda doc: doc.ranking, reverse=True)
    return res
    

#    return ""

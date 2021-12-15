import json
import random


class AnalyticsData:
    """
    An in memory persistence object.
    Declare more variables to hold analytics tables.
    """
    # statistics table 1
    # fact_clicks is a dictionary with the click counters: key = doc id | value = click counter
    fact_clicks = dict([])

    # List of queries the user has made
    searched_queries = []

    # Docs the user has clicked for each query
    query2doc = dict([])

    # Query that has led to each doc
    doc2query = dict([])

    def save_query_terms(self, terms: str) -> int:
        print(self)
        self.searched_queries.append(terms)
        self.current_query = terms
        return random.randint(0, 100000)
    
    def add_doc(self, doc_id, query):
        if query in self.query2doc:
            self.query2doc[query].append(doc_id)
        else:
            self.query2doc[query] = [doc_id]
            
        if doc_id in self.doc2query:
            if query not in self.doc2query[doc_id]: 
                self.doc2query[doc_id].append(query)
        else:
            self.doc2query[doc_id] = [query]
            
            
        return
        
    def __str__(self):
        print("SEARCHED QUERIES:\n", self.searched_queries)
        print("DOCS CLICKED PER QUERY:\n", self.query2doc)
        return ""


class ClickedDoc:
    def __init__(self, doc_id, description, counter):
        self.doc_id = doc_id
        self.description = description
        self.counter = counter

    def to_json(self):
        return self.__dict__

    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)
        
            
class ActiveUser:
    ip = ""
    userAgent = ""
    
    def trackUser(self, ip_, userAgent_):
        self.ip = ip_
        self.userAgent = userAgent_
        
        
        
        
    
    
    
    

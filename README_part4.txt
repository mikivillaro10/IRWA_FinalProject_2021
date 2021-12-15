README
This file includes step by step instructions about how to run the code and how to select the different functions, algorithms and/or other options to run the ranking scores.
This code has to be downloaded and imported in any python-supported platform (this was created using Pycharm, as a reference) together with the file to be analysed “dataset_tweets_WHO.json” (also included as a .txt file in the inputs folder).




Important: 


The ZIP file contains a more specific README regarding the main configurations when running the main program (such as the environment, needed packages, etc.) and how to actually run it. Note that there is one more package to be installed called “emoji”.


In the “main” function (web_app.py), we can find the main parameters (which can also be changed according to the device’s specifications), such as the port in which the page is launched (8088 by default), the host’s IP address (by default 0.0.0.0)...


The file “web_app.py” contains the main functions which configure the main interface.
The file “analytics_data.py” contains the classes that define the data that we intend to collect from searchers (users) and their behavior as, for example, the number of clicks. It also contains a class named User that collects the queries searched by the user, the IP, the OS, etc.
The file “index.py” is a file that contains the necessary functions to create and load the index used for the documents’ ranking.
The file “algorithms.py” mainly contains the function “search_in_corpus”, used to search within the tweets’ dataset given a query, the model, etc.
The file “load_corpus.py” has the functions necessary to obtain the dataframe of tweets used as the “searched” engine.
The file “objects.py” contains the classes Document, StatsDocument and ResultItem, referring to the tweets, their interaction statistics and the search’s results.
The file “search_engine.py” represents, as its name states, the class which calls the search function which activates the rest of the classes.


The code which creates and benchmarks the indexes corresponding to the given dataset makes it so that, if a search in the index is wanted, only numbers, letters and characters # and @ are allowed.
The “rank_tweets” function classifies documents in a word2vec way and returns a ranked list of them.


Any other classes, functions and/or displays are commented and explained in the code itself




Remarks:
The first search made takes some time to load (around 90 seconds approximately), as the index is created.
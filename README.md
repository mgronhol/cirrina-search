cirrina-search
==============


What is a minimum span text search?
============

A way to characterise the relevance of a search result is the span in which the search terms are found.
Large span means that the search terms are scattered sparsely around that spot and there is a high 
probability that the search result isn't very relevant or useful.

Minimum span text search tries to find such combination of found search terms that it minimises the span that
covers all of them. This increases the meaningfulness of the results (except in some pathological cases).


Why should I use it?
============

Usually full text search results are just occurences of search terms (perhaps agumented with some score 
that depends on was the hit a whole word or just a part of it). Especially when the search terms are a bit vague
or the subject that the user is looking for doesn't have very specific vocabulary associated with it the simple search
term matching doesn't provide the results as accurately as needed. 

When searching with multiple search terms, it comes more pronouced that the system should rank the results in a meaningful
and preferably well-defined way. Minimum span text search provides a way to enhance the search results so that the results 
are more useful to the user.


Example
============

    from Cirrina import Cirrina
    
    text = read_from_file(....)
    
    # Parse text into a searchable corpus
    search = Cirrina( text )
    
    # search for a minimum span that contains all given search terms
    result = search( search_terms )
    
    # Show results
    lines = text.splitlines()
    print lines[ result[0] : result[1] + 1 ]



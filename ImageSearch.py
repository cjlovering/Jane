from py_ms_cognitive import PyMsCognitiveImageSearch 
from random import randint


def getURL (search_term):
    search_service = PyMsCognitiveImageSearch('5a41108e4cee4b4297e3887cff817ab3' , search_term)
    res = randint(0,20) 
    first_fifty_result = search_service.search(limit=50, format='json') #1-50
    return first_fifty_result[res].content_url



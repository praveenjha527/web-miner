# Create your views here.
from webMiner.search_index import search
from django.shortcuts import render_to_response
from django.template import RequestContext,Context
def searcher(request):
    result=search(request.GET['q'])
    query_string=''
    
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
    
        

        

    return render_to_response('search_results.html',
                          { 'query_string': query_string, 'result': result 
						  },
                          context_instance=RequestContext(request))

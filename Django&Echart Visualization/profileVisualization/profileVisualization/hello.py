from django.http import HttpResponse
from django.shortcuts import render

def hello(request):
    #return HttpResponse("Hello world ! ")
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'hello.html', context)

def goodbye(request):
    #return HttpResponse("Hello world ! ")
    print "goodbye",request.GET['id']
    context = {}
    context['hello'] = 'Goodbye!'
    context['candidates_list'] = ['a','b','c']
    #return render(request, 'hello.html', context)
    return HttpResponse("Goodbye!")
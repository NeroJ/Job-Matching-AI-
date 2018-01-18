# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response
from Model.linkedinModels import Skills,Profile

# 表单
def search_form(request):
    return render_to_response('hello.html')

# 接收请求数据
def search(request):
    request.encoding='utf-8'
    if 'q' in request.GET and 'f' in request.GET:
        message = 'You search people with ' + request.GET['f'] + ':' + request.GET['q']
    else:
        message = u'你提交了空表单'
    return HttpResponse(message)


from django.shortcuts import render
from django.views.decorators import csrf


# 接收POST请求数据
def search_post(request):
    ctx = {}
    if request.POST:
        ctx['field'] = request.POST['f']
        ctx['query'] = request.POST['q']
        ctx['candidates_list'] = Profile.objects.filter(skills__skill_name__icontains=request.POST['q']).distinct()
    return render(request, "hello.html", ctx)
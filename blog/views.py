from django.views.generic import TemplateView
from .models import Article, Ine
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.http.response import JsonResponse
import json 
import urllib.request

class index(TemplateView):
    template_name = "blog/index.html" 

def new(request):
    template_name = "blog/new.html"
    if request.method == "POST":
        article = Article.objects.create(title = request.POST["title"], text = request.POST["text"])
        return redirect(view_article, article.pk)
    return render(request, template_name)

def article_all(request):
    template_name = "blog/article_all.html"
    context = {"articles":Article.objects.all()}
    return render(request, template_name, context)

def view_article(request, pk):
    template_name = "blog/view_article.html"
    try:
        article = Article.objects.get(pk=pk)

        #JSON 下のurlにアクセスして読み込み(pkで各記事毎にいいね数取得)
        url = "http://localhost:8000/article/{}/ine_ajax/".format(pk)
        res = urllib.request.urlopen(url)
        ine = json.loads(res.read().decode('utf-8'))

    except Article.DoesNotExist:
        raise Http404
    context = {"article":article, "ine":ine}
    return render(request, template_name, context)

def edit(request,pk):
    template_name = "blog/edit.html"
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        raise Http404
    if request.method == "POST":
        article.title = request.POST["title"]
        article.text = request.POST["text"]
        article.save()
        return redirect(view_article, pk)
    context = {"article": article}
    return render(request, template_name, context)

def delete(request, pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        raise Http404
    article.delete()
    return redirect(article_all)

def add_ine(request, pk):
    
    post = get_object_or_404(Article, pk=pk)
    ip_address = get_client_ip(request)
    ips = [ine.ip_address for ine in Ine.objects.filter(parent=post).all()]

    if ip_address in ips:
        msg = '登録済みです'
    else:
        ine = Ine.objects.create(ip_address=ip_address, parent=post)
        ine.save()
        msg = '登録しました'
    d = {
        'count': Ine.objects.filter(parent=post).count(),
        'msg': msg,
    }
    return JsonResponse(d)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

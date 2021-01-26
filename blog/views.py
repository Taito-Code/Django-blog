from django.views.generic import TemplateView
from . import models
from django.shortcuts import render, redirect
from django.http import Http404 

class index(TemplateView):
    template_name = "blog/index.html" 

def new(request):
    template_name = "blog/new.html"
    if request.method == "POST":
        article = models.Article.objects.create(title = request.POST["title"], text = request.POST["text"])
        return redirect(view_article, article.pk)
    return render(request, template_name)

def article_all(request):
    template_name = "blog/article_all.html"
    context = {"articles":models.Article.objects.all()}
    return render(request, template_name, context)

def view_article(request, pk):
    template_name = "blog/view_article.html"
    try:
        article = models.Article.objects.get(pk=pk)
    except models.Article.DoesNotExist:
        raise Http404
    context = {"article":article}
    return render(request, template_name, context)

def edit(request,pk):
    template_name = "blog/edit.html"
    try:
        article = models.Article.objects.get(pk=pk)
    except models.Article.DoesNotExist:
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
        article = models.Article.objects.get(pk=pk)
    except models.Article.DoesNotExist:
        raise Http404
    article.delete()
    return redirect(article_all)

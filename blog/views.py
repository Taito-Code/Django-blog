from django.views.generic import TemplateView
from .models import Article, Ine, Comment
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.http.response import JsonResponse
import json 
import urllib.request
from .forms import ArticleForm
from django.contrib.auth.decorators import login_required

#index表示
def index(request):
    template_name = "blog/index.html"
    context = {"articles":Article.objects.all().order_by('-posted_at')}
    return render(request, template_name, context)

#technology-blogのみ表示
def tech_all(request):
    template_name = "blog/article_tech.html"
    context = {"articles":Article.objects.filter(tags__name__in=["Technology",]).order_by('-posted_at')}
    return render(request, template_name, context)

#daily-blogのみ表示
def life_all(request):
    template_name = "blog/article_life.html"
    context = {"articles":Article.objects.filter(tags__name__in=["Life",]).order_by('-posted_at')}
    return render(request, template_name, context)

#aboutページを表示
def about(request):
    template_name = "blog/about.html"
    return render(request, template_name)

#contactページを表示
def contact(request):
    template_name = "blog/contact.html"
    return render(request, template_name)

#privacypolicyを表示
def privacypolicy(request):
    template_name = "blog/privacypolicy.html"
    return render(request, template_name)

#新規作成
@login_required
def new(request):
    template_name = "blog/new.html"
    if request.method == "POST":
        form = ArticleForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(article_all)

    else:
        form = ArticleForm
    return render(request, template_name, {'form': form })

#管理者ページ
@login_required
def article_all(request):
    template_name = "blog/article_all.html"
    context = {"articles":Article.objects.all()}
    return render(request, template_name, context)

#記事を閲覧
def view_article(request, pk):
    template_name = "blog/view_article.html"
    try:
        article = Article.objects.get(pk=pk)
        post = get_object_or_404(Article, pk=pk)
        post.pv += 1
        ine = Ine.objects.filter(parent=post).count()
        post.save()

    except Article.DoesNotExist:
        raise Http404
    
    if request.method == "POST":
        # データベースに投稿されたコメントを保存
        Comment.objects.create(text=request.POST["text"], article=article) 
    context = {"article":article, "ine":ine}
    return render(request, template_name, context)

#編集ページ
@login_required
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

#記事削除
@login_required
def delete(request, pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        raise Http404
    article.delete()
    return redirect(article_all)

#いいね関数
def add_ine(request, pk):
    
    post = get_object_or_404(Article, pk=pk) #Articleの受け取り
    ip_address = get_client_ip(request) #IPアドレスをget_client_ip()で取得
    ips = [ine.ip_address for ine in Ine.objects.filter(parent=post).all()]

    #IPアドレスが未登録の場合はDBに登録
    if ip_address in ips:
        msg = '登録済みです'
    else:
        ine = Ine.objects.create(ip_address=ip_address, parent=post)
        ine.save()
        msg = '登録しました'

    #Json形式にして格納
    d = {
        'count': Ine.objects.filter(parent=post).count(),
        'msg': msg,
    }
    return JsonResponse(d)

#IPアドレスを取得
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

from django.db.models import Exists, OuterRef
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, FormView, DetailView, DeleteView
from django.contrib import messages
from .models import Article, LikeArticle
from .forms import ArticleForm
from comments.forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Count
from comments.models import LikeComment


@method_decorator(login_required, name="dispatch")
class ArticleIndexView(ListView):
    model = Article
    template_name = "articles/index.html"

    def get_queryset(self):
        return Article.objects.annotate(like_count=Count("article"))


@method_decorator(login_required, name="dispatch")
class NewView(FormView):
    def get(self, request):
        form = ArticleForm()
        return render(request, "articles/new.html", {"form": form})

    def post(self, request):
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = self.request.user
            article.save()
            return redirect("articles:index")
        return render(request, "articles/new.html", {"form": form})


@method_decorator(login_required, name="dispatch")
class ShowView(DetailView):
    model = Article
    extra_context = {"comment_form": CommentForm()}

    def get_queryset(self):
        like_subquery = LikeArticle.objects.filter(
            like_by_article_id=self.request.user.id, like_article_id=OuterRef("pk")
        )
        return Article.objects.annotate(is_like=Exists(like_subquery))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        like_comment_subquery = LikeComment.objects.filter(
            like_by_id=self.request.user.id, like_comment_id=OuterRef("pk")
        ).values("pk")
        comments_with_likes = self.object.comments.annotate(
            is_like=Exists(like_comment_subquery)
        )
        context["comments"] = comments_with_likes

        return context

    def post(self, request, pk):
        article = self.get_object()
        form = CommentForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "更新成功")
        return redirect("articles:show", pk=article.id)


@login_required
@require_POST
def create(request):
    form = ArticleForm(request.POST)

    if form.is_valid():
        form.save()
        messages.success(request, "文章新增成功")
    return redirect("articles:index")


@login_required
def edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    form = ArticleForm(instance=article)
    return render(request, "articles/edit.html", {"article": article, "form": form})


class DeleteView(DeleteView):
    model = Article

    def get_success_url(self):
        messages.success(self.request, "已刪除")
        return reverse("articles:index")


@login_required
@require_POST
def add_like(req, pk):
    LikeArticle.objects.create(like_by_article_id=req.user.id, like_article_id=int(pk))
    return HttpResponse("")


@login_required
@require_POST
def remove_like(req, pk):
    try:
        like = LikeArticle.objects.get(
            like_by_article_id=req.user.id, like_article_id=pk
        )
        like.delete()
    except:
        pass
    return HttpResponse("")

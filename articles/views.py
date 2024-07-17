from django.db.models import Exists, OuterRef, Count, Prefetch
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView, FormView, DetailView, DeleteView, UpdateView
from .models import Article, LikeArticle
from .forms import ArticleForm
from comments.forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from comments.models import LikeComment
from boards.models import Category
from .models import Category
from django.http import Http404


@method_decorator(login_required, name="dispatch")
class ArticleIndexView(ListView):
    model = Article
    template_name = "articles/index.html"

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        sort = self.request.GET.get("sort", "最新")

        if sort == "熱門":
            return (
                Article.objects.with_count()
                .filter(category_id=category_id)
                .annotate(like_count=Count("like_article", distinct=True))
                .order_by("-like_count")
            )
        else:
            return (
                Article.objects.with_count()
                .filter(category_id=category_id)
                .annotate(like_count=Count("like_article", distinct=True))
                .order_by("-created_at")
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = get_object_or_404(
            Category, id=self.kwargs.get("category_id")
        )
        context["category_list"] = Category.objects.all()
        context["sort"] = self.request.GET.get("sort", "最新")
        return context


@method_decorator(login_required, name="dispatch")
class NewView(FormView):
    template_name = "articles/new.html"
    form_class = ArticleForm
    success_url = reverse_lazy("articles:index")

    def get_initial(self):
        initial = super().get_initial()
        initial["author"] = self.request.user.username
        return initial

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        article.category_id = self.kwargs.get("category_id")
        article.save()
        return redirect("articles:index", category_id=self.kwargs.get("category_id"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["author"] = self.request.user
        context["category"] = get_object_or_404(
            Category, id=self.kwargs.get("category_id")
        )
        context["category_list"] = Category.objects.all()
        return context


@method_decorator(login_required, name="dispatch")
class ShowView(DetailView):
    model = Article
    extra_context = {"comment_form": CommentForm()}

    def get_initial(self):
        initial = super().get_initial()
        initial["member"] = self.request.user.username
        return initial

    def get_queryset(self):
        like_subquery = LikeArticle.objects.filter(
            like_by_article_id=self.request.user.id, like_article_id=OuterRef("pk")
        )
        return Article.objects.with_count().annotate(is_like=Exists(like_subquery))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        like_comment_subquery = LikeComment.objects.filter(
            like_by_id=self.request.user.id, like_comment_id=OuterRef("pk")
        ).values("pk")
        comments_with_likes = self.object.comments.annotate(
            is_like=Exists(like_comment_subquery), like_count=Count("like_comment")
        ).prefetch_related("member")
        context["comments"] = comments_with_likes
        context["comment_form"] = CommentForm(initial={"member": self.request.user.id})
        context["category_list"] = Category.objects.all()
        return context

    def post(self, request, pk):
        article = self.get_object()
        form = CommentForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
        return redirect("articles:show", pk=article.id)


@login_required
@require_POST
def create(request, category_id):
    form = ArticleForm(request.POST, request.FILES)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.category_id = category_id
        article.save()
        url = reverse("articles:index", kwargs={"category_id": article.category_id})
        return redirect(f"{url}?sort=最新")
    return redirect("articles:new", category_id=category_id)


@method_decorator(login_required, name="dispatch")
class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "articles/edit.html"

    def get_success_url(self):
        return reverse_lazy("articles:show", kwargs={"pk": self.object.id})

    def get_object(self, queryset=None):
        obj = super(ArticleUpdateView, self).get_object(queryset=queryset)
        if obj.author != self.request.user:
            return Http404("")
        return obj


@login_required
def edit(request, id):
    article = get_object_or_404(Article, pk=id)
    form = ArticleForm(instance=article)
    return render(
        request, "articles/article_detail.html", {"article": article, "form": form}
    )


class DeleteView(DeleteView):
    model = Article

    def get_success_url(self):
        category_id = self.object.category.id
        return reverse("articles:index", kwargs={"category_id": category_id})


@login_required
@require_POST
def add_like(req, pk):
    article = get_object_or_404(Article, id=pk)
    article.like_article.add(req.user)
    article.like_count = article.like_article.count()
    article.is_like = True
    return render(req, "articles/shared/like_button.html", {"article": article})


@login_required
@require_POST
def remove_like(req, pk):
    article = get_object_or_404(Article, id=pk)
    article.like_article.remove(req.user)
    article.like_count = article.like_article.count()
    article.is_like = False
    return render(req, "articles/shared/like_button.html", {"article": article})

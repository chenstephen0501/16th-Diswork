from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib import messages
from members.models import Member
from .models import Comment, LikeComment
from .forms import CommentForm
from articles.models import Article
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name="dispatch")
class CommentListView(ListView):
    model = Comment
    template_name = "comments/article_detail.html"
    context_object_name = "comments"

    def get_queryset(self):
        member_id = self.kwargs["id"]
        self.member = get_object_or_404(Member, id=member_id)
        return Comment.objects.filter(member=self.member).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["member_id"] = self.member.id
        context["form"] = CommentForm()
        return context


@method_decorator(login_required, name="dispatch")
class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "articles/article_detail.html"

    def form_valid(self, form):
        article_id = self.kwargs["pk"]
        article = get_object_or_404(Article, pk=article_id)

        form.instance.article = article
        form.instance.member = self.request.user

        self.object = form.save()
        return redirect("articles:show", pk=article_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member_id = self.request.user.id
        member = get_object_or_404(Member, id=member_id)
        article = get_object_or_404(Article, id=self.kwargs["pk"])
        context["member_id"] = member_id
        context["comments"] = Comment.objects.filter(member=member).order_by(
            "-created_at"
        )
        context["article"] = article
        return context


@require_POST
def delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    article_id = comment.article_id
    comment.delete()
    return redirect("articles:show", pk=article_id)


@login_required
@require_POST
def add_like(req, pk):
    comment = get_object_or_404(Comment, id=pk)
    comment.like_comment.add(req.user)
    comment.save()
    comment.is_like = True
    comment.like_count = LikeComment.objects.filter(like_by=req.user).count()
    return render(req, "shared/like_comment_btn.html", {"comment": comment})


@login_required
@require_POST
def remove_like(req, pk):
    comment = get_object_or_404(Comment, id=pk)
    comment.like_comment.remove(req.user)
    comment.is_like = False
    comment.like_count = LikeComment.objects.filter(like_by=req.user).count()
    return render(req, "shared/like_comment_btn.html", {"comment": comment})

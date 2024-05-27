from django.shortcuts import get_object_or_404, redirect, HttpResponse, render
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib import messages
from members.models import Member
from .models import Comment, LikeComment
from .forms import CommentForm
from articles.models import Article
from django.contrib.auth.decorators import login_required


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


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "articles/article_detail.html"

    def form_valid(self, form):
        article_id = self.kwargs["pk"]
        article = get_object_or_404(Article, pk=article_id)
        form.instance.article = article
        self.object = form.save()
        messages.success(self.request, "已新增留言！！！")
        return redirect("articles:show", pk=article_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member_id = self.kwargs["id"]
        member = get_object_or_404(Member, id=member_id)
        context["member_id"] = member_id
        context["comments"] = Comment.objects.filter(member=member).order_by(
            "-created_at"
        )
        return context


@require_POST
def delete(req, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect("articles:show", pk=comment.article_id)

@login_required
@require_POST
def add_like(req, pk):
    LikeComment.objects.create(like_by_id = req.user.id, like_comment_id = pk)
    return HttpResponse("")

@login_required
@require_POST
def remove_like(req, pk):
    try:
        like = LikeComment.objects.get(like_by_id = req.user.id, like_comment_id = pk)
        like.delete()
    except:
        pass
    return HttpResponse("")

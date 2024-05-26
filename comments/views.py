from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib import messages
from members.models import Member
from articles.models import Article
from .models import Comment
from .forms import CommentForm
from django.views.decorators.http import require_POST


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

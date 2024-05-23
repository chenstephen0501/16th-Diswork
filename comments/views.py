from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib import messages
from members.models import Member
from .models import Comment
from .forms import CommentForm

class CommentListView(ListView):
    model = Comment
    template_name = "comments/comment_area.html"
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
    template_name = "comments/comment_area.html"
    
    def form_valid(self, form):
        member_id = self.kwargs["id"]
        member = get_object_or_404(Member, id=member_id)
        form.instance.member = member
        self.object = form.save()
        messages.success(self.request, "已新增留言！！！")
        return redirect("comments:comment_area", id=member_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member_id = self.kwargs["id"]
        member = get_object_or_404(Member, id=member_id)
        context["member_id"] = member_id
        context["comments"] = Comment.objects.filter(member=member).order_by("-created_at")
        return context

class CommentDeleteView(DeleteView):
    model = Comment
    def get_success_url(self):
        member_id = self.object.member.id
        return reverse_lazy("comments:comment_area", kwargs={"id":member_id})
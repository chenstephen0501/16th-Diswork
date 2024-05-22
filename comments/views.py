from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.http import require_POST
from members.models import Member
from .forms import CommentForm
from .models import Comment
from django.views.generic import DeleteView
from django.urls import reverse

@require_POST
def create(request, id):
    member = get_object_or_404(Member, id=id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.member = member
        comment.save()
    return redirect("article:show", id=member.id)

class deleteMemberView(DeleteView):
    model = Member
    
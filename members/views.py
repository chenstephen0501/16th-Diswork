from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.generic import TemplateView, FormView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from .models import Member
from .forms import MemberUpdateForm

# email check start
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.encoding import force_str
# email check end

# 登入
class LoginView(FormView):
    template_name = "registration/login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


# 登出
class LogoutView(TemplateView):
    template_name = "registration/logout.html"

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "登出成功！")
        return redirect("index")


# 註冊
class RegisterView(FormView):
    template_name = "registration/register.html"
    form_class = SignUpForm
    success_url = reverse_lazy("members:login")
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False # is_activate db column，預設尚未驗證
        user.save()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        link = self.request.build_absolute_uri(reverse('members:activate', kwargs={'uidb64': uid, 'token': token}))
        # 發送郵件
        send_mail(
            'Diswork會員驗證信件',
            '點擊此連結驗證您的帳戶： {}'.format(link),
            'dali175666@gmail.com',
            [user.email],
            fail_silently=False,
        )
        messages.success(self.request, "請至您的註冊信箱查看信件並完成註冊。")
        return super().form_valid(form)

class MemberUpdateView(UpdateView):
    model = Member
    form_class = MemberUpdateForm
    template_name = "registration/edit.html"
    context_object_name = "user"

    def get_success_url(self):
        return reverse_lazy("index")

    def get_object(self, queryset=None):
        return self.request.user

# mail驗證 2024/5/9 增加 -- Jeter
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Member.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, '您的帳號已驗證成功！')
        return redirect('members:login')
    else:
        messages.error(request, '驗證連結無效！')
        return redirect('members:register')
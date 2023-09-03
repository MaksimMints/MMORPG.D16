from django.contrib.auth import logout
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView

from .forms import UserForm, SignUpForm, ConfirmationSignUpForm


class SingUpView(CreateView): #регистрация нового пользователя
    model = User
    template_name = 'registration/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('signup_mail_sent')


def signup_mail_sent_view(request):
    context = {}
    logout(request)
    return HttpResponse(render(request, 'registration/signup_email_sent.html', context))


class ConfirmationSignUp(UpdateView):
    raise_exception = True
    form_class = ConfirmationSignUpForm
    model = User
    template_name = 'registration/conf_signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.cleaned_data.get('user')
        user.is_active = True
        user_auth = Group.objects.get(name="user_auth")
        user.groups.add(user_auth)
        user.save()
        return response


class UserProfile(UpdateView):
    template_name = 'user_profile.html'
    form_class = UserForm
    success_url = reverse_lazy('bulletin_board')

    def get_object(self, **kwargs):
        user = self.request.user
        return User.objects.get(username=user)



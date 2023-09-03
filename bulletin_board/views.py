from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView
)
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import BulletinForm, DetailFormWithResponse
from .filters import ResponseFilter


class BulletinList(ListView):
    model = Bulletin
    template_name = 'bulletins.html'
    context_object_name = 'bulletins'


class BulletinDetail(DetailView):
    # model = Bulletin
    template_name = 'bulletin.html'
    queryset = Bulletin.objects.all()
    # context_object_name = 'bulletin'
    form_class = DetailFormWithResponse
    extra_context = {'form': DetailFormWithResponse}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        bull_author = Bulletin.objects.get(id=pk).user
        current_user = self.request.user
        if current_user.is_authenticated:

            if bull_author == self.request.user:
                context['surf_response'] = False
                context['message_response'] = False

            elif Response.objects.filter(respAuthor=self.request.user).filter(respBulletin=pk).exists():
                context['surf_response'] = False
                context['message_response'] = True

            # если ты не автор объявления, и не сделал отклик ранее, то поле отображается
            else:
                context['surf_response'] = True
                context['message_response'] = False

        return context

    def post(self, request, bulletin_id=None, *args, **kwargs):
        """При отправки формы выполнить следующий код"""

        form = DetailFormWithResponse(request.POST)

        if form.is_valid():

            form.instance.respBulletin_id = self.kwargs.get('pk')
            form.instance.respAuthor = self.request.user
            form.save()

        return redirect(request.META.get('HTTP_REFERER'))


class BulletinCreate(LoginRequiredMixin, CreateView):
    form_class = BulletinForm #форма создания объявления
    model = Bulletin
    template_name = 'bulletin_create.html'

    def form_valid(self, form): #Автозаполнение поля user
        form.instance.user = self.request.user
        return super().form_valid(form)


class BulletinUpdate(LoginRequiredMixin, UpdateView):
    form_class = BulletinForm
    model = Bulletin
    template_name = 'bulletin_edit.html'


class ResponseList(ListView):
    """Страница откликов на объявления пользователя"""
    model = Response
    template_name = 'response_list.html'
    context_object_name = 'response'

    def get_queryset(self, **kwargs):
        user_id = self.request.user.id
        return Response.objects.filter(respBulletin__user=user_id).filter(status_no=False).filter(status_ok=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ResponseFilter(self.request.GET, queryset=self.get_queryset())
        return context


class ResponseAccept(View):

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        response = Response.objects.get(pk=pk)
        response.status_ok = 1
        response.status_no = 0
        response.save()

        return redirect('response')


class ResponseRemove(View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        response = Response.objects.get(id=pk)
        response.status_no = 1
        response.status_ok = 0
        response.save()

        return redirect('response')

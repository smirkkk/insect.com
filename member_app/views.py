import json
import time

from allauth.account.views import PasswordChangeView
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import logout

# Create your views here.
from django.views.generic.base import View

from member_app.models import Profile, NonMemberSession


class ProfileView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request=self.request, context=context, template_name='member/profile.html')

    def post(self, request):
        pass


class NicknameDuplicateCheck(View):
    def post(self, request):
        nickname = self.request.POST.get('nickname')
        if Profile.objects.filter(nickname=nickname).exists() or NonMemberSession.objects.filter(
                nickname=nickname).exists():
            context = {'status': 'duplicated'}
        else:
            request.user.profile.nickname = nickname
            request.user.profile.save()

            context = {'status': 'success'}
        return HttpResponse(json.dumps(context), content_type="application/json")


class ChangeEmailView(View):
    def post(self, request):
        email = self.request.POST.get('email')
        request.user.email = email
        request.user.save()

        context = {'status': 'success'}
        return HttpResponse(json.dumps(context), content_type="application/json")


class CustomPasswordChangeView(PasswordChangeView):
    @property
    def success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)

        return '/accounts/login'

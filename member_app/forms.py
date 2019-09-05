from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Profile


class SignupForm(forms.Form):
    nickname = forms.CharField(label=_('닉네임'),
                            max_length=30,
                            widget=forms.TextInput(
                                attrs={'placeholder':
                                           _('ex) 파밍하는 티모'), }))

    def signup(self, request, user):
        user.save()

        profile = Profile()
        profile.user = user
        profile.nickname = self.cleaned_data['nickname']
        profile.save()
